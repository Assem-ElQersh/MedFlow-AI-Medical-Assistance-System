from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from PIL import Image
import io
import logging

from app.api import deps
from app.services.medgemma_service import MedGemmaService
from app.schemas.diagnosis import (
    DiagnosisRequest,
    DiagnosisResponse,
    SymptomInput,
    VitalSigns,
    EnhancedDiagnosisResponse
)
from app.models.medical_record import EnhancedMedicalRecord
from app.models.user import User

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize MedGemma service
medgemma_service = MedGemmaService()

@router.post("/analyze", response_model=EnhancedDiagnosisResponse)
async def analyze_medical_data(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    symptoms: List[SymptomInput],
    vital_signs: VitalSigns,
    medical_image: Optional[UploadFile] = File(None),
    patient_history: Optional[dict] = None
):
    """
    Analyze medical data using MedGemma AI
    """
    try:
        # Convert symptoms to dictionary format
        symptoms_dict = [
            {
                'name': symptom.name,
                'severity': symptom.severity,
                'duration': symptom.duration,
                'description': symptom.description
            }
            for symptom in symptoms
        ]
        
        # Convert vital signs to dictionary format
        vital_signs_dict = {
            'blood_pressure': vital_signs.blood_pressure,
            'heart_rate': vital_signs.heart_rate,
            'temperature': vital_signs.temperature,
            'respiratory_rate': vital_signs.respiratory_rate,
            'oxygen_saturation': vital_signs.oxygen_saturation
        }
        
        # Process medical image if provided
        image = None
        if medical_image:
            contents = await medical_image.read()
            image = Image.open(io.BytesIO(contents))
        
        # Get comprehensive analysis from MedGemma
        analysis = await medgemma_service.comprehensive_medical_analysis(
            image=image,
            text=" ".join([s['description'] for s in symptoms_dict]),
            vital_signs=vital_signs_dict,
            patient_history=patient_history
        )
        
        # Create enhanced medical record
        medical_record = EnhancedMedicalRecord(
            user_id=current_user.id,
            symptoms=symptoms_dict,
            vital_signs=vital_signs_dict,
            medical_images=[medical_image.filename] if medical_image else [],
            patient_history=patient_history,
            
            # MedGemma Analysis Results
            medgemma_analysis=analysis,
            image_analysis=analysis.get('image_analysis', {}),
            text_analysis=analysis.get('text_analysis', {}),
            consensus_analysis=analysis.get('consensus_analysis', {}),
            
            # Diagnosis and Treatment
            primary_diagnosis=analysis.get('text_analysis', {}).get('primary_diagnosis'),
            differential_diagnoses=analysis.get('text_analysis', {}).get('differential_diagnoses', []),
            confidence_score=analysis.get('text_analysis', {}).get('confidence', 0.0),
            treatment_plan=analysis.get('recommendations', []),
            
            # Emergency and Follow-up
            is_emergency=len(analysis.get('emergency_flags', [])) > 0,
            emergency_flags=analysis.get('emergency_flags', []),
            urgency_level=analysis.get('risk_assessment', {}).get('urgency_level', 1),
            follow_up_plan=analysis.get('recommendations', [])
        )
        
        db.add(medical_record)
        db.commit()
        db.refresh(medical_record)
        
        # Prepare response
        response = EnhancedDiagnosisResponse(
            medical_record_id=medical_record.id,
            diagnosis=analysis.get('text_analysis', {}),
            image_analysis=analysis.get('image_analysis', {}),
            emergency_flags=analysis.get('emergency_flags', []),
            recommendations=analysis.get('recommendations', []),
            created_at=medical_record.created_at
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/analyze-radiology", response_model=dict)
async def analyze_radiology_image(
    *,
    imaging_type: str,  # 'chest_xray', 'ct_scan', 'mri', etc.
    file: UploadFile = File(...),
    clinical_context: Optional[str] = None,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Specialized radiology analysis for different imaging modalities
    """
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Get MedGemma analysis
        analysis = await medgemma_service.analyze_medical_image(
            image=image,
            context={
                'imaging_type': imaging_type,
                'clinical_context': clinical_context
            }
        )
        
        return {
            'imaging_type': imaging_type,
            'analysis': analysis,
            'findings': analysis.get('findings', []),
            'recommendations': analysis.get('recommendations', [])
        }
        
    except Exception as e:
        logger.error(f"Radiology analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 