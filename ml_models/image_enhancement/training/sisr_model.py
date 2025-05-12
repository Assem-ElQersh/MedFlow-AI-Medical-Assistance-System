import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

# Configuration Parameters
CONFIG = {
    'data_dir': 'ml_models/image_enhancement/data',
    'model_save_dir': 'ml_models/image_enhancement/models',
    'results_dir': 'ml_models/image_enhancement/results',
    'image_size': 256,
    'scale_factor': 4,  # Upscaling factor
    'batch_size': 16,
    'num_epochs': 100,
    'learning_rate': 0.0001,
    'device': torch.device('cuda' if torch.cuda.is_available() else 'cpu')
}

class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(channels)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(channels)

    def forward(self, x):
        residual = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.bn2(out)
        out += residual
        return out

class SISRModel(nn.Module):
    def __init__(self, scale_factor=4):
        super(SISRModel, self).__init__()
        self.scale_factor = scale_factor
        
        # Initial feature extraction
        self.conv1 = nn.Conv2d(3, 64, kernel_size=9, padding=4)
        self.relu = nn.ReLU(inplace=True)
        
        # Residual blocks
        self.res_blocks = nn.Sequential(
            ResidualBlock(64),
            ResidualBlock(64),
            ResidualBlock(64),
            ResidualBlock(64),
            ResidualBlock(64)
        )
        
        # Upsampling layers
        self.upsampling = nn.Sequential(
            nn.Conv2d(64, 256, kernel_size=3, padding=1),
            nn.PixelShuffle(2),
            nn.Conv2d(64, 256, kernel_size=3, padding=1),
            nn.PixelShuffle(2)
        )
        
        # Final convolution
        self.conv2 = nn.Conv2d(64, 3, kernel_size=9, padding=4)

    def forward(self, x):
        out = self.relu(self.conv1(x))
        residual = out
        out = self.res_blocks(out)
        out = out + residual
        out = self.upsampling(out)
        out = self.conv2(out)
        return out

class MedicalImageDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.image_files = []
        
        # Load all medical images
        for root, _, files in os.walk(data_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.dcm')):
                    self.image_files.append(os.path.join(root, file))
    
    def __len__(self):
        return len(self.image_files)
    
    def __getitem__(self, idx):
        img_path = self.image_files[idx]
        
        # Load image
        if img_path.lower().endswith('.dcm'):
            import pydicom
            image = pydicom.dcmread(img_path).pixel_array
            image = Image.fromarray(image)
        else:
            image = Image.open(img_path).convert('RGB')
        
        # Create low-resolution version
        lr_size = (CONFIG['image_size'] // CONFIG['scale_factor'], 
                  CONFIG['image_size'] // CONFIG['scale_factor'])
        hr_size = (CONFIG['image_size'], CONFIG['image_size'])
        
        lr_image = image.resize(lr_size, Image.BICUBIC)
        hr_image = image.resize(hr_size, Image.BICUBIC)
        
        if self.transform:
            lr_image = self.transform(lr_image)
            hr_image = self.transform(hr_image)
        
        return lr_image, hr_image

def train_model(model, train_loader, val_loader, criterion, optimizer, num_epochs):
    """Train the SISR model"""
    best_val_loss = float('inf')
    history = {'train_loss': [], 'val_loss': []}
    
    for epoch in range(num_epochs):
        # Training phase
        model.train()
        train_loss = 0.0
        
        train_bar = tqdm(train_loader, desc=f'Epoch {epoch+1}/{num_epochs} [Train]')
        for lr_images, hr_images in train_bar:
            lr_images = lr_images.to(CONFIG['device'])
            hr_images = hr_images.to(CONFIG['device'])
            
            optimizer.zero_grad()
            outputs = model(lr_images)
            loss = criterion(outputs, hr_images)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            train_bar.set_postfix({'loss': train_loss/len(train_loader)})
        
        # Validation phase
        model.eval()
        val_loss = 0.0
        
        with torch.no_grad():
            val_bar = tqdm(val_loader, desc=f'Epoch {epoch+1}/{num_epochs} [Val]')
            for lr_images, hr_images in val_bar:
                lr_images = lr_images.to(CONFIG['device'])
                hr_images = hr_images.to(CONFIG['device'])
                
                outputs = model(lr_images)
                loss = criterion(outputs, hr_images)
                val_loss += loss.item()
                val_bar.set_postfix({'loss': val_loss/len(val_loader)})
        
        # Calculate epoch metrics
        train_loss = train_loss/len(train_loader)
        val_loss = val_loss/len(val_loader)
        
        # Update history
        history['train_loss'].append(train_loss)
        history['val_loss'].append(val_loss)
        
        print(f'\nEpoch {epoch+1}/{num_epochs}:')
        print(f'Train Loss: {train_loss:.4f}')
        print(f'Val Loss: {val_loss:.4f}')
        
        # Save best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_loss': val_loss,
            }, os.path.join(CONFIG['model_save_dir'], 'best_model.pth'))
    
    return history

def plot_training_history(history):
    """Plot training history"""
    plt.figure(figsize=(10, 5))
    plt.plot(history['train_loss'], label='Train Loss')
    plt.plot(history['val_loss'], label='Validation Loss')
    plt.title('Training History')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.savefig(os.path.join(CONFIG['results_dir'], 'training_history.png'))
    plt.close()

def main():
    # Create necessary directories
    os.makedirs(CONFIG['data_dir'], exist_ok=True)
    os.makedirs(CONFIG['model_save_dir'], exist_ok=True)
    os.makedirs(CONFIG['results_dir'], exist_ok=True)
    
    # Define transforms
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Create datasets
    train_dataset = MedicalImageDataset(
        os.path.join(CONFIG['data_dir'], 'train'),
        transform=transform
    )
    val_dataset = MedicalImageDataset(
        os.path.join(CONFIG['data_dir'], 'val'),
        transform=transform
    )
    
    # Create data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=CONFIG['batch_size'],
        shuffle=True,
        num_workers=4
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=CONFIG['batch_size'],
        shuffle=False,
        num_workers=4
    )
    
    # Initialize model
    model = SISRModel(scale_factor=CONFIG['scale_factor'])
    model = model.to(CONFIG['device'])
    
    # Define loss function and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=CONFIG['learning_rate'])
    
    # Train model
    history = train_model(model, train_loader, val_loader, criterion, optimizer, CONFIG['num_epochs'])
    
    # Plot training history
    plot_training_history(history)

if __name__ == '__main__':
    main() 