import tensorflow as tf
try: [tf.config.experimental.set_memory_growth(gpu, True) for gpu in tf.config.experimental.list_physical_devices("GPU")]
except: pass

from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, TensorBoard

from mltu.preprocessors import ImageReader
from mltu.transformers import ImageResizer, LabelIndexer, LabelPadding, ImageShowCV2
from mltu.augmentors import RandomBrightness, RandomRotate, RandomErodeDilate, RandomSharpen
from mltu.annotations.images import CVImage

from mltu.tensorflow.dataProvider import DataProvider
from mltu.tensorflow.losses import CTCloss
from mltu.tensorflow.callbacks import Model2onnx, TrainLogger
from mltu.tensorflow.metrics import CWERMetric

from model import train_model
from configs import ModelConfigs

import os
import tarfile
from tqdm import tqdm
from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile


def download_and_unzip(url, extract_to="Datasets", chunk_size=1024*1024):
    """ consigue el IAM data set """
    http_response = urlopen(url)

    data = b""
    iterations = http_response.length // chunk_size + 1
    for _ in tqdm(range(iterations)):
        data += http_response.read(chunk_size)

    zipfile = ZipFile(BytesIO(data))
    zipfile.extractall(path=extract_to)


# en caso de no tenerlo descargado, re descarga el data set
dataset_path = os.path.join("Datasets", "IAM_Words")
if not os.path.exists(dataset_path): 
    download_and_unzip("https://git.io/J0fjL", extract_to="Datasets")

    file = tarfile.open(os.path.join(dataset_path, "words.tgz"))
    file.extractall(os.path.join(dataset_path, "words"))

dataset, vocab, max_len = [], set(), 0

# Preprocess the dataset by the specific IAM_Words dataset file structure
words = open(os.path.join(dataset_path, "words.txt"), "r").readlines()
for line in tqdm(words):
    if line.startswith("#"): # simbolo de comentarios
        continue

    line_split = line.split(" ")
    if line_split[1] == "err":
        continue

    folder1 = line_split[0][:3]
    folder2 = "-".join(line_split[0].split("-")[:2])
    file_name = line_split[0] + ".png"
    label = line_split[-1].rstrip("\n")

    rel_path = os.path.join(dataset_path, "words", folder1, folder2, file_name)
    if not os.path.exists(rel_path):
        print(f"File not found: {rel_path}")
        continue

    dataset.append([rel_path, label])
    vocab.update(list(label)) # el vocab total se almacena con los labels
    max_len = max(max_len, len(label))

# Model config configutarion
configs = ModelConfigs()

# Almacena el vocabulario maximo
configs.vocab = "".join(vocab)
configs.max_text_length = max_len
configs.save()

# Este es un objeto con propiedades para dividir y modificar las imagenes
data_provider = DataProvider(
    dataset=dataset,
    skip_validation=True,
    batch_size=configs.batch_size,
    data_preprocessors=[ImageReader(CVImage)],
    transformers=[
        ImageResizer(configs.width, configs.height, keep_aspect_ratio=False),
        LabelIndexer(configs.vocab),
        LabelPadding(max_word_length=configs.max_text_length, padding_value=len(configs.vocab)),
        ],
)

# Training y validación
train_data_provider, val_data_provider = data_provider.split(split = 0.9)
    # [] un ejercicio propuesto es agregar un test_data_provider
    # realizanod un split extra, de manera que una vez estamos feliz con la validación
    # utilizamos datos nunca antes vistos, ni en validación o entrenameinto para medir al modelo

# Incremento del data set
    # aplicar operaciones a la imagen como modificar brillos, rotaciones pequeñas, ...
    # esto hace que las matrices que observa el modelo (las imagenes son numeros para este)
    # sean distintos pero continuen diciendo lo mismo, permaneciendo con su labeles
    # esta es una forma de incrementar los datos y que el modelo entrene en imagens desenfocadas
train_data_provider.augmentors = [
    RandomBrightness(), 
    RandomErodeDilate(),
    RandomSharpen(),
    RandomRotate(angle=10), 
    ]

# Arquitectura del modelo
model = train_model(
    input_dim = (configs.height, configs.width, 3),
    output_dim = len(configs.vocab),
)

# Compulación del modelo
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=configs.learning_rate), 
    loss=CTCloss(), 
    metrics=[CWERMetric(padding_token=len(configs.vocab))],
)
model.summary(line_length=110)

# Callbacks
# se encargan de detener al modelo en caso de que
# 1. el entrenamiento sea demasiado lento, estamos cerca del limite (earlyStopping)
    # puedes modificar la paciencia para buscar otros minimos
earlystopper = EarlyStopping(monitor="val_CER", patience=20, verbose=1)
# 2. checkpoint, guarda el mejor modelo hasta el momento
checkpoint = ModelCheckpoint(f"{configs.model_path}/model.h5", monitor="val_CER", verbose=1, save_best_only=True, mode="min")
trainLogger = TrainLogger(configs.model_path)
# en caso de no tener tensorBoard puedes comentar esta parte
tb_callback = TensorBoard(f"{configs.model_path}/logs", update_freq=1)
# similar al early stopping identifica cuando el entrenamiento converge
reduceLROnPlat = ReduceLROnPlateau(monitor="val_CER", factor=0.9, min_delta=1e-10, patience=10, verbose=1, mode="auto")
model2onnx = Model2onnx(f"{configs.model_path}/model.h5")

# Training
model.fit(
    train_data_provider,
    validation_data=val_data_provider,
    epochs=configs.train_epochs,
    callbacks=[earlystopper, checkpoint, trainLogger, reduceLROnPlat, tb_callback, model2onnx],
    workers=configs.train_workers
)

# CSV
train_data_provider.to_csv(os.path.join(configs.model_path, "train.csv"))
val_data_provider.to_csv(os.path.join(configs.model_path, "val.csv"))