from typing import Dict, List, Optional, Union
import numpy as np
from loguru import logger
from app.core.config import settings
from app.services.ai.medgemma_service import MedGemmaService

class ImageAnalysisService:
    """Service for medical image analysis"""
    
    def __init__(self):
        self.medgemma = MedGemmaService()
        self.supported_modalities = [
            "xray",
            "ct",
            "mri",
            "ultrasound"
        ]
    
    async def analyze_image(
        self,
        image_data: Union[str, bytes],
        modality: str,
        patient_data: Optional[Dict] = None
    ) -> Dict:
        """
        Analyze medical image using MedGemma
        """
        try:
            # Validate modality
            if modality.lower() not in self.supported_modalities:
                raise ValueError(f"Unsupported modality: {modality}")
            
            # Preprocess image
            processed_image = await self._preprocess_image(image_data, modality)
            
            # Get MedGemma analysis
            analysis = await self.medgemma.analyze_image(
                processed_image,
                modality,
                patient_data
            )
            
            # Post-process results
            results = self._post_process_analysis(analysis, modality)
            
            return results
            
        except Exception as e:
            logger.error(f"Image analysis failed: {str(e)}")
            raise
    
    async def _preprocess_image(
        self,
        image_data: Union[str, bytes],
        modality: str
    ) -> np.ndarray:
        """Preprocess image for analysis"""
        try:
            # Convert image to numpy array
            if isinstance(image_data, str):
                # Handle file path
                import cv2
                image = cv2.imread(image_data)
            else:
                # Handle bytes
                import cv2
                nparr = np.frombuffer(image_data, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Apply modality-specific preprocessing
            if modality.lower() == "xray":
                image = self._preprocess_xray(image)
            elif modality.lower() == "ct":
                image = self._preprocess_ct(image)
            elif modality.lower() == "mri":
                image = self._preprocess_mri(image)
            elif modality.lower() == "ultrasound":
                image = self._preprocess_ultrasound(image)
            
            return image
            
        except Exception as e:
            logger.error(f"Image preprocessing failed: {str(e)}")
            raise
    
    def _preprocess_xray(self, image: np.ndarray) -> np.ndarray:
        """Preprocess X-ray image"""
        # Convert to grayscale
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Normalize
        image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
        
        # Apply CLAHE for better contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        image = clahe.apply(image)
        
        return image
    
    def _preprocess_ct(self, image: np.ndarray) -> np.ndarray:
        """Preprocess CT image"""
        # Convert to grayscale
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Normalize to Hounsfield units
        image = (image - image.min()) / (image.max() - image.min()) * 4000 - 1000
        
        # Clip to typical HU range
        image = np.clip(image, -1000, 3000)
        
        return image
    
    def _preprocess_mri(self, image: np.ndarray) -> np.ndarray:
        """Preprocess MRI image"""
        # Convert to grayscale
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Normalize
        image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
        
        # Apply Gaussian blur to reduce noise
        image = cv2.GaussianBlur(image, (5, 5), 0)
        
        return image
    
    def _preprocess_ultrasound(self, image: np.ndarray) -> np.ndarray:
        """Preprocess ultrasound image"""
        # Convert to grayscale
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Normalize
        image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
        
        # Apply bilateral filter to reduce noise while preserving edges
        image = cv2.bilateralFilter(image, 9, 75, 75)
        
        return image
    
    def _post_process_analysis(
        self,
        analysis: Dict,
        modality: str
    ) -> Dict:
        """Post-process analysis results"""
        results = {
            "findings": [],
            "confidence_scores": {},
            "recommendations": [],
            "modality": modality
        }
        
        # Process findings
        if "findings" in analysis:
            for finding in analysis["findings"]:
                results["findings"].append({
                    "description": finding["description"],
                    "location": finding.get("location", "unknown"),
                    "severity": finding.get("severity", "unknown")
                })
        
        # Process confidence scores
        if "confidence_scores" in analysis:
            results["confidence_scores"] = analysis["confidence_scores"]
        
        # Generate recommendations
        results["recommendations"] = self._generate_recommendations(
            results["findings"],
            modality
        )
        
        return results
    
    def _generate_recommendations(
        self,
        findings: List[Dict],
        modality: str
    ) -> List[str]:
        """Generate recommendations based on findings"""
        recommendations = []
        
        # Add modality-specific recommendations
        if modality.lower() == "xray":
            if any(f["severity"] == "high" for f in findings):
                recommendations.append("Immediate follow-up with radiologist recommended")
            if any("fracture" in f["description"].lower() for f in findings):
                recommendations.append("Orthopedic consultation recommended")
        
        elif modality.lower() == "ct":
            if any(f["severity"] == "high" for f in findings):
                recommendations.append("Urgent specialist consultation recommended")
            if any("mass" in f["description"].lower() for f in findings):
                recommendations.append("Oncology consultation recommended")
        
        elif modality.lower() == "mri":
            if any(f["severity"] == "high" for f in findings):
                recommendations.append("Neurology consultation recommended")
            if any("tumor" in f["description"].lower() for f in findings):
                recommendations.append("Neurosurgery consultation recommended")
        
        elif modality.lower() == "ultrasound":
            if any(f["severity"] == "high" for f in findings):
                recommendations.append("Obstetrics/Gynecology consultation recommended")
            if any("mass" in f["description"].lower() for f in findings):
                recommendations.append("Surgical consultation recommended")
        
        return recommendations 