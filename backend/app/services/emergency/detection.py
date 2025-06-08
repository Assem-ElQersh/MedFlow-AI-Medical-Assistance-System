from typing import Dict, List, Optional
from loguru import logger
from app.core.config import settings

class EmergencyDetectionService:
    """Service for detecting emergency conditions"""
    
    def __init__(self):
        self.emergency_threshold = settings.EMERGENCY_CONFIDENCE_THRESHOLD
    
    async def analyze_emergency_conditions(
        self,
        vital_signs: Dict,
        symptoms: List[Dict],
        image_analysis: Optional[Dict] = None,
        patient_history: Optional[Dict] = None
    ) -> Dict:
        """
        Analyze all available data for emergency conditions
        """
        try:
            results = {
                "emergency_flags": [],
                "urgency_level": 1,  # Default to lowest urgency
                "recommendations": []
            }
            
            # Check vital signs
            vital_signs_flags = self._check_vital_signs(vital_signs)
            results["emergency_flags"].extend(vital_signs_flags)
            
            # Check symptoms
            symptom_flags = self._check_symptoms(symptoms)
            results["emergency_flags"].extend(symptom_flags)
            
            # Check image analysis if available
            if image_analysis:
                image_flags = self._check_image_analysis(image_analysis)
                results["emergency_flags"].extend(image_flags)
            
            # Calculate urgency level
            results["urgency_level"] = self._calculate_urgency_level(
                results["emergency_flags"],
                patient_history
            )
            
            # Generate recommendations
            results["recommendations"] = self._generate_emergency_recommendations(
                results["emergency_flags"],
                results["urgency_level"]
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Emergency analysis failed: {str(e)}")
            raise
    
    def _check_vital_signs(self, vital_signs: Dict) -> List[str]:
        """Check vital signs for emergency conditions"""
        flags = []
        
        # Blood pressure check
        if vital_signs.get("blood_pressure"):
            systolic, diastolic = map(int, vital_signs["blood_pressure"].split("/"))
            if systolic > 180 or diastolic > 120:
                flags.append("Severe hypertension")
            elif systolic < 90 or diastolic < 60:
                flags.append("Severe hypotension")
        
        # Heart rate check
        heart_rate = vital_signs.get("heart_rate")
        if heart_rate:
            if heart_rate > 150:
                flags.append("Severe tachycardia")
            elif heart_rate < 40:
                flags.append("Severe bradycardia")
        
        # Temperature check
        temperature = vital_signs.get("temperature")
        if temperature:
            if temperature > 39.5:
                flags.append("High fever")
            elif temperature < 35:
                flags.append("Hypothermia")
        
        # Respiratory rate check
        resp_rate = vital_signs.get("respiratory_rate")
        if resp_rate:
            if resp_rate > 30:
                flags.append("Severe tachypnea")
            elif resp_rate < 8:
                flags.append("Severe bradypnea")
        
        # Oxygen saturation check
        o2_sat = vital_signs.get("oxygen_saturation")
        if o2_sat:
            if o2_sat < 90:
                flags.append("Hypoxemia")
        
        return flags
    
    def _check_symptoms(self, symptoms: List[Dict]) -> List[str]:
        """Check symptoms for emergency conditions"""
        flags = []
        emergency_symptoms = {
            "chest pain": "Severe chest pain",
            "shortness of breath": "Severe respiratory distress",
            "severe bleeding": "Severe bleeding",
            "loss of consciousness": "Loss of consciousness",
            "seizure": "Active seizure",
            "stroke symptoms": "Possible stroke"
        }
        
        for symptom in symptoms:
            name = symptom.get("name", "").lower()
            severity = symptom.get("severity", "").lower()
            
            if name in emergency_symptoms and severity in ["severe", "critical"]:
                flags.append(emergency_symptoms[name])
        
        return flags
    
    def _check_image_analysis(self, image_analysis: Dict) -> List[str]:
        """Check image analysis results for emergency conditions"""
        flags = []
        
        # Check for critical findings
        findings = image_analysis.get("findings", [])
        for finding in findings:
            if finding.get("severity") == "critical":
                flags.append(f"Critical finding: {finding.get('description')}")
        
        return flags
    
    def _calculate_urgency_level(
        self,
        emergency_flags: List[str],
        patient_history: Optional[Dict] = None
    ) -> int:
        """Calculate urgency level (1-5) based on emergency flags"""
        if not emergency_flags:
            return 1
        
        # Count critical flags
        critical_flags = [flag for flag in emergency_flags if "critical" in flag.lower()]
        
        # Adjust based on patient history
        risk_multiplier = 1.0
        if patient_history:
            if patient_history.get("high_risk_conditions"):
                risk_multiplier = 1.5
            if patient_history.get("immunocompromised"):
                risk_multiplier = 1.3
        
        # Calculate base level
        base_level = min(5, 1 + len(critical_flags))
        
        # Apply risk multiplier
        final_level = min(5, int(base_level * risk_multiplier))
        
        return final_level
    
    def _generate_emergency_recommendations(
        self,
        emergency_flags: List[str],
        urgency_level: int
    ) -> List[Dict]:
        """Generate emergency recommendations based on flags and urgency"""
        recommendations = []
        
        if urgency_level >= 4:
            recommendations.append({
                "action": "Immediate emergency response",
                "details": "Call emergency services immediately",
                "priority": "critical"
            })
        
        if urgency_level >= 3:
            recommendations.append({
                "action": "Urgent medical attention",
                "details": "Seek immediate medical care",
                "priority": "high"
            })
        
        # Add specific recommendations based on flags
        for flag in emergency_flags:
            if "chest pain" in flag.lower():
                recommendations.append({
                    "action": "Cardiac evaluation",
                    "details": "Immediate ECG and cardiac enzymes",
                    "priority": "high"
                })
            elif "respiratory" in flag.lower():
                recommendations.append({
                    "action": "Respiratory support",
                    "details": "Oxygen therapy and respiratory monitoring",
                    "priority": "high"
                })
        
        return recommendations 