import cv2
import os
import random

# ... (rest of the imports and model loading)

# Function to choose a random image
def choose_random_image(directory):
  supported_extensions = [".png", ".jpg", ".jpeg"]
  all_images = []
  for filename in os.listdir(directory):
    if filename.lower().endswith(tuple(supported_extensions)):
      all_images.append(os.path.join(directory, filename))
  return random.choice(all_images)

# Select a random image path
image_path = choose_random_image("path/to/your/image/folder")

# Make prediction on the image
prediction_text = model.predict(cv2.imread(image_path))

# Print results
print(f"Image: {image_path}")
print(f"Predicted Text: {prediction_text}")

# Optional: Display the image
# ... (OpenCV code to display the image)
