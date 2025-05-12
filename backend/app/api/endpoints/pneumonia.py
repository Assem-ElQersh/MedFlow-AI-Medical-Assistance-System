from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional
import os
import shutil
import logging
from pathlib import Path

from ...schemas.pneumonia import PneumoniaPrediction, PneumoniaDiagnosisRequest
from ...services.pneumonia_service import PneumoniaService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()
pneumonia_service = PneumoniaService()

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path(__file__).parent.parent.parent.parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
logger.info(f"Upload directory: {UPLOAD_DIR}")

@router.post("/diagnose", response_model=PneumoniaPrediction)
async def diagnose_pneumonia(
    file: Optional[UploadFile] = File(None),
    request: Optional[PneumoniaDiagnosisRequest] = None
):
    """
    Diagnose pneumonia from a chest X-ray image.
    
    Args:
        file: Uploaded chest X-ray image
        request: Optional request containing image_path and model_type
        
    Returns:
        PneumoniaPrediction: Prediction results including class and confidence
    """
    try:
        # Handle file upload
        if file:
            logger.info(f"Processing uploaded file: {file.filename}")
            # Save uploaded file
            file_path = UPLOAD_DIR / file.filename
            try:
                with file_path.open("wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                logger.info(f"File saved to: {file_path}")
            except Exception as e:
                logger.error(f"Error saving uploaded file: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Error saving uploaded file: {str(e)}"
                )
            
            try:
                # Make prediction
                result = pneumonia_service.predict(
                    str(file_path),
                    model_type=request.model_type if request else 'resnet50'
                )
                
                # Clean up uploaded file
                os.remove(file_path)
                logger.info(f"Temporary file removed: {file_path}")
                
                return result
                
            except Exception as e:
                # Clean up on error
                if file_path.exists():
                    os.remove(file_path)
                    logger.info(f"Temporary file removed after error: {file_path}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Error processing image: {str(e)}"
                )
            
        # Handle existing file path
        elif request and request.image_path:
            logger.info(f"Processing file path: {request.image_path}")
            try:
                return pneumonia_service.predict(
                    request.image_path,
                    model_type=request.model_type
                )
            except FileNotFoundError as e:
                logger.error(f"File not found: {str(e)}")
                raise HTTPException(
                    status_code=404,
                    detail=str(e)
                )
            except ValueError as e:
                logger.error(f"Invalid image: {str(e)}")
                raise HTTPException(
                    status_code=400,
                    detail=str(e)
                )
            except Exception as e:
                logger.error(f"Error processing image: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Error processing image: {str(e)}"
                )
            
        else:
            logger.error("No file or image path provided")
            raise HTTPException(
                status_code=400,
                detail="Either file upload or image_path must be provided"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        ) 