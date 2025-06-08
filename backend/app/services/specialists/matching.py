from typing import Dict, List, Optional
from loguru import logger
from app.core.config import settings
from app.models.specialist import Specialist
from app.schemas.specialist import SpecialistMatch

class SpecialistMatchingService:
    """Service for matching patients with appropriate specialists"""
    
    def __init__(self):
        self.match_threshold = settings.SPECIALIST_MATCH_THRESHOLD
    
    async def find_matching_specialists(
        self,
        diagnosis: Dict,
        patient_data: Dict,
        location: Optional[Dict] = None,
        max_results: int = 5
    ) -> List[SpecialistMatch]:
        """
        Find matching specialists based on diagnosis and patient data
        """
        try:
            # Get required specialties based on diagnosis
            required_specialties = self._determine_required_specialties(diagnosis)
            
            # Get available specialists
            specialists = await self._get_available_specialists(
                required_specialties,
                location
            )
            
            # Score and rank specialists
            scored_specialists = self._score_specialists(
                specialists,
                diagnosis,
                patient_data
            )
            
            # Filter and sort by score
            matches = [
                match for match in scored_specialists
                if match.score >= self.match_threshold
            ]
            matches.sort(key=lambda x: x.score, reverse=True)
            
            return matches[:max_results]
            
        except Exception as e:
            logger.error(f"Specialist matching failed: {str(e)}")
            raise
    
    def _determine_required_specialties(self, diagnosis: Dict) -> List[str]:
        """Determine required specialties based on diagnosis"""
        specialties = set()
        
        # Add primary specialty based on condition
        if "condition" in diagnosis:
            condition = diagnosis["condition"].lower()
            if "cardiac" in condition or "heart" in condition:
                specialties.add("cardiology")
            elif "respiratory" in condition or "lung" in condition:
                specialties.add("pulmonology")
            elif "neurological" in condition or "brain" in condition:
                specialties.add("neurology")
            # Add more condition mappings as needed
        
        # Add specialties based on symptoms
        if "symptoms" in diagnosis:
            for symptom in diagnosis["symptoms"]:
                symptom = symptom.lower()
                if "chest pain" in symptom:
                    specialties.add("cardiology")
                elif "shortness of breath" in symptom:
                    specialties.add("pulmonology")
                elif "headache" in symptom:
                    specialties.add("neurology")
                # Add more symptom mappings as needed
        
        return list(specialties)
    
    async def _get_available_specialists(
        self,
        specialties: List[str],
        location: Optional[Dict] = None
    ) -> List[Specialist]:
        """Get available specialists matching the required specialties"""
        # TODO: Implement database query to get available specialists
        # This is a placeholder implementation
        return []
    
    def _score_specialists(
        self,
        specialists: List[Specialist],
        diagnosis: Dict,
        patient_data: Dict
    ) -> List[SpecialistMatch]:
        """Score and rank specialists based on various factors"""
        matches = []
        
        for specialist in specialists:
            score = 0.0
            
            # Score based on specialty match
            if specialist.specialty in self._determine_required_specialties(diagnosis):
                score += 0.4
            
            # Score based on experience with condition
            if self._has_experience_with_condition(specialist, diagnosis):
                score += 0.3
            
            # Score based on patient history compatibility
            if self._is_compatible_with_patient(specialist, patient_data):
                score += 0.2
            
            # Score based on availability
            if self._is_available_soon(specialist):
                score += 0.1
            
            matches.append(SpecialistMatch(
                specialist=specialist,
                score=score,
                match_reasons=self._get_match_reasons(specialist, diagnosis)
            ))
        
        return matches
    
    def _has_experience_with_condition(
        self,
        specialist: Specialist,
        diagnosis: Dict
    ) -> bool:
        """Check if specialist has experience with the condition"""
        # TODO: Implement experience check
        return True
    
    def _is_compatible_with_patient(
        self,
        specialist: Specialist,
        patient_data: Dict
    ) -> bool:
        """Check if specialist is compatible with patient's needs"""
        # TODO: Implement compatibility check
        return True
    
    def _is_available_soon(self, specialist: Specialist) -> bool:
        """Check if specialist is available soon"""
        # TODO: Implement availability check
        return True
    
    def _get_match_reasons(
        self,
        specialist: Specialist,
        diagnosis: Dict
    ) -> List[str]:
        """Get reasons why the specialist is a good match"""
        reasons = []
        
        if specialist.specialty in self._determine_required_specialties(diagnosis):
            reasons.append(f"Specializes in {specialist.specialty}")
        
        if self._has_experience_with_condition(specialist, diagnosis):
            reasons.append("Has experience with this condition")
        
        if self._is_available_soon(specialist):
            reasons.append("Available for immediate consultation")
        
        return reasons 