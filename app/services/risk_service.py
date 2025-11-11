from app.core.config import settings
from app.models.compliance import RiskLevel


class RiskService:
    def calculate_risk_percentage(self, total_risk_points: float, num_items: int) -> float:
        """Calculate risk percentage (0-100)"""
        if num_items < 2:
            return 0.0
        
        max_possible_score = num_items * (num_items - 1) * 25 / 2
        
        if max_possible_score > 0:
            return min(100.0, (total_risk_points / max_possible_score) * 100)
        
        return 0.0
    
    def get_risk_level(self, risk_score: float) -> RiskLevel:
        """Get risk level based on score"""
        if risk_score < settings.RISK_LOW_THRESHOLD:
            return RiskLevel.LOW
        elif risk_score < settings.RISK_MEDIUM_THRESHOLD:
            return RiskLevel.MEDIUM
        elif risk_score < settings.RISK_HIGH_THRESHOLD:
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL