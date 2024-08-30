import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from torchvision import transforms, models, datasets
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from PIL import Image


# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Define transformation for inference
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Load class names
data_dir = '/home/abp/Documents/ABPProduction/ABP/FaceVerification/Version3/Dataset'
train_dataset = datasets.ImageFolder(root=data_dir,transform=transform)
class_names = train_dataset.classes


# Initialize the model
model = models.resnet18(pretrained=False)  # Initialize model without pre-trained weights
model_path = '/home/abp/Documents/ABPProduction/ABP/FaceVerification/Version4/resnet_model1.pth'
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, len(class_names))  # Adjust the final layer for classification

# Load the trained model
model.load_state_dict(torch.load(model_path))
model = model.to(device)
model.eval()

# Dummy data for demonstration (replace with actual dataset)

data_loader = DataLoader(train_dataset, batch_size=2, shuffle=True)

class FeatureExtractor(torch.nn.Module):
    def __init__(self, model):
        super(FeatureExtractor, self).__init__()
        self.model = model
        self.features = []

    def forward(self, x):
        x = self.model.conv1(x)
        x = self.model.bn1(x)
        x = self.model.relu(x)
        x = self.model.maxpool(x)

        x = self.model.layer1(x)
        x = self.model.layer2(x)
        x = self.model.layer3(x)
        x = self.model.layer4(x)

        x = self.model.avgpool(x)
        x = torch.flatten(x, 1)

        self.features.append(x)
        return x

extractor = FeatureExtractor(model)

features = []
# Extract features
with torch.no_grad():
    for images, _ in data_loader:
        images = images.to(device)
        output_features = extractor(images)
        features.append(output_features)

features = torch.cat(features).to(device)
mean = features.mean(dim=0).to(device)
cov_matrix = torch.cov(features.T).to(device)

# Regularize covariance matrix to make it invertible
cov_matrix += 1e-6 * torch.eye(cov_matrix.size(0)).to(device)
inv_cov_matrix = torch.linalg.inv(cov_matrix).to(device)

def mahalanobis_distance(x, mean, inv_cov_matrix):
    diff = x - mean
    return torch.sqrt(torch.matmul(torch.matmul(diff.unsqueeze(0), inv_cov_matrix), diff.unsqueeze(1)).squeeze())

torch.save(mean, 'meane1.pt')
torch.save(inv_cov_matrix, 'invconvmatrixe1.pt')


# Example with a new image
image_path = "/home/abp/Documents/ABPProduction/ABP/FaceVerification/Version3/Dataset/AadharFront/Adhar Card Front_170512100801.png"
new_image = Image.open(image_path).convert('RGB') #torch.randn(3, 224, 224)
new_image = transform(new_image).unsqueeze(0).to(device)
with torch.no_grad():
    new_features = extractor(new_image).squeeze()
    distance = mahalanobis_distance(new_features, mean, inv_cov_matrix)
    print(f"Mahalanobis Distance: {distance.item()}")