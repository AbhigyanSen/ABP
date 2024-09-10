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
import warnings
warnings.filterwarnings("ignore")

# Define paths and load model for classification
model_path = 'resnet18_model50_frozen.pth'
# data_dir = '/home/abp/Documents/ABPProduction/ABP/FaceVerification/Version3/Dataset'

# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load class names
# train_dataset = datasets.ImageFolder(root=data_dir)
# class_names = train_dataset.classes
class_names = ['AadharFront', 'DrivingFront', 'PanFront', 'VoterFront']

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
    transforms.ToTensor()
    # transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Define face matching functions
try:
    app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
    app.prepare(ctx_id=-1)
except Exception as e:
    print(f"Error loading model: {e}")
    app = None

def getFace(url):
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content)).convert("RGB")
        imagearr = np.asarray(image)
        faces = app.get(imagearr)
        if len(faces) == 1:
            return faces[0]["embedding"]
        else:
            print("Face count mismatch")
            return None
    except Exception as e:
        print(f"Error processing face from URL {url}: {e}")
        return None

def compareFaceToDocument(face_url, document_url):
    faceEmbed = getFace(face_url)
    DocumentEmbed = getFace(document_url)
    if faceEmbed is not None and DocumentEmbed is not None:
        similarity = cosine_similarity([faceEmbed], [DocumentEmbed])
        # percnt = (math.pi - math.acos(similarity)) * 100 / math.pi
        return similarity
    else:
        print("Mismatch in face embeddings")
        return None

# Define function to load image from URL and predict
def load_image_from_url(url):
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content)).convert('RGB')
        return image
    except Exception as e:
        print(f"Error loading image from URL {url}: {e}")
        return None

def predict(image_url):
    image = load_image_from_url(image_url)
    if image is None:
        return None, 0.0

    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image)
        probabilities = F.softmax(output, dim=1)
        confidence, predicted = torch.max(probabilities, 1)

    class_name = class_names[predicted.item()]
    confidence_score = confidence.item()
    # print(image_url)
    return class_name, confidence_score

# Combined process
def process_images(face_url, document_url):
    # Predict Document Type
    document_class_name, document_confidence = predict(document_url)
    print(f'\nDocument Type: {document_class_name}')
    print(f'Confidence score: {document_confidence:.4f}')
    print("\n")

    # Check if confidence is above threshold
    if document_confidence > 0.8:
        # Perform face match
        similarity_percentage = compareFaceToDocument(face_url, document_url)
        if similarity_percentage is not None:
            print(f'Face similarity percentage: {similarity_percentage}')
            return f'Face similarity percentage: {similarity_percentage}'
        else:
            print('Face comparison failed.')
            return 'Face comparison failed.'
    else:
        print('Low Confidence Score. Rejected.')
        return "Low Confidence Score. Rejected."


# Example usage
if __name__ == "__main__":
    face_url = "https://cdn.abpweddings.com/documents/233a8247f88b7baa80ceeccc376c9cc2/1720013554470.webp?width=150"
    document_url = "https://cdn.abpweddings.com/documents/233a8247f88b7baa80ceeccc376c9cc2/1715496020276.jpg"
    process_images(face_url, document_url)