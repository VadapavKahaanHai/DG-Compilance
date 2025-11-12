from typing import List, Dict
from app.models.cargo import CargoItem
from app.models.compliance import Recommendation


class RecommendationService:
    """
    🎯 Generate actionable recommendations
    Equivalent to generate_recommendations() from your Streamlit app
    """
    
    def generate_recommendations(
        self, 
        assessment: Dict, 
        cargo_items: List[CargoItem]
    ) -> List[Recommendation]:
        """
        Generate comprehensive recommendations based on assessment
        """
        recommendations = []
        
        # 🚨 CRITICAL: Violations detected
        if assessment['violations']:
            recommendations.append(Recommendation(
                priority='CRITICAL',
                action=f"Resolve {len(assessment['violations'])} prohibited combinations",
                detail="These cargo items MUST be in separate holds or cannot be shipped together"
            ))
        
        # ⚠️ HIGH: Warnings present
        if assessment['warnings']:
            recommendations.append(Recommendation(
                priority='HIGH',
                action=f"Address {len(assessment['warnings'])} warning combinations",
                detail="Ensure proper separation distances are maintained (1.5m - 3m minimum)"
            ))
        
        # 📊 HIGH: Overall risk assessment
        if assessment['risk_score'] > 50:
            recommendations.append(Recommendation(
                priority='HIGH',
                action="Review overall cargo plan",
                detail="High-risk configuration detected. Consider reorganizing cargo placement"
            ))
        
        # ✅ LOW: All compliant
        if not assessment['violations'] and not assessment['warnings']:
            recommendations.append(Recommendation(
                priority='LOW',
                action="Proceed with current configuration",
                detail="All cargo combinations are compliant with IMDG Code"
            ))
        
        # 🧨 Class-specific recommendations
        class_counts = {}
        for item in cargo_items:
            class_id = item.class_id
            class_counts[class_id] = class_counts.get(class_id, 0) + 1
        
        # Explosives
        if '1.1' in class_counts or '1.2' in class_counts:
            recommendations.append(Recommendation(
                priority='CRITICAL',
                action="Explosive cargo detected",
                detail="Ensure explosive magazine requirements and maximum segregation distances"
            ))
        
        # Infectious substances
        if '6.2' in class_counts:
            recommendations.append(Recommendation(
                priority='HIGH',
                action="Infectious substances present",
                detail="Verify special packaging and containment protocols"
            ))
        
        # Radioactive materials
        if '7' in class_counts:
            recommendations.append(Recommendation(
                priority='CRITICAL',
                action="Radioactive materials detected",
                detail="Implement radiation monitoring and category-based segregation"
            ))
        
        return recommendations