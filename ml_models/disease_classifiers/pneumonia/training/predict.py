import os
import torch
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt
from pneumonia_classifier import get_model, CONFIG
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration Parameters
CONFIG = {
    'data_dir': 'ml_models/disease_classifiers/pneumonia/data/processed/pneumonia',
    'model_save_dir': 'ml_models/disease_classifiers/pneumonia/models',
    'results_dir': 'ml_models/disease_classifiers/pneumonia/results',
    'image_size': 224,
    'model_type': 'resnet50',  # Default to ResNet50, can be changed to match your trained model
    'num_classes': 2,
    'class_names': ['NORMAL', 'PNEUMONIA'],
    'device': torch.device('cuda' if torch.cuda.is_available() else 'cpu')
}

def load_model(model_path):
    """Load a trained model"""
    logger.info(f"Loading model from {model_path}")
    
    # Initialize model
    model = get_model(CONFIG['model_type'], CONFIG['num_classes'])
    
    # Load state dict
    checkpoint = torch.load(model_path, map_location=CONFIG['device'])
    model.load_state_dict(checkpoint['model_state_dict'])
    
    # Set to evaluation mode
    model.eval()
    model = model.to(CONFIG['device'])
    
    logger.info(f"Model loaded successfully. Using device: {CONFIG['device']}")
    return model

def predict_image(model, image_path):
    """Make prediction for a single image"""
    logger.info(f"Processing image: {image_path}")
    
    # Load and preprocess image
    image = Image.open(image_path).convert('RGB')
    
    # Define transform
    transform = transforms.Compose([
        transforms.Resize((CONFIG['image_size'], CONFIG['image_size'])),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Transform image
    image_tensor = transform(image).unsqueeze(0).to(CONFIG['device'])
    
    # Make prediction
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.softmax(outputs, dim=1)
        predicted_class = torch.argmax(probabilities, dim=1).item()
        confidence = probabilities[0][predicted_class].item()
    
    return {
        'class': CONFIG['class_names'][predicted_class],
        'confidence': confidence,
        'probabilities': probabilities[0].cpu().numpy()
    }

def visualize_prediction(image_path, prediction):
    """Visualize the image and prediction"""
    # Load image
    image = Image.open(image_path).convert('RGB')
    
    # Create figure
    plt.figure(figsize=(10, 5))
    
    # Plot image
    plt.subplot(1, 2, 1)
    plt.imshow(image)
    plt.title('Input Image')
    plt.axis('off')
    
    # Plot probabilities
    plt.subplot(1, 2, 2)
    bars = plt.bar(CONFIG['class_names'], prediction['probabilities'])
    plt.title('Class Probabilities')
    plt.ylim(0, 1)
    
    # Add probability values on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2%}',
                ha='center', va='bottom')
    
    plt.tight_layout()
    return plt.gcf()

def main():
    # Get the best model path
    model_path = os.path.join(CONFIG['model_save_dir'], 'best_model.pth')
    
    if not os.path.exists(model_path):
        logger.error(f"Error: Model not found at {model_path}")
        logger.error("Please train the model first using pneumonia_classifier.py")
        return
    
    # Load model
    logger.info("Loading model...")
    model = load_model(model_path)
    
    # Create results directory for predictions
    pred_dir = os.path.join(CONFIG['results_dir'], 'predictions')
    os.makedirs(pred_dir, exist_ok=True)
    
    # Test on some sample images
    test_dir = os.path.join(CONFIG['data_dir'], 'test')
    if not os.path.exists(test_dir):
        logger.error(f"Test directory not found at {test_dir}")
        logger.error("Please ensure the test data is in the correct location")
        return
        
    for class_name in CONFIG['class_names']:
        class_dir = os.path.join(test_dir, class_name)
        if not os.path.exists(class_dir):
            logger.warning(f"Class directory not found: {class_dir}")
            continue
            
        # Get first image from each class
        for img_name in os.listdir(class_dir)[:2]:  # Test 2 images per class
            img_path = os.path.join(class_dir, img_name)
            
            # Make prediction
            logger.info(f"\nPredicting for {img_path}...")
            prediction = predict_image(model, img_path)
            
            # Print results
            logger.info(f"Predicted class: {prediction['class']}")
            logger.info(f"Confidence: {prediction['confidence']:.2%}")
            
            # Visualize
            fig = visualize_prediction(img_path, prediction)
            save_path = os.path.join(pred_dir, f"pred_{class_name}_{img_name}.png")
            fig.savefig(save_path)
            plt.close(fig)
            logger.info(f"Visualization saved to {save_path}")

if __name__ == '__main__':
    main() 