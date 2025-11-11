from typing import List, Dict
from app.models.cargo import CargoItem
from app.repositories.segregation_repository import SegregationRepository
from app.services.risk_service import RiskService


class ComplianceService:
    def __init__(self):
        self.segregation_repo = SegregationRepository()
        self.risk_service = RiskService()
    
    def assess_cargo_compatibility(self, cargo_list: List[CargoItem]) -> Dict:
        """Assess compatibility of multiple cargo items"""
        violations = []
        warnings = []
        compliant = []
        total_risk_score = 0
        
        # Convert Pydantic models to dicts
        cargo_dicts = [item.dict() for item in cargo_list]
        
        # Compare each pair
        for i, cargo1 in enumerate(cargo_dicts):
            for j, cargo2 in enumerate(cargo_dicts[i+1:], start=i+1):
                class1 = cargo1['class_id']
                class2 = cargo2['class_id']
                
                # Get segregation rule
                rule = self.segregation_repo.get_rule(class1, class2)
                seg_code = rule['segregation_code']
                
                comparison = {
                    'cargo1': cargo1,
                    'cargo2': cargo2,
                    'rule': rule,
                    'index_pair': (i, j)
                }
                
                # Categorize based on segregation code
                if seg_code == 'X':
                    compliant.append(comparison)
                elif seg_code in ['1', '2']:
                    warnings.append(comparison)
                    total_risk_score += rule['risk_penalty']
                elif seg_code in ['3', '4']:
                    violations.append(comparison)
                    total_risk_score += rule['risk_penalty']
        
        # Calculate risk percentage
        risk_score = self.risk_service.calculate_risk_percentage(
            total_risk_score, len(cargo_list)
        )
        
        risk_level = self.risk_service.get_risk_level(risk_score)
        
        return {
            'compliant': compliant,
            'warnings': warnings,
            'violations': violations,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'total_risk_points': total_risk_score,
            'total_comparisons': len(violations) + len(warnings) + len(compliant)
        }