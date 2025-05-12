import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from knowledge_base.rules import (
    DISEASE_CATEGORIES,
    DISEASE_RULES,
    EMERGENCY_CONDITIONS,
    TREATMENT_RECOMMENDATIONS,
    RISK_ASSESSMENT
)

class ExpertSystem:
    def __init__(self):
        self.disease_categories = DISEASE_CATEGORIES
        self.disease_rules = DISEASE_RULES
        self.emergency_conditions = EMERGENCY_CONDITIONS
        self.treatment_recommendations = TREATMENT_RECOMMENDATIONS
        self.risk_assessment = RISK_ASSESSMENT

    def analyze_symptoms(self, symptoms, vital_signs=None, risk_factors=None):
        """
        Analyze symptoms and return possible diagnoses with confidence scores
        """
        diagnoses = []
        emergency_flags = []

        # Check for emergency conditions first
        for condition, rules in self.emergency_conditions.items():
            for symptom in rules['symptoms']:
                if symptom in symptoms:
                    symptom_data = symptoms[symptom]
                    if (symptom_data.get('severity') == rules['severity'] and
                        symptom_data.get('duration') == rules['duration']):
                        emergency_flags.append({
                            'condition': condition,
                            'priority': rules['priority'],
                            'symptoms': [symptom]
                        })

        # Analyze for specific diseases
        for disease, rules in self.disease_rules.items():
            confidence = 0.0
            matched_symptoms = []
            
            # Check required symptoms
            required_matches = 0
            for symptom in rules['required_symptoms']:
                if symptom in symptoms:
                    symptom_data = symptoms[symptom]
                    weight = self.disease_categories[rules['category']]['symptoms'][symptom]['weight']
                    severity = symptom_data.get('severity', 'moderate')
                    severity_weight = self.disease_categories[rules['category']]['symptoms'][symptom]['severity_levels'][severity]
                    confidence += weight * severity_weight
                    required_matches += 1
                    matched_symptoms.append(symptom)
            
            # Check optional symptoms
            for symptom in rules['optional_symptoms']:
                if symptom in symptoms:
                    symptom_data = symptoms[symptom]
                    weight = self.disease_categories[rules['category']]['symptoms'][symptom]['weight']
                    severity = symptom_data.get('severity', 'moderate')
                    severity_weight = self.disease_categories[rules['category']]['symptoms'][symptom]['severity_levels'][severity]
                    confidence += 0.5 * weight * severity_weight
                    matched_symptoms.append(symptom)
            
            # Check vital signs if provided
            if vital_signs and 'vital_signs' in rules:
                vital_signs_match = 0
                total_vital_signs = len(rules['vital_signs'])
                
                for vital_sign, ranges in rules['vital_signs'].items():
                    if vital_sign in vital_signs:
                        value = vital_signs[vital_sign]
                        if ranges['min'] <= value <= ranges['max']:
                            vital_signs_match += 1
                
                confidence += 0.2 * (vital_signs_match / total_vital_signs)
            
            # Check risk factors if provided
            if risk_factors and 'risk_factors' in rules:
                risk_score = 0
                for factor in rules['risk_factors']:
                    if factor in risk_factors:
                        risk_level = self._assess_risk_level(factor, risk_factors[factor])
                        risk_score += 0.1 if risk_level == 'high' else 0.05
                confidence += min(0.2, risk_score)
            
            # Normalize confidence based on required symptoms
            if required_matches == len(rules['required_symptoms']):
                confidence = confidence / (len(rules['required_symptoms']) + 0.5 * len(rules['optional_symptoms']))
                
                if confidence >= rules['confidence_threshold']:
                    diagnoses.append({
                        'disease': disease,
                        'confidence': confidence,
                        'matched_symptoms': matched_symptoms,
                        'category': rules['category']
                    })
        
        # Sort diagnoses by confidence
        diagnoses.sort(key=lambda x: x['confidence'], reverse=True)
        
        return {
            'diagnoses': diagnoses,
            'emergency_flags': emergency_flags
        }

    def get_treatment_recommendations(self, diagnosis):
        """
        Get treatment recommendations for a specific diagnosis
        """
        if diagnosis in self.treatment_recommendations:
            return self.treatment_recommendations[diagnosis]
        return None

    def _assess_risk_level(self, factor, value):
        """
        Assess risk level for a specific factor
        """
        if factor not in self.risk_assessment:
            return 'low'
        
        rules = self.risk_assessment[factor]
        
        if isinstance(value, (int, float)):
            if 'high' in rules and value >= rules['high']['min']:
                return 'high'
            elif 'moderate' in rules and rules['moderate']['min'] <= value <= rules['moderate']['max']:
                return 'moderate'
            else:
                return 'low'
        elif isinstance(value, bool):
            if value and 'high' in rules and rules['high'].get('current', False):
                return 'high'
            elif value and 'moderate' in rules and rules['moderate'].get('former', False):
                return 'moderate'
            else:
                return 'low'
        elif isinstance(value, list):
            if any(item in rules['high'] for item in value):
                return 'high'
            elif any(item in rules['moderate'] for item in value):
                return 'moderate'
            else:
                return 'low'
        
        return 'low'

def main():
    # Example usage
    expert_system = ExpertSystem()
    
    # Example symptoms
    symptoms = {
        'cough': {
            'severity': 'moderate',
            'duration': '3 days',
            'subtype': 'wet'
        },
        'shortness_of_breath': {
            'severity': 'severe',
            'duration': 'sudden'
        },
        'chest_pain': {
            'severity': 'moderate',
            'duration': '2 days',
            'subtype': 'pressure'
        }
    }
    
    # Example vital signs
    vital_signs = {
        'temperature': 38.5,
        'respiratory_rate': 24,
        'oxygen_saturation': 92
    }
    
    # Example risk factors
    risk_factors = {
        'age': 70,
        'smoking': True,
        'chronic_disease': ['diabetes', 'hypertension']
    }
    
    # Analyze symptoms
    results = expert_system.analyze_symptoms(symptoms, vital_signs, risk_factors)
    
    # Print results
    print("\nDiagnosis Results:")
    for diagnosis in results['diagnoses']:
        print(f"\nDisease: {diagnosis['disease']}")
        print(f"Confidence: {diagnosis['confidence']:.2%}")
        print(f"Matched Symptoms: {', '.join(diagnosis['matched_symptoms'])}")
        
        # Get treatment recommendations
        treatment = expert_system.get_treatment_recommendations(diagnosis['disease'])
        if treatment:
            print("\nTreatment Recommendations:")
            print(f"Immediate: {', '.join(treatment['immediate'])}")
            print(f"Medical: {', '.join(treatment['medical'])}")
            print(f"Follow-up: {', '.join(treatment['follow_up'])}")
            print(f"Duration: {treatment['duration']}")
    
    if results['emergency_flags']:
        print("\nEMERGENCY ALERTS:")
        for flag in results['emergency_flags']:
            print(f"- {flag['condition']} (Priority: {flag['priority']})")

if __name__ == '__main__':
    main() 