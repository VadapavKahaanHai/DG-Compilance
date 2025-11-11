from typing import List, Dict
from app.models.cargo import CargoItem
from app.models.compliance import Recommendation


class RecommendationService:
    def generate_recommendations(self, assessment: Dict, cargo_items: List[CargoItem]) -> List[Recommendation]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if assessment['violations']:
            recommendations.append(Recommendation(
                priority='CRITICAL',
                action=f"Resolve {len(assessment['violations'])} prohibited combinations",
                detail="These cargo items MUST be in separate holds or cannot be shipped together"
            ))
        
        if assessment['warnings']:
            recommendations.append(Recommendation(
                priority='HIGH',
                action=f"Address {len(assessment['warnings'])} warning combinations",
                detail="Ensure proper separation distances are maintained (1.5m - 3m minimum)"
            ))
        
        if assessment['risk_score'] > 50:
            recommendations.append(Recommendation(
                priority='HIGH',
                action="Review overall cargo plan",
                detail="High-risk configuration detected. Consider reorganizing cargo placement"
            ))
        
        if not assessment['violations'] and not assessment['warnings']:
            recommendations.append(Recommendation(
                priority='LOW',
                action="Proceed with current configuration",
                detail="All cargo combinations are compliant with IMDG Code"
            ))
        
        return recommendations