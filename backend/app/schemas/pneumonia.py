from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile

class PneumoniaPrediction(BaseModel):
    """Schema for pneumonia prediction response"""
    prediction: str  # 'NORMAL' or 'PNEUMONIA'
    confidence: float
    probabilities: dict[str, float]  # {'NORMAL': 0.2, 'PNEUMONIA': 0.8}

class PneumoniaDiagnosisRequest(BaseModel):
    """Schema for pneumonia diagnosis request"""
    image_path: Optional[str] = None  # Path to image if already on server
    model_type: str = 'resnet50'  # Default to ResNet50, can be 'densenet121' or 'efficientnet_b0' 