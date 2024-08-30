import gradio as gr
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import math
from sklearn.metrics.pairwise import cosine_similarity
import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms, models, datasets
import insightface
from insightface.app import FaceAnalysis

# Define paths and load model for classification
model_path = '/home/abp/Documents/ABPProduction/ABP/FaceVerification/Version5/resnet_model20.pth'
data_dir = '/home/abp/Documents/ABPProduction/ABP/FaceVerification/Version3/Dataset'

# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load class names
train_dataset = datasets.ImageFolder(root=data_dir)
class_names = train_dataset.classes

# Initialize the model
model = models.resnet18(pretrained=False)  # Initialize model without pre-trained weights
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, len(class_names))  # Adjust the final layer for classification

# Load the trained model
model.load_state_dict(torch.load(model_path))
model = model.to(device)
model.eval()

# Define transformation for inference
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Define face matching functions
try:
    app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
    app.prepare(ctx_id=-1)
except Exception as e:
    print(f"Error loading model: {e}")
    app = None

def getFace(image):
    try:
        imagearr = np.asarray(image)
        faces = app.get(imagearr)
        if len(faces) == 1:
            return faces[0]["embedding"]
        else:
            print("Face count mismatch")
            return None
    except Exception as e:
        print(f"Error processing face from image: {e}")
        return None

def compareFaceToDocument(face_image, document_image):
    faceEmbed = getFace(face_image)
    DocumentEmbed = getFace(document_image)
    if faceEmbed is not None and DocumentEmbed is not None:
        similarity = cosine_similarity([faceEmbed], [DocumentEmbed])
        percnt = (math.pi - math.acos(similarity)) * 100 / math.pi
        return percnt
    else:
        print("Mismatch in face embeddings")
        return None

# Define function to predict document class
def predict(image):
    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image)
        probabilities = F.softmax(output, dim=1)
        confidence, predicted = torch.max(probabilities, 1)

    class_name = class_names[predicted.item()]
    confidence_score = confidence.item()
    return class_name, confidence_score

# Gradio interface function
def process_images(face_image, document_image):
    # Predict Document Type
    document_class_name, document_confidence = predict(document_image)
    result = f'\nDocument Type: {document_class_name}\nConfidence score: {document_confidence:.4f}\n\n'

    # Check if confidence is above threshold
    if document_confidence > 0.8:
        # Perform face match
        similarity_percentage = compareFaceToDocument(face_image, document_image)
        if similarity_percentage is not None:
            result += f'\nFace similarity percentage: {similarity_percentage:.2f}%\n'
        else:
            result += 'Face comparison failed.'
    else:
        result += 'Low Confidence Score. Rejected.'
    
    return result

# Define the Gradio interface
iface = gr.Interface(
    fn=process_images,
    inputs=[
        gr.Textbox(label="Face Image URL"),
        gr.Textbox(label="Document Image URL")
    ],
    outputs=[
        gr.Image(type="pil", label="Face Image"),
        gr.Image(type="pil", label="Document Image"),
        gr.Textbox(label="Result")
    ],
    title="Face and Document Verification",
    description="Upload a face image and a document image to verify the document type and match the face."
)

if __name__ == "__main__":
    iface.launch()