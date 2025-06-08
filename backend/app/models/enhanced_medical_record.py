# app/models/enhanced_medical_record.py - Enhanced version of your medical_record.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Float, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class EnhancedMedicalRecord(Base):
    """Enhanced medical record with MedGemma analysis fields"""
    __tablename__ = "enhanced_medical_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    record_date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Basic Medical Information
    symptoms = Column(JSON)  # List of symptoms with severity
    vital_signs = Column(JSON)  # Vital signs measurements
    medical_images = Column(JSON)  # List of medical image paths
    patient_history = Column(JSON)  # Relevant medical history
    
    # MedGemma Analysis Results
    medgemma_analysis = Column(JSON)  # Raw MedGemma analysis
    image_analysis = Column(JSON)  # Medical image analysis results
    text_analysis = Column(JSON)  # Clinical text analysis
    consensus_analysis = Column(JSON)  # Combined analysis results
    
    # Diagnosis and Treatment
    primary_diagnosis = Column(String)
    differential_diagnoses = Column(JSON)  # List of possible diagnoses
    confidence_score = Column(Float)
    treatment_plan = Column(JSON)
    medications = Column(JSON)
    
    # Emergency and Follow-up
    is_emergency = Column(Boolean, default=False)
    emergency_flags = Column(JSON)
    urgency_level = Column(Integer)  # 1-5 scale
    follow_up_date = Column(DateTime)
    follow_up_plan = Column(JSON)
    
    # Model Performance
    model_versions = Column(JSON)
    processing_time_ms = Column(Integer)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="medical_records")

# EDIT POINT 9: Add model comparison tracking
class ModelComparisonRecord(Base):
    """Track comparisons between MedGemma and legacy models"""
    __tablename__ = "model_comparisons"
    
    id = Column(Integer, primary_key=True, index=True)
    medical_record_id = Column(Integer, ForeignKey("enhanced_medical_records.id"))
    
    # Model Results
    medgemma_prediction = Column(String)
    medgemma_confidence = Column(Float)
    legacy_prediction = Column(String)
    legacy_confidence = Column(Float)
    
    # Comparison Metrics
    agreement_level = Column(String)  # 'high', 'medium', 'low'
    consensus_reached = Column(Boolean)
    human_validation = Column(String)  # If validated by physician
    
    # Performance Tracking
    accuracy_score = Column(Float)  # If ground truth available
    processing_time_comparison = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    medical_record = relationship("EnhancedMedicalRecord", back_populates="model_comparisons")

# EDIT POINT 10: Enhanced user model with medical profile
class EnhancedUser(Base):
    """Enhanced user model with comprehensive medical profile"""
    __tablename__ = "enhanced_users"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Keep existing fields
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    date_of_birth = Column(DateTime)
    gender = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # NEW: Enhanced medical profile
    medical_history = Column(JSON)              # Comprehensive medical history
    current_medications = Column(JSON)          # Current medication list
    allergies = Column(JSON)                   # Known allergies
    family_history = Column(JSON)             # Family medical history
    lifestyle_factors = Column(JSON)          # Smoking, alcohol, exercise, etc.
    
    # Risk factors
    chronic_conditions = Column(JSON)          # List of chronic conditions
    risk_assessment = Column(JSON)             # Calculated risk scores
    
    # Preferences
    ai_model_preferences = Column(JSON)        # User preferences for AI analysis
    notification_preferences = Column(JSON)    # Alert preferences
    
    # Emergency contacts
    emergency_contacts = Column(JSON)          # Emergency contact information
    
    # Relationships
    medical_records = relationship("EnhancedMedicalRecord", back_populates="user")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())