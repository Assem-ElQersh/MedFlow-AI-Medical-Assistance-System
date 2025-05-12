from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class SymptomInput(BaseModel):
    name: str
    severity: int = Field(..., ge=1, le=10)
    duration: str
    description: Optional[str] = None

class VitalSigns(BaseModel):
    blood_pressure: str  # Format: "120/80"
    heart_rate: int
    temperature: float
    respiratory_rate: int
    oxygen_saturation: float

class DiagnosisRequest(BaseModel):
    symptoms: List[SymptomInput]
    vital_signs: VitalSigns
    medical_history: Optional[Dict[str, Any]] = None

class DiagnosisResult(BaseModel):
    disease: str
    confidence_score: float
    alternative_diagnoses: List[Dict[str, float]]
    recommendations: List[str]
    is_emergency: bool = False

class DiagnosisResponse(BaseModel):
    diagnosis: DiagnosisResult
    medical_record_id: int
    created_at: datetime

    class Config:
        orm_mode = True 