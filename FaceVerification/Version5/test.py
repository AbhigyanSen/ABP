import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms, models, datasets
from PIL import Image
from pathlib import Path

# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Define paths
model_path = 'resnet18_model50_frozen.pth'
# data_dir = '/home/abp/Documents/ABPProduction/ABP/FaceVerification/Version3/Dataset'

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

def fhook(module,input,output):
    print(torch.flatten(output))


# Prediction function
def predict(image_path):
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(image)
        probabilities = F.softmax(output, dim=1)
        confidence, predicted = torch.max(probabilities, 1)

    class_name = class_names[predicted.item()]
    confidence_score = confidence.item()
    return class_name, confidence_score

# Example usage
if __name__ == "__main__":
    model.avgpool.register_forward_hook(fhook)
    # for a,b in model.named_modules():
    #     print(a)
    import sys
    if len(sys.argv) != 2:
        print("Usage: python test.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    class_name, confidence_score = predict(image_path)
    print(f'\nDocument Type: {class_name}')
    print(f'Confidence score: {confidence_score:.4f}')