from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class SymptomInput(BaseModel):
    name: str
    severity: str = Field(..., description="Severity level: mild, moderate, severe")
    duration: str = Field(..., description="Duration of symptoms")
    description: Optional[str] = None

class VitalSigns(BaseModel):
    blood_pressure: str = Field(..., description="Format: '120/80'")
    heart_rate: int = Field(..., ge=0, le=250)
    temperature: float = Field(..., ge=35.0, le=42.0)
    respiratory_rate: int = Field(..., ge=0, le=60)
    oxygen_saturation: float = Field(..., ge=0.0, le=100.0)

class DiagnosisRequest(BaseModel):
    symptoms: List[SymptomInput]
    vital_signs: VitalSigns
    patient_history: Optional[Dict] = None

class DiagnosisResult(BaseModel):
    disease: str
    confidence_score: float
    alternative_diagnoses: List[Dict[str, float]]
    recommendations: List[str]
    is_emergency: bool = False

class DiagnosisResponse(BaseModel):
    medical_record_id: int
    diagnosis: Dict
    image_analysis: Optional[Dict] = None
    emergency_flags: List[str]
    recommendations: List[Dict]
    created_at: datetime

class EnhancedDiagnosisResponse(DiagnosisResponse):
    """Enhanced response model with additional MedGemma analysis fields"""
    medgemma_insights: Optional[Dict] = None
    model_consensus: Optional[Dict] = None
    clinical_reasoning: Optional[Dict] = None
    follow_up_plan: Optional[List[Dict]] = None

class RadiologyAnalysisRequest(BaseModel):
    imaging_type: str = Field(..., description="Type of imaging: chest_xray, ct_scan, mri, etc.")
    clinical_context: Optional[str] = None

class RadiologyAnalysisResponse(BaseModel):
    imaging_type: str
    analysis: Dict
    findings: List[Dict]
    recommendations: List[Dict]
    confidence_score: float
    created_at: datetime

    class Config:
        orm_mode = True 