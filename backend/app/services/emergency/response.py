from typing import Dict, List, Optional
from loguru import logger
from app.core.config import settings

class EmergencyResponseService:
    """Service for handling emergency responses"""
    
    def __init__(self):
        self.notification_enabled = settings.EMERGENCY_NOTIFICATION_ENABLED
    
    async def handle_emergency(
        self,
        emergency_data: Dict,
        patient_data: Dict,
        contact_info: Optional[Dict] = None
    ) -> Dict:
        """
        Handle emergency situation based on analysis results
        """
        try:
            response = {
                "actions_taken": [],
                "notifications_sent": [],
                "follow_up_required": False
            }
            
            # Determine required actions based on urgency level
            urgency_level = emergency_data.get("urgency_level", 1)
            emergency_flags = emergency_data.get("emergency_flags", [])
            
            # Take immediate actions
            actions = self._determine_actions(urgency_level, emergency_flags)
            response["actions_taken"].extend(actions)
            
            # Send notifications if enabled
            if self.notification_enabled:
                notifications = self._send_notifications(
                    urgency_level,
                    emergency_flags,
                    patient_data,
                    contact_info
                )
                response["notifications_sent"].extend(notifications)
            
            # Determine if follow-up is required
            response["follow_up_required"] = self._requires_follow_up(
                urgency_level,
                emergency_flags
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Emergency response failed: {str(e)}")
            raise
    
    def _determine_actions(
        self,
        urgency_level: int,
        emergency_flags: List[str]
    ) -> List[Dict]:
        """Determine required actions based on urgency level and flags"""
        actions = []
        
        # Level 5 - Critical
        if urgency_level == 5:
            actions.append({
                "type": "emergency_services",
                "action": "Call 911",
                "priority": "immediate"
            })
            actions.append({
                "type": "hospital_alert",
                "action": "Alert nearest hospital",
                "priority": "immediate"
            })
        
        # Level 4 - Severe
        elif urgency_level == 4:
            actions.append({
                "type": "urgent_care",
                "action": "Direct to urgent care",
                "priority": "high"
            })
            actions.append({
                "type": "specialist_alert",
                "action": "Alert relevant specialist",
                "priority": "high"
            })
        
        # Level 3 - Moderate
        elif urgency_level == 3:
            actions.append({
                "type": "primary_care",
                "action": "Schedule immediate primary care visit",
                "priority": "medium"
            })
        
        # Add specific actions based on emergency flags
        for flag in emergency_flags:
            if "cardiac" in flag.lower():
                actions.append({
                    "type": "cardiac_monitoring",
                    "action": "Initiate cardiac monitoring",
                    "priority": "high"
                })
            elif "respiratory" in flag.lower():
                actions.append({
                    "type": "respiratory_support",
                    "action": "Prepare respiratory support",
                    "priority": "high"
                })
        
        return actions
    
    def _send_notifications(
        self,
        urgency_level: int,
        emergency_flags: List[str],
        patient_data: Dict,
        contact_info: Optional[Dict] = None
    ) -> List[Dict]:
        """Send notifications to relevant parties"""
        notifications = []
        
        # Notify emergency contacts if available
        if contact_info:
            if urgency_level >= 4:
                notifications.append({
                    "type": "emergency_contact",
                    "recipient": contact_info.get("emergency_contact"),
                    "message": "Emergency medical attention required",
                    "priority": "high"
                })
            
            if urgency_level >= 3:
                notifications.append({
                    "type": "family",
                    "recipient": contact_info.get("family_contact"),
                    "message": "Urgent medical attention recommended",
                    "priority": "medium"
                })
        
        # Notify healthcare providers
        if urgency_level >= 4:
            notifications.append({
                "type": "healthcare_provider",
                "recipient": patient_data.get("primary_physician"),
                "message": "Emergency situation requiring immediate attention",
                "priority": "high"
            })
        
        return notifications
    
    def _requires_follow_up(
        self,
        urgency_level: int,
        emergency_flags: List[str]
    ) -> bool:
        """Determine if follow-up is required"""
        # Always require follow-up for high urgency levels
        if urgency_level >= 4:
            return True
        
        # Check for specific flags that require follow-up
        follow_up_flags = [
            "cardiac",
            "respiratory",
            "neurological",
            "severe"
        ]
        
        return any(flag in " ".join(emergency_flags).lower() for flag in follow_up_flags) 