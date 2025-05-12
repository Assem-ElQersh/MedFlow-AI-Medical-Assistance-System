import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, models
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
from tqdm import tqdm
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Configuration Parameters (Easily adjustable for experimentation)
CONFIG = {
    'data_dir': 'ml_models/data_preparation/datasets/pneumonia',
    'model_save_dir': 'ml_models/disease_classifiers/pneumonia/models',
    'results_dir': 'ml_models/disease_classifiers/pneumonia/results',
    'image_size': 224,  # Standard size for most pretrained models
    'batch_size': 32,
    'num_epochs': 50,
    'learning_rate': 0.001,
    'weight_decay': 1e-4,
    'early_stopping_patience': 10,
    'model_type': 'resnet50',  # Options: 'resnet50', 'densenet121', 'efficientnet_b0'
    'use_pretrained': True,
    'num_classes': 2,
    'class_names': ['NORMAL', 'PNEUMONIA'],
    'device': torch.device('cuda' if torch.cuda.is_available() else 'cpu')
}

class PneumoniaDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.classes = CONFIG['class_names']
        self.class_to_idx = {cls_name: i for i, cls_name in enumerate(self.classes)}
        
        self.images = []
        self.labels = []
        
        # Load all images and their labels
        for class_name in self.classes:
            class_dir = os.path.join(data_dir, class_name)
            for img_name in os.listdir(class_dir):
                if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    self.images.append(os.path.join(class_dir, img_name))
                    self.labels.append(self.class_to_idx[class_name])
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        img_path = self.images[idx]
        label = self.labels[idx]
        
        # Load and transform image
        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        
        return image, label

def get_model(model_type, num_classes):
    """Initialize the specified model architecture"""
    if model_type == 'resnet50':
        model = models.resnet50(pretrained=CONFIG['use_pretrained'])
        model.fc = nn.Linear(model.fc.in_features, num_classes)
    elif model_type == 'densenet121':
        model = models.densenet121(pretrained=CONFIG['use_pretrained'])
        model.classifier = nn.Linear(model.classifier.in_features, num_classes)
    elif model_type == 'efficientnet_b0':
        model = models.efficientnet_b0(pretrained=CONFIG['use_pretrained'])
        model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")
    
    return model

def train_model(model, train_loader, val_loader, criterion, optimizer, num_epochs):
    """Train the model with early stopping"""
    best_val_acc = 0.0
    patience_counter = 0
    history = {'train_loss': [], 'train_acc': [], 'val_loss': [], 'val_acc': []}
    
    for epoch in range(num_epochs):
        # Training phase
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0
        
        train_bar = tqdm(train_loader, desc=f'Epoch {epoch+1}/{num_epochs} [Train]')
        for inputs, labels in train_bar:
            inputs, labels = inputs.to(CONFIG['device']), labels.to(CONFIG['device'])
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            _, predicted = outputs.max(1)
            train_total += labels.size(0)
            train_correct += predicted.eq(labels).sum().item()
            
            train_bar.set_postfix({
                'loss': train_loss/train_total,
                'acc': 100.*train_correct/train_total
            })
        
        # Validation phase
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        
        with torch.no_grad():
            val_bar = tqdm(val_loader, desc=f'Epoch {epoch+1}/{num_epochs} [Val]')
            for inputs, labels in val_bar:
                inputs, labels = inputs.to(CONFIG['device']), labels.to(CONFIG['device'])
                
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item()
                _, predicted = outputs.max(1)
                val_total += labels.size(0)
                val_correct += predicted.eq(labels).sum().item()
                
                val_bar.set_postfix({
                    'loss': val_loss/val_total,
                    'acc': 100.*val_correct/val_total
                })
        
        # Calculate epoch metrics
        train_loss = train_loss/len(train_loader)
        train_acc = 100.*train_correct/train_total
        val_loss = val_loss/len(val_loader)
        val_acc = 100.*val_correct/val_total
        
        # Update history
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)
        
        print(f'\nEpoch {epoch+1}/{num_epochs}:')
        print(f'Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%')
        print(f'Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%')
        
        # Early stopping check
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            patience_counter = 0
            # Save best model
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_acc': val_acc,
            }, os.path.join(CONFIG['model_save_dir'], 'best_model.pth'))
        else:
            patience_counter += 1
            if patience_counter >= CONFIG['early_stopping_patience']:
                print(f'Early stopping triggered after {epoch+1} epochs')
                break
    
    return history

def evaluate_model(model, test_loader):
    """Evaluate the model on test data"""
    model.eval()
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for inputs, labels in tqdm(test_loader, desc='Evaluating'):
            inputs, labels = inputs.to(CONFIG['device']), labels.to(CONFIG['device'])
            outputs = model(inputs)
            _, preds = outputs.max(1)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    
    # Generate classification report
    report = classification_report(all_labels, all_preds, target_names=CONFIG['class_names'])
    print("\nClassification Report:")
    print(report)
    
    # Generate confusion matrix
    cm = confusion_matrix(all_labels, all_preds)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=CONFIG['class_names'],
                yticklabels=CONFIG['class_names'])
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.savefig(os.path.join(CONFIG['results_dir'], 'confusion_matrix.png'))
    plt.close()
    
    return report, cm

def plot_training_history(history):
    """Plot training history"""
    plt.figure(figsize=(12, 4))
    
    # Plot training & validation accuracy
    plt.subplot(1, 2, 1)
    plt.plot(history['train_acc'], label='Train')
    plt.plot(history['val_acc'], label='Validation')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy (%)')
    plt.legend()
    
    # Plot training & validation loss
    plt.subplot(1, 2, 2)
    plt.plot(history['train_loss'], label='Train')
    plt.plot(history['val_loss'], label='Validation')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(CONFIG['results_dir'], 'training_history.png'))
    plt.close()

def main():
    # Create necessary directories
    os.makedirs(CONFIG['model_save_dir'], exist_ok=True)
    os.makedirs(CONFIG['results_dir'], exist_ok=True)
    
    # Data transforms
    train_transform = transforms.Compose([
        transforms.Resize((CONFIG['image_size'], CONFIG['image_size'])),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((CONFIG['image_size'], CONFIG['image_size'])),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Create datasets
    train_dataset = PneumoniaDataset(
        os.path.join(CONFIG['data_dir'], 'train'),
        transform=train_transform
    )
    val_dataset = PneumoniaDataset(
        os.path.join(CONFIG['data_dir'], 'val'),
        transform=val_transform
    )
    test_dataset = PneumoniaDataset(
        os.path.join(CONFIG['data_dir'], 'test'),
        transform=val_transform
    )
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=CONFIG['batch_size'],
                            shuffle=True, num_workers=4)
    val_loader = DataLoader(val_dataset, batch_size=CONFIG['batch_size'],
                          shuffle=False, num_workers=4)
    test_loader = DataLoader(test_dataset, batch_size=CONFIG['batch_size'],
                           shuffle=False, num_workers=4)
    
    # Initialize model
    model = get_model(CONFIG['model_type'], CONFIG['num_classes'])
    model = model.to(CONFIG['device'])
    
    # Loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=CONFIG['learning_rate'],
                          weight_decay=CONFIG['weight_decay'])
    
    # Train model
    print(f"Training {CONFIG['model_type']} model...")
    history = train_model(model, train_loader, val_loader, criterion, optimizer,
                         CONFIG['num_epochs'])
    
    # Plot training history
    plot_training_history(history)
    
    # Load best model for evaluation
    checkpoint = torch.load(os.path.join(CONFIG['model_save_dir'], 'best_model.pth'))
    model.load_state_dict(checkpoint['model_state_dict'])
    
    # Evaluate on test set
    print("\nEvaluating best model on test set...")
    report, cm = evaluate_model(model, test_loader)
    
    # Save results
    with open(os.path.join(CONFIG['results_dir'], 'classification_report.txt'), 'w') as f:
        f.write(report)
    
    # Save configuration
    with open(os.path.join(CONFIG['results_dir'], 'config.txt'), 'w') as f:
        for key, value in CONFIG.items():
            f.write(f"{key}: {value}\n")

if __name__ == '__main__':
    main() 