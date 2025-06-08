# app/api/endpoints/enhanced_diagnosis.py - Drop-in replacement for diagnosis.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from PIL import Image
import io
import logging

from app.api import deps
from app.services.enhanced_ai_service import EnhancedAIService  # NEW: MedGemma service
from app.schemas.diagnosis import (
    DiagnosisRequest,
    DiagnosisResponse,
    SymptomInput,
    VitalSigns,
    EnhancedDiagnosisResponse  # NEW: Enhanced response schema
)
from app.models.medical_record import MedicalRecord, EnhancedMedicalRecord  # NEW: Enhanced model
from app.models.user import User

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize enhanced AI service with MedGemma
ai_service = EnhancedAIService()

@router.post("/analyze-enhanced", response_model=EnhancedDiagnosisResponse)
async def analyze_medical_data_enhanced(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    symptoms: List[SymptomInput],
    vital_signs: VitalSigns,
    medical_image: Optional[UploadFile] = File(None),
    patient_history: Optional[dict] = None
):
    """
    ENHANCED: Analyze medical data using MedGemma + your existing models
    Maintains backward compatibility with your existing API
    """
    try:
        # Convert symptoms to your existing format
        symptoms_dict = [
            {
                'name': symptom.name,
                'severity': symptom.severity,
                'duration': symptom.duration,
                'description': symptom.description
            }
            for symptom in symptoms
        ]
        
        # Convert vital signs to your existing format
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
        
        # ENHANCED: Get comprehensive analysis from MedGemma + legacy models
        analysis = await ai_service.process_medical_data(
            image=image,
            symptoms=symptoms_dict,
            vital_signs=vital_signs_dict,
            risk_factors={'age': current_user.age, **(patient_history or {})}
        )
        
        # Create enhanced medical record with MedGemma results
        medical_record = EnhancedMedicalRecord(
            user_id=current_user.id,
            symptoms=symptoms_dict,
            vital_signs=vital_signs_dict,
            
            # Original fields (backward compatibility)
            diagnosis=analysis.get('symptom_analysis', {}).get('final_diagnosis'),
            confidence_score=analysis.get('symptom_analysis', {}).get('confidence_score'),
            recommendations=analysis.get('recommendations', []),
            
            # NEW: Enhanced fields with MedGemma analysis
            medgemma_analysis=analysis.get('image_analysis', {}),
            legacy_model_comparison=analysis.get('legacy_comparison', {}),
            consensus_analysis=analysis.get('symptom_analysis', {}),
            confidence_metrics=analysis.get('confidence_metrics', {}),
            emergency_flags=analysis.get('emergency_flags', [])
        )
        
        db.add(medical_record)
        db.commit()
        db.refresh(medical_record)
        
        # Enhanced response with MedGemma insights
        response = EnhancedDiagnosisResponse(
            medical_record_id=medical_record.id,
            
            # Original response fields (backward compatibility)
            diagnosis=analysis.get('symptom_analysis', {}),
            image_analysis=analysis.get('image_analysis', {}),
            emergency_flags=analysis.get('emergency_flags', []),
            recommendations=analysis.get('recommendations', []),
            
            # NEW: Enhanced fields
            medgemma_insights=analysis.get('image_analysis', {}),
            model_consensus=analysis.get('confidence_metrics', {}),
            clinical_reasoning=analysis.get('symptom_analysis', {}),
            follow_up_plan=analysis.get('recommendations', []),
            
            created_at=medical_record.created_at
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Enhanced analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# EDIT POINT 7: Keep your existing pneumonia endpoint but enhance it
@router.post("/pneumonia/enhanced", response_model=dict)
async def enhanced_pneumonia_analysis(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    file: UploadFile = File(...),
    symptoms: Optional[str] = None
):
    """
    Enhanced pneumonia analysis comparing MedGemma vs your existing model
    """
    try:
        # Load image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Get both MedGemma and legacy analysis
        analysis = await ai_service.medgemma_service.comprehensive_medical_analysis(
            image=image,
            symptoms=[{'name': symptoms, 'severity': 'moderate'}] if symptoms else None
        )
        
        return {
            'medgemma_analysis': analysis.get('medgemma_analysis', {}),
            'legacy_model': analysis.get('legacy_comparison', {}),
            'consensus': analysis.get('combined_diagnosis', {}),
            'confidence_comparison': {
                'medgemma_confidence': analysis.get('medgemma_analysis', {}).get('confidence', 0),
                'legacy_confidence': analysis.get('legacy_comparison', {}).get('confidence', 0),
                'consensus_level': analysis.get('combined_diagnosis', {}).get('consensus_level', 'unknown')
            }
        }
        
    except Exception as e:
        logger.error(f"Enhanced pneumonia analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# EDIT POINT 8: Add specialized endpoints for different imaging types
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
    Leverages MedGemma's multimodal capabilities for specific imaging types
    """
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Customize analysis based on imaging type
        imaging_prompts = {
            'chest_xray': "Analyze this chest X-ray for pneumonia, pneumothorax, pleural effusion, and cardiac abnormalities.",
            'ct_scan': "Analyze this CT scan for anatomical abnormalities, lesions, and pathological findings.",
            'mri': "Analyze this MRI scan for tissue abnormalities, lesions, and structural changes.",
            'mammography': "Analyze this mammogram for masses, calcifications, and suspicious findings.",
            'dermatology': "Analyze this skin lesion for malignancy risk using ABCDE criteria."
        }
        
        specialized_prompt = imaging_prompts.get(imaging_type, "Perform general medical image analysis.")
        
        # Get MedGemma analysis with specialized context
        analysis = await ai_service.medgemma_service._medgemma_image_analysis(
            image=image,
            symptoms=[{'name': clinical_context}] if clinical_context else None
        )
        
        return {
            'imaging_type': imaging_type,
            'analysis': analysis,
            'specialized_findings': analysis.get('findings', {}),
            'recommendations': analysis.get('recommendations', [])
        }
        
    except Exception as e:
        logger.error(f"Radiology analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))