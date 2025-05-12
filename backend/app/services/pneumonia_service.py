import os
import torch
from torchvision import transforms
from PIL import Image
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root to Python path
project_root = str(Path(__file__).parent.parent.parent.parent)
sys.path.append(project_root)

from ml_models.disease_classifiers.pneumonia.training.pneumonia_classifier import get_model

class PneumoniaService:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.models = {}
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        self.class_names = ['NORMAL', 'PNEUMONIA']
        logger.info(f"Initialized PneumoniaService with device: {self.device}")
        
    def load_model(self, model_type: str = 'resnet50'):
        """Load a specific model type if not already loaded"""
        try:
            if model_type not in self.models:
                model_path = os.path.join(
                    project_root,
                    'ml_models/disease_classifiers/pneumonia/models',
                    'best_model.pth'
                )
                
                if not os.path.exists(model_path):
                    logger.error(f"Model not found at {model_path}")
                    raise FileNotFoundError(f"Model not found at {model_path}")
                
                logger.info(f"Loading model from {model_path}")
                # Initialize and load model
                model = get_model(model_type, num_classes=2)
                checkpoint = torch.load(model_path, map_location=self.device)
                model.load_state_dict(checkpoint['model_state_dict'])
                model.eval()
                model = model.to(self.device)
                
                self.models[model_type] = model
                logger.info(f"Model {model_type} loaded successfully")
                
            return self.models[model_type]
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def predict(self, image_path: str, model_type: str = 'resnet50') -> dict:
        """Make prediction for a given image"""
        try:
            # Convert to Path object and resolve
            image_path = Path(image_path).resolve()
            logger.info(f"Processing image: {image_path}")
            
            if not image_path.exists():
                logger.error(f"Image file not found: {image_path}")
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            # Load model
            model = self.load_model(model_type)
            
            # Load and preprocess image
            try:
                image = Image.open(image_path).convert('RGB')
                image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            except Exception as e:
                logger.error(f"Error processing image: {str(e)}")
                raise ValueError(f"Error processing image: {str(e)}")
            
            # Make prediction
            with torch.no_grad():
                outputs = model(image_tensor)
                probabilities = torch.softmax(outputs, dim=1)
                predicted_class = torch.argmax(probabilities, dim=1).item()
                confidence = probabilities[0][predicted_class].item()
            
            # Format probabilities
            prob_dict = {
                self.class_names[i]: float(prob)
                for i, prob in enumerate(probabilities[0].cpu().numpy())
            }
            
            result = {
                'prediction': self.class_names[predicted_class],
                'confidence': confidence,
                'probabilities': prob_dict
            }
            
            logger.info(f"Prediction result: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error in prediction: {str(e)}")
            raise 