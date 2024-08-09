import torch
from PIL import Image
from transformers import AutoModelForImageClassification, ViTImageProcessor
import torch.nn.functional as F
import requests
from io import BytesIO

# Define the image URL
image_url = "https://cdn.abpweddings.com/documents/0340d385f44319a2e3d70dd9077c98aa/1707180598038.webp"

# Download and open the image
response = requests.get(image_url)
img = Image.open(BytesIO(response.content))

# Load model and processor
model = AutoModelForImageClassification.from_pretrained("Falconsai/nsfw_image_detection")
processor = ViTImageProcessor.from_pretrained('Falconsai/nsfw_image_detection')

# Preprocess image and perform inference
with torch.no_grad():
    inputs = processor(images=img, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits

# Compute probabilities using softmax
probabilities = F.softmax(logits, dim=-1)

# Get predicted label and confidence
predicted_label = logits.argmax(-1).item()
confidence = (probabilities[0, predicted_label].item()) * 100

# Print the results
print(f"Predicted Label: {model.config.id2label[predicted_label]}")
print(f"Confidence: {confidence:.2f}%")