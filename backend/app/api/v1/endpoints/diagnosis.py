from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from PIL import Image
import io

from app.api import deps
from app.services.ai_service import AIService
from app.schemas.diagnosis import (
    DiagnosisRequest,
    DiagnosisResponse,
    SymptomInput,
    VitalSigns
)
from app.models.medical_record import MedicalRecord
from app.models.user import User

router = APIRouter()
ai_service = AIService()

@router.post("/analyze", response_model=DiagnosisResponse)
async def analyze_medical_data(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    symptoms: List[SymptomInput],
    vital_signs: VitalSigns,
    medical_image: Optional[UploadFile] = File(None)
):
    """
    Analyze medical data including symptoms, vital signs, and optional medical image.
    Returns diagnosis with confidence scores and recommendations.
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
        
        # Convert vital signs to dictionary
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
        
        # Get analysis from AI service
        analysis = await ai_service.process_medical_data(
            image=image,
            symptoms=symptoms_dict,
            vital_signs=vital_signs_dict,
            risk_factors={'age': current_user.age}  # Add more risk factors as needed
        )
        
        # Create medical record
        medical_record = MedicalRecord(
            user_id=current_user.id,
            symptoms=symptoms_dict,
            vital_signs=vital_signs_dict,
            diagnosis=analysis['symptom_analysis'][0]['disease'] if analysis['symptom_analysis'] else None,
            confidence_score=analysis['symptom_analysis'][0]['confidence'] if analysis['symptom_analysis'] else None,
            recommendations=analysis['recommendations']
        )
        db.add(medical_record)
        db.commit()
        db.refresh(medical_record)
        
        # Prepare response
        response = DiagnosisResponse(
            medical_record_id=medical_record.id,
            diagnosis=analysis['symptom_analysis'][0] if analysis['symptom_analysis'] else None,
            image_analysis=analysis['image_analysis'],
            emergency_flags=analysis['emergency_flags'],
            recommendations=analysis['recommendations'],
            created_at=medical_record.created_at
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[DiagnosisResponse])
async def get_diagnosis_history(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 10
):
    """
    Get user's diagnosis history with pagination.
    """
    records = db.query(MedicalRecord)\
        .filter(MedicalRecord.user_id == current_user.id)\
        .order_by(MedicalRecord.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return [
        DiagnosisResponse(
            medical_record_id=record.id,
            diagnosis={
                'disease': record.diagnosis,
                'confidence': record.confidence_score
            },
            recommendations=record.recommendations,
            created_at=record.created_at
        )
        for record in records
    ] 