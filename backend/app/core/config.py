# app/core/enhanced_config.py - Enhanced version of your config.py
from typing import Any, Dict, List, Union

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
from pydantic import validator


class EnhancedSettings(BaseSettings):
    # Keep all your existing settings
    PROJECT_NAME: str = "MedFlow AI - Enhanced with MedGemma"
    API_V1_STR: str = "/api/v1"
    
    # CORS Configuration (keep existing)
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Database Configuration (keep existing)
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "medflow_enhanced"  # NEW: Use enhanced database
    SQLALCHEMY_DATABASE_URI: str = None
    
    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: str, values: dict) -> str:
        if isinstance(v, str):
            return v
        return f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}/{values.get('POSTGRES_DB')}"
    
    # JWT Configuration (keep existing)
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ENHANCED: MedGemma Model Configuration
    MEDGEMMA_MULTIMODAL_MODEL: str = "google/medgemma-4b-it"
    MEDGEMMA_TEXT_MODEL: str = "google/medgemma-27b-text-it"
    MEDGEMMA_CACHE_DIR: str = "./model_cache"
    
    # Model parameters - EDIT POINT 11: Tune these for your use case
    MEDGEMMA_TEMPERATURE: float = 0.2          # Conservative for medical accuracy
    MEDGEMMA_MAX_LENGTH: int = 2048            # Maximum response length
    MEDGEMMA_TOP_P: float = 0.9                # Nucleus sampling parameter
    
    # Legacy model paths (keep your existing paths)
    SISR_MODEL_PATH: str = "ml_models/image_enhancement/sisr_model.pth"
    DISEASE_CLASSIFIER_PATH: str = "ml_models/disease_classifiers/"
    EXPERT_SYSTEM_PATH: str = "ml_models/expert_system/"
    
    # NEW: Model comparison settings
    ENABLE_MODEL_COMPARISON: bool = True       # Compare MedGemma vs legacy models
    CONSENSUS_THRESHOLD: float = 0.8           # Threshold for model agreement
    LEGACY_MODEL_WEIGHT: float = 0.3           # Weight for legacy models in consensus
    MEDGEMMA_MODEL_WEIGHT: float = 0.7         # Weight for MedGemma in consensus
    
    # NEW: Emergency detection settings - EDIT POINT 12
    EMERGENCY_CONFIDENCE_THRESHOLD: float = 0.8
    EMERGENCY_KEYWORDS: List[str] = [
        "severe chest pain", "difficulty breathing", "unconscious",
        "severe bleeding", "stroke symptoms", "heart attack"
    ]
    EMERGENCY_VITAL_SIGNS_THRESHOLDS: Dict[str, Dict[str, float]] = {
        "heart_rate": {"min": 50, "max": 120},
        "blood_pressure_systolic": {"min": 90, "max": 180},
        "temperature": {"min": 35.0, "max": 39.5},
        "oxygen_saturation": {"min": 90, "max": 100}
    }
    
    # NEW: Specialty-specific configurations - EDIT POINT 13
    SPECIALTY_CONFIGS: Dict[str, Dict[str, Any]] = {
        "cardiology": {
            "emergency_keywords": ["chest pain", "palpitations", "syncope"],
            "required_tests": ["ECG", "troponin", "echo"],
            "specialist_required_threshold": 0.7
        },
        "pulmonology": {
            "emergency_keywords": ["shortness of breath", "hemoptysis"],
            "required_tests": ["chest_xray", "ABG", "spirometry"],
            "specialist_required_threshold": 0.7
        },
        "dermatology": {
            "emergency_keywords": ["rapid growth", "bleeding lesion"],
            "required_tests": ["dermoscopy", "biopsy"],
            "specialist_required_threshold": 0.6
        }
    }
    
    # NEW: Performance monitoring - EDIT POINT 14
    ENABLE_PERFORMANCE_MONITORING: bool = True
    LOG_MODEL_RESPONSES: bool = True           # Log all model responses for analysis
    TRACK_PROCESSING_TIME: bool = True         # Track processing times
    ENABLE_A_B_TESTING: bool = False           # A/B test different model configs
    
    # NEW: Integration settings
    ENABLE_DICOM_SUPPORT: bool = True          # Support DICOM medical images
    ENABLE_HL7_INTEGRATION: bool = False       # HL7 FHIR integration
    ENABLE_EHR_INTEGRATION: bool = False       # Electronic Health Record integration
    
    # NEW: Security and compliance - EDIT POINT 15
    HIPAA_COMPLIANCE_MODE: bool = True         # Enable HIPAA compliance features
    AUDIT_LOG_ENABLED: bool = True             # Enable audit logging
    DATA_RETENTION_DAYS: int = 2555            # 7 years for medical records
    ENCRYPTION_AT_REST: bool = True            # Encrypt sensitive data
    
    # NEW: API rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60            # API calls per minute per user
    ANALYSIS_RATE_LIMIT: int = 10              # AI analyses per minute per user
    
    # NEW: Model resource management
    GPU_MEMORY_FRACTION: float = 0.8           # Fraction of GPU memory to use
    BATCH_SIZE_MULTIMODAL: int = 1             # Batch size for multimodal model
    BATCH_SIZE_TEXT: int = 4                   # Batch size for text model
    
    class Config:
        case_sensitive = True
        env_file = ".env"

# EDIT POINT 16: Specialty-specific prompt templates
PROMPT_TEMPLATES = {
    "general_analysis": """
    Medical Case Analysis:
    Patient Information: {patient_info}
    Symptoms: {symptoms}
    Vital Signs: {vital_signs}
    Medical History: {history}
    
    Please provide a comprehensive medical analysis including:
    1. Primary diagnosis with confidence level
    2. Differential diagnoses (top 3)
    3. Recommended tests and follow-up
    4. Risk assessment
    5. Emergency indicators
    """,
    
    "chest_xray_analysis": """
    Chest X-ray Analysis:
    Clinical Context: {clinical_context}
    
    Please analyze this chest X-ray for:
    1. Pulmonary findings (pneumonia, pneumothorax, effusion)
    2. Cardiac silhouette assessment
    3. Bone and soft tissue evaluation
    4. Overall impression and recommendations
    
    Consider the clinical context in your analysis.
    """,
    
    "emergency_assessment": """
    EMERGENCY MEDICAL ASSESSMENT:
    Presenting Symptoms: {symptoms}
    Vital Signs: {vital_signs}
    Duration: {duration}
    
    Urgent Assessment Required:
    1. Immediate life-threatening conditions
    2. Triage level (1-5)
    3. Required immediate interventions
    4. Specialist consultation needs
    5. Time-sensitive diagnostics
    """,
    
    "chronic_disease_monitoring": """
    Chronic Disease Monitoring:
    Conditions: {chronic_conditions}
    Current Symptoms: {symptoms}
    Medications: {medications}
    Recent Changes: {changes}
    
    Assessment Focus:
    1. Disease progression evaluation
    2. Medication effectiveness
    3. Complications screening
    4. Lifestyle recommendations
    5. Follow-up scheduling
    """
}

settings = EnhancedSettings()