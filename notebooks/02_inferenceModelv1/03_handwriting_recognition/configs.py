import os
from datetime import datetime

# liberia helper
from mltu.configs import BaseModelConfigs

#   Puedes encontrar los hiperparametros del modelo
#   separe lo que no conviene modificar como la geometria del modelo
#   en su lugar es preferible modificar los parametros de training
#
#

class ModelConfigs(BaseModelConfigs):
    def __init__(self):
        super().__init__()
        self.model_path = os.path.join("Models/03_handwriting_recognition", datetime.strftime(datetime.now(), "%Y%m%d%H%M"))
        # se permite un update previo del modelo
        self.vocab = ""
            # hacer un webscraping y tener una lista de todos los nombres de medicamentos
                # tener posibles abreviaciones
        # geometria del modelo
        self.height = 32
        self.width = 128
        self.max_text_length = 0
        self.batch_size = 16
        # hiperparametros de training
        self.learning_rate = 0.0005
        self.train_epochs = 1000
        self.train_workers = 20