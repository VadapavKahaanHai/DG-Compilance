from app.core.config import settings
from app.models.compliance import RiskLevel


class RiskService:
    """
    🎯 Risk scoring and level determination
    Equivalent to get_risk_level() from your Streamlit app
    """
    
    def calculate_risk_percentage(self, total_risk_points: float, num_items: int) -> float:
        """
        Calculate risk percentage (0-100 scale)
        Same logic as your Streamlit version
        """
        if num_items < 2:
            return 0.0
        
        # Max penalty per pair is 25 points
        max_possible_score = num_items * (num_items - 1) * 25 / 2
        
        if max_possible_score > 0:
            risk_percentage = min(100.0, (total_risk_points / max_possible_score) * 100)
        else:
            risk_percentage = 0.0
        
        return round(risk_percentage, 2)
    
    def get_risk_level(self, risk_score: float) -> RiskLevel:
        """
        Determine risk level based on thresholds
        """
        if risk_score < settings.RISK_LOW_THRESHOLD:  # < 20
            return RiskLevel.LOW
        elif risk_score < settings.RISK_MEDIUM_THRESHOLD:  # < 50
            return RiskLevel.MEDIUM
        elif risk_score < settings.RISK_HIGH_THRESHOLD:  # < 75
            return RiskLevel.HIGH
        else:
            return RiskLevel.CRITICAL
    
    def get_risk_color(self, risk_level: RiskLevel) -> str:
        """Get color code for risk level"""
        colors = {
            RiskLevel.LOW: "#28a745",
            RiskLevel.MEDIUM: "#ffc107",
            RiskLevel.HIGH: "#fd7e14",
            RiskLevel.CRITICAL: "#dc3545"
        }
        return colors.get(risk_level, "#6c757d")