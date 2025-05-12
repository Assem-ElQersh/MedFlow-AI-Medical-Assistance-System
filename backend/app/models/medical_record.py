from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Float, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    record_date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Symptoms and complaints
    symptoms = Column(JSON)  # List of symptoms with severity
    description = Column(String)
    
    # Vital signs
    blood_pressure = Column(String)  # Format: "120/80"
    heart_rate = Column(Integer)
    temperature = Column(Float)
    respiratory_rate = Column(Integer)
    oxygen_saturation = Column(Float)
    
    # Medical images
    image_paths = Column(JSON)  # List of paths to medical images
    image_analysis_results = Column(JSON)  # Results from AI analysis
    
    # Diagnosis
    primary_diagnosis = Column(String)
    confidence_score = Column(Float)
    alternative_diagnoses = Column(JSON)  # List of alternative diagnoses with confidence scores
    
    # Treatment
    treatment_plan = Column(JSON)
    medications = Column(JSON)
    follow_up_date = Column(DateTime)
    
    # Emergency status
    is_emergency = Column(Boolean, default=False)
    emergency_notes = Column(String)
    
    # Relationships
    user = relationship("User", back_populates="medical_records")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 