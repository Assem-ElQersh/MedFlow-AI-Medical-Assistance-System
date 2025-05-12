import os
import torch
import torch.nn as nn
from PIL import Image
import numpy as np
from typing import List, Dict, Any, Optional
import sys

# Add ml_models to Python path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ml_models'))

from disease_classifiers.pneumonia.training.pneumonia_classifier import get_model as get_pneumonia_model
from image_enhancement.training.sisr_model import SISRModel as SISRModel
from expert_system.rules_engine.inference import ExpertSystem

class DiseaseClassifier:
    def __init__(self, model_path: str, model_type: str = 'resnet50'):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = get_pneumonia_model(model_type, num_classes=2)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device)['model_state_dict'])
        self.model.eval()
        self.model = self.model.to(self.device)
        
        self.transform = torchvision.transforms.Compose([
            torchvision.transforms.Resize((224, 224)),
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def predict(self, image: Image.Image) -> Dict[str, Any]:
        """Predict disease from image"""
        image_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(image_tensor)
            probabilities = torch.softmax(outputs, dim=1)
            predicted_class = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_class].item()
        
        return {
            'class': 'PNEUMONIA' if predicted_class == 1 else 'NORMAL',
            'confidence': confidence,
            'probabilities': probabilities[0].cpu().numpy().tolist()
        }

class SISRModel:
    def __init__(self, model_path: str):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = SISRModel(scale_factor=4)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device)['model_state_dict'])
        self.model.eval()
        self.model = self.model.to(self.device)
        
        self.transform = torchvision.transforms.Compose([
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

    def enhance(self, image: Image.Image) -> Image.Image:
        """Enhance image resolution"""
        image_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            enhanced = self.model(image_tensor)
        
        # Convert back to PIL Image
        enhanced = enhanced.squeeze(0).cpu()
        enhanced = torchvision.transforms.ToPILImage()(enhanced)
        
        return enhanced

class ExpertSystem:
    def __init__(self):
        self.expert_system = ExpertSystem()

    def analyze(self, symptoms: List[Dict[str, Any]], vital_signs: Optional[Dict[str, Any]] = None,
               risk_factors: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze symptoms and return diagnosis"""
        return self.expert_system.analyze_symptoms(symptoms, vital_signs, risk_factors)

class AIService:
    def __init__(self):
        # Initialize models
        self.disease_classifier = DiseaseClassifier(
            model_path=os.path.join('ml_models', 'disease_classifiers', 'pneumonia', 'models', 'best_model.pth')
        )
        
        self.sisr_model = SISRModel(
            model_path=os.path.join('ml_models', 'image_enhancement', 'models', 'best_model.pth')
        )
        
        self.expert_system = ExpertSystem()

    async def process_medical_data(self, 
                                 image: Optional[Image.Image] = None,
                                 symptoms: Optional[List[Dict[str, Any]]] = None,
                                 vital_signs: Optional[Dict[str, Any]] = None,
                                 risk_factors: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process medical data and return comprehensive analysis"""
        results = {
            'image_analysis': None,
            'symptom_analysis': None,
            'emergency_flags': [],
            'recommendations': []
        }

        # Process image if provided
        if image is not None:
            # Enhance image
            enhanced_image = self.sisr_model.enhance(image)
            
            # Analyze for diseases
            disease_prediction = self.disease_classifier.predict(enhanced_image)
            
            results['image_analysis'] = {
                'enhanced_image': enhanced_image,
                'disease_prediction': disease_prediction
            }

        # Analyze symptoms if provided
        if symptoms is not None:
            analysis = self.expert_system.analyze(symptoms, vital_signs, risk_factors)
            
            results['symptom_analysis'] = analysis['diagnoses']
            results['emergency_flags'] = analysis['emergency_flags']
            
            # Get treatment recommendations for each diagnosis
            for diagnosis in analysis['diagnoses']:
                treatment = self.expert_system.get_treatment_recommendations(diagnosis['disease'])
                if treatment:
                    results['recommendations'].append({
                        'disease': diagnosis['disease'],
                        'treatment': treatment
                    })

        return results 