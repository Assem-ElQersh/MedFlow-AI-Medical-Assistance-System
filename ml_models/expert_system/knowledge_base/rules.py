"""
Medical Expert System Knowledge Base
Contains rules and facts for disease diagnosis based on symptoms
"""

# Disease categories and their associated symptoms
DISEASE_CATEGORIES = {
    'respiratory': {
        'name': 'Respiratory Diseases',
        'symptoms': {
            'cough': {
                'weight': 0.8,
                'subtypes': ['dry', 'wet', 'persistent'],
                'severity_levels': {
                    'mild': 0.3,
                    'moderate': 0.6,
                    'severe': 0.9
                }
            },
            'shortness_of_breath': {
                'weight': 0.9,
                'severity_levels': {
                    'mild': 0.4,
                    'moderate': 0.7,
                    'severe': 1.0
                }
            },
            'chest_pain': {
                'weight': 0.85,
                'subtypes': ['sharp', 'dull', 'pressure'],
                'severity_levels': {
                    'mild': 0.3,
                    'moderate': 0.6,
                    'severe': 0.9
                }
            }
        }
    },
    'cardiovascular': {
        'name': 'Cardiovascular Diseases',
        'symptoms': {
            'chest_pain': {
                'weight': 0.9,
                'subtypes': ['pressure', 'tightness', 'squeezing'],
                'severity_levels': {
                    'mild': 0.4,
                    'moderate': 0.7,
                    'severe': 1.0
                }
            },
            'palpitations': {
                'weight': 0.75,
                'severity_levels': {
                    'mild': 0.3,
                    'moderate': 0.6,
                    'severe': 0.9
                }
            },
            'shortness_of_breath': {
                'weight': 0.8,
                'severity_levels': {
                    'mild': 0.3,
                    'moderate': 0.6,
                    'severe': 0.9
                }
            }
        }
    },
    'neurological': {
        'name': 'Neurological Disorders',
        'symptoms': {
            'headache': {
                'weight': 0.7,
                'subtypes': ['migraine', 'tension', 'cluster'],
                'severity_levels': {
                    'mild': 0.3,
                    'moderate': 0.6,
                    'severe': 0.9
                }
            },
            'dizziness': {
                'weight': 0.65,
                'severity_levels': {
                    'mild': 0.3,
                    'moderate': 0.6,
                    'severe': 0.9
                }
            },
            'numbness': {
                'weight': 0.75,
                'severity_levels': {
                    'mild': 0.3,
                    'moderate': 0.6,
                    'severe': 0.9
                }
            }
        }
    }
}

# Disease-specific rules
DISEASE_RULES = {
    'pneumonia': {
        'category': 'respiratory',
        'required_symptoms': ['cough', 'shortness_of_breath'],
        'optional_symptoms': ['chest_pain', 'fever'],
        'vital_signs': {
            'temperature': {'min': 37.5, 'max': 41.0},
            'respiratory_rate': {'min': 20, 'max': 30},
            'oxygen_saturation': {'min': 90, 'max': 100}
        },
        'risk_factors': ['age', 'smoking', 'chronic_disease'],
        'confidence_threshold': 0.7
    },
    'heart_failure': {
        'category': 'cardiovascular',
        'required_symptoms': ['shortness_of_breath', 'chest_pain'],
        'optional_symptoms': ['palpitations', 'fatigue'],
        'vital_signs': {
            'blood_pressure': {'min': 90, 'max': 140},
            'heart_rate': {'min': 60, 'max': 100},
            'oxygen_saturation': {'min': 90, 'max': 100}
        },
        'risk_factors': ['age', 'hypertension', 'diabetes'],
        'confidence_threshold': 0.75
    },
    'migraine': {
        'category': 'neurological',
        'required_symptoms': ['headache'],
        'optional_symptoms': ['nausea', 'sensitivity_to_light'],
        'vital_signs': {
            'blood_pressure': {'min': 90, 'max': 140},
            'heart_rate': {'min': 60, 'max': 100}
        },
        'risk_factors': ['stress', 'family_history'],
        'confidence_threshold': 0.65
    }
}

# Emergency conditions and their triggers
EMERGENCY_CONDITIONS = {
    'severe_chest_pain': {
        'symptoms': ['chest_pain'],
        'severity': 'severe',
        'duration': 'sudden',
        'priority': 'high'
    },
    'severe_shortness_of_breath': {
        'symptoms': ['shortness_of_breath'],
        'severity': 'severe',
        'duration': 'sudden',
        'priority': 'high'
    },
    'severe_headache': {
        'symptoms': ['headache'],
        'severity': 'severe',
        'duration': 'sudden',
        'priority': 'high'
    }
}

# Treatment recommendations
TREATMENT_RECOMMENDATIONS = {
    'pneumonia': {
        'immediate': ['rest', 'hydration', 'fever_management'],
        'medical': ['antibiotics', 'bronchodilators'],
        'follow_up': ['chest_xray', 'blood_tests'],
        'duration': '7-14 days'
    },
    'heart_failure': {
        'immediate': ['rest', 'salt_restriction'],
        'medical': ['diuretics', 'ace_inhibitors'],
        'follow_up': ['ecg', 'echo'],
        'duration': 'lifetime'
    },
    'migraine': {
        'immediate': ['rest', 'dark_room'],
        'medical': ['pain_relievers', 'triptans'],
        'follow_up': ['neurology_consult'],
        'duration': 'as_needed'
    }
}

# Risk assessment rules
RISK_ASSESSMENT = {
    'age': {
        'high': {'min': 65},
        'moderate': {'min': 45, 'max': 64},
        'low': {'max': 44}
    },
    'smoking': {
        'high': {'current': True},
        'moderate': {'former': True},
        'low': {'never': True}
    },
    'chronic_disease': {
        'high': ['diabetes', 'hypertension', 'heart_disease'],
        'moderate': ['asthma', 'copd'],
        'low': []
    }
} 