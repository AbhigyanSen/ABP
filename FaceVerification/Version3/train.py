import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
from pathlib import Path

# Set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Define paths and hyperparameters
data_dir = 'Dataset'
batch_size = 32
num_epochs = 20
learning_rate = 0.001

# Data augmentation and normalization
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # ResNet expects 224x224 input images
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Load datasets
train_dataset = datasets.ImageFolder(root=data_dir, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4)

# Initialize ResNet model
model = models.resnet18(pretrained=True)  # You can use resnet50 or resnet34 based on your need
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, len(train_dataset.classes))  # Update the final layer for classification

# Move model to the device
model = model.to(device)

# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Training loop
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * images.size(0)

    epoch_loss = running_loss / len(train_loader.dataset)
    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss:.4f}')

print('Training completed')

# Save the model
torch.save(model.state_dict(), 'resnet_model.pth')
print('Model saved to resnet_model.pth')