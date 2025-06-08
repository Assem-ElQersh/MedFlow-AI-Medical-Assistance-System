# app/services/enhanced_ai_service.py - Completely rebuilt with MedGemma
import os
import torch
import torch.nn as nn
from PIL import Image
import numpy as np
from typing import List, Dict, Any, Optional
import sys
from transformers import AutoTokenizer, AutoModelForCausalLM
import json
import logging

# Import your existing models for comparison
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ml_models'))
from disease_classifiers.pneumonia.training.pneumonia_classifier import get_model as get_pneumonia_model
from expert_system.rules_engine.inference import ExpertSystem

logger = logging.getLogger(__name__)

class MedGemmaService:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load MedGemma models
        logger.info("Loading MedGemma models...")
        self.multimodal_model = AutoModelForCausalLM.from_pretrained(
            "google/medgemma-4b-it",
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.text_model = AutoModelForCausalLM.from_pretrained(
            "google/medgemma-27b-text-it",
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained("google/medgemma-4b-it")
        
        # Keep your existing models for validation/comparison
        self.legacy_pneumonia_model = None
        self.expert_system = ExpertSystem()
        
        # EDIT POINT 1: Add more disease classifiers from your existing work
        self.disease_models = {
            'pneumonia': self._load_legacy_pneumonia_model(),
            # Add tuberculosis, COVID-19, brain tumor models here
        }
        
    def _load_legacy_pneumonia_model(self):
        """Load your existing pneumonia model for comparison"""
        try:
            model_path = os.path.join('ml_models/disease_classifiers/pneumonia/models/best_model.pth')
            if os.path.exists(model_path):
                model = get_pneumonia_model('resnet50', num_classes=2)
                checkpoint = torch.load(model_path, map_location=self.device)
                model.load_state_dict(checkpoint['model_state_dict'])
                model.eval()
                return model.to(self.device)
        except Exception as e:
            logger.warning(f"Could not load legacy pneumonia model: {e}")
        return None

    async def comprehensive_medical_analysis(self, 
                                           image: Optional[Image.Image] = None,
                                           symptoms: Optional[List[Dict[str, Any]]] = None,
                                           vital_signs: Optional[Dict[str, Any]] = None,
                                           patient_history: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Enhanced analysis combining MedGemma with your existing expert system"""
        
        results = {
            'medgemma_analysis': {},
            'legacy_comparison': {},
            'expert_system_analysis': {},
            'combined_diagnosis': {},
            'emergency_flags': [],
            'recommendations': []
        }
        
        # 1. MedGemma Multimodal Analysis (if image provided)
        if image is not None:
            results['medgemma_analysis'] = await self._medgemma_image_analysis(
                image, symptoms, vital_signs, patient_history
            )
        
        # 2. MedGemma Text-based Clinical Reasoning
        if symptoms or vital_signs:
            results['medgemma_analysis']['clinical_reasoning'] = await self._medgemma_clinical_reasoning(
                symptoms, vital_signs, patient_history
            )
        
        # 3. Legacy Model Comparison (your existing pneumonia model)
        if image is not None and self.legacy_pneumonia_model:
            results['legacy_comparison'] = self._legacy_model_analysis(image)
        
        # 4. Expert System Analysis (your existing rule-based system)
        if symptoms:
            expert_analysis = self.expert_system.analyze_symptoms(
                symptoms, vital_signs, patient_history
            )
            results['expert_system_analysis'] = expert_analysis
            results['emergency_flags'].extend(expert_analysis.get('emergency_flags', []))
        
        # 5. Combined Analysis
        results['combined_diagnosis'] = self._combine_analyses(results)
        
        return results
    
    async def _medgemma_image_analysis(self, image: Image.Image, symptoms=None, vital_signs=None, history=None) -> Dict:
        """EDIT POINT 2: Customize for different imaging modalities"""
        symptom_context = ""
        if symptoms:
            symptom_context = f"Patient reports: {', '.join([s.get('name', '') for s in symptoms])}"
        
        vital_context = ""
        if vital_signs:
            vital_context = f"Vital signs: BP {vital_signs.get('blood_pressure', 'N/A')}, HR {vital_signs.get('heart_rate', 'N/A')}, Temp {vital_signs.get('temperature', 'N/A')}°C"
        
        prompt = f"""
        <image>
        Medical Image Analysis Request:
        
        Clinical Context:
        {symptom_context}
        {vital_context}
        
        Please analyze this medical image and provide:
        1. Detailed imaging findings
        2. Most likely diagnosis with confidence percentage
        3. Differential diagnoses (top 3 alternatives)
        4. Urgency level (1-5 scale, 5 being emergency)
        5. Recommended follow-up imaging or tests
        6. Clinical correlation with reported symptoms
        
        Respond in JSON format with fields: findings, primary_diagnosis, differential_diagnoses, urgency_level, recommendations, clinical_correlation
        """
        
        inputs = self.tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = self.multimodal_model.generate(
                **inputs,
                max_length=2048,
                temperature=0.2,  # Conservative for medical accuracy
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return self._parse_medical_response(response)
    
    async def _medgemma_clinical_reasoning(self, symptoms=None, vital_signs=None, history=None) -> Dict:
        """EDIT POINT 3: Customize clinical reasoning prompts for your hospital protocols"""
        
        # Format clinical data
        clinical_summary = self._format_clinical_data(symptoms, vital_signs, history)
        
        prompt = f"""
        Clinical Case Analysis:
        
        {clinical_summary}
        
        As an experienced physician, please provide:
        1. Systematic review of symptoms and vital signs
        2. Most likely primary diagnosis with confidence level
        3. Complete differential diagnosis list (rank by probability)
        4. Risk stratification (low/moderate/high risk)
        5. Immediate management plan
        6. Diagnostic workup recommendations
        7. Follow-up timeline
        8. Warning signs that would require emergency care
        
        Use evidence-based medicine principles and current clinical guidelines.
        Respond in structured JSON format.
        """
        
        inputs = self.tokenizer(prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = self.text_model.generate(
                **inputs,
                max_length=3072,
                temperature=0.2,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return self._parse_clinical_response(response)
    
    def _legacy_model_analysis(self, image: Image.Image) -> Dict:
        """Compare with your existing pneumonia model"""
        if self.legacy_pneumonia_model is None:
            return {'error': 'Legacy model not available'}
        
        try:
            # Use your existing prediction logic
            from ml_models.disease_classifiers.pneumonia.training.pneumonia_classifier import CONFIG
            import torchvision.transforms as transforms
            
            transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
            ])
            
            image_tensor = transform(image).unsqueeze(0).to(self.device)
            
            with torch.no_grad():
                outputs = self.legacy_pneumonia_model(image_tensor)
                probabilities = torch.softmax(outputs, dim=1)
                predicted_class = torch.argmax(probabilities, dim=1).item()
                confidence = probabilities[0][predicted_class].item()
            
            class_names = ['NORMAL', 'PNEUMONIA']
            
            return {
                'prediction': class_names[predicted_class],
                'confidence': confidence,
                'probabilities': {
                    class_names[i]: float(prob)
                    for i, prob in enumerate(probabilities[0].cpu().numpy())
                }
            }
        except Exception as e:
            logger.error(f"Legacy model analysis failed: {e}")
            return {'error': str(e)}
    
    def _combine_analyses(self, results: Dict) -> Dict:
        """EDIT POINT 4: Customize how different AI systems are combined"""
        combined = {
            'final_diagnosis': '',
            'confidence_score': 0.0,
            'consensus_level': '',
            'recommendations': [],
            'follow_up': []
        }
        
        # Extract diagnoses from different sources
        medgemma_diagnosis = results.get('medgemma_analysis', {}).get('primary_diagnosis', {})
        legacy_diagnosis = results.get('legacy_comparison', {})
        expert_diagnosis = results.get('expert_system_analysis', {}).get('diagnoses', [])
        
        # EDIT POINT 5: Implement your consensus algorithm
        if medgemma_diagnosis and legacy_diagnosis:
            # If both agree, high confidence
            if (medgemma_diagnosis.get('disease', '').lower() == 
                legacy_diagnosis.get('prediction', '').lower()):
                combined['final_diagnosis'] = medgemma_diagnosis.get('disease', '')
                combined['confidence_score'] = min(0.95, 
                    (medgemma_diagnosis.get('confidence', 0) + legacy_diagnosis.get('confidence', 0)) / 2)
                combined['consensus_level'] = 'high'
            else:
                # If they disagree, recommend further evaluation
                combined['final_diagnosis'] = 'Requires further evaluation'
                combined['confidence_score'] = 0.6
                combined['consensus_level'] = 'low'
                combined['recommendations'].append('Conflicting AI analyses - recommend specialist consultation')
        
        return combined
    
    def _format_clinical_data(self, symptoms, vital_signs, history) -> str:
        """Format clinical data for MedGemma input"""
        sections = []
        
        if symptoms:
            symptom_list = []
            for symptom in symptoms:
                name = symptom.get('name', '')
                severity = symptom.get('severity', 'moderate')
                duration = symptom.get('duration', 'unknown')
                symptom_list.append(f"{name} ({severity} severity, {duration} duration)")
            sections.append(f"Chief Complaint: {', '.join(symptom_list)}")
        
        if vital_signs:
            vital_items = []
            for key, value in vital_signs.items():
                vital_items.append(f"{key}: {value}")
            sections.append(f"Vital Signs: {', '.join(vital_items)}")
        
        if history:
            sections.append(f"Medical History: {history}")
        
        return '\n'.join(sections)
    
    def _parse_medical_response(self, response: str) -> Dict:
        """Parse MedGemma medical response"""
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback parsing
                return {'raw_response': response, 'parsed': False}
        except Exception as e:
            return {'raw_response': response, 'parsing_error': str(e)}
    
    def _parse_clinical_response(self, response: str) -> Dict:
        """Parse MedGemma clinical reasoning response"""
        return self._parse_medical_response(response)

# EDIT POINT 6: Enhanced API endpoints that use your existing structure
class EnhancedAIService:
    """Enhanced service that integrates with your existing FastAPI structure"""
    
    def __init__(self):
        self.medgemma_service = MedGemmaService()
    
    async def process_medical_data(self, 
                                 image: Optional[Image.Image] = None,
                                 symptoms: Optional[List[Dict[str, Any]]] = None,
                                 vital_signs: Optional[Dict[str, Any]] = None,
                                 risk_factors: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Drop-in replacement for your existing AI service"""
        
        # Use enhanced MedGemma analysis
        analysis = await self.medgemma_service.comprehensive_medical_analysis(
            image=image,
            symptoms=symptoms,
            vital_signs=vital_signs,
            patient_history=risk_factors
        )
        
        # Format response to match your existing API structure
        return {
            'image_analysis': analysis.get('medgemma_analysis', {}),
            'symptom_analysis': analysis.get('combined_diagnosis', {}),
            'emergency_flags': analysis.get('emergency_flags', []),
            'recommendations': analysis.get('recommendations', []),
            'legacy_comparison': analysis.get('legacy_comparison', {}),
            'confidence_metrics': {
                'medgemma_confidence': analysis.get('medgemma_analysis', {}).get('confidence', 0),
                'consensus_level': analysis.get('combined_diagnosis', {}).get('consensus_level', 'unknown')
            }
        }