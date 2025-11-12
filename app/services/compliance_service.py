from typing import List, Dict
from app.models.cargo import CargoItem
from app.repositories.segregation_repository import SegregationRepository
from app.repositories.dg_class_repository import DGClassRepository
from app.services.risk_service import RiskService


class ComplianceService:
    def __init__(self):
        self.segregation_repo = SegregationRepository()
        self.dg_class_repo = DGClassRepository()
        self.risk_service = RiskService()
    
    def assess_cargo_compatibility(self, cargo_list: List[CargoItem]) -> Dict:
        """
        Assess compatibility of multiple cargo items
        """
        violations = []
        warnings = []
        compliant = []
        total_risk_score = 0
        
        # Convert Pydantic models to dicts
        cargo_dicts = [item.dict() for item in cargo_list]
        
        print(f"Assessing {len(cargo_dicts)} cargo items")
        
        # Compare each pair
        total_pairs = 0
        for i in range(len(cargo_dicts)):
            for j in range(i + 1, len(cargo_dicts)):
                cargo1 = cargo_dicts[i]
                cargo2 = cargo_dicts[j]
                
                class1 = cargo1['class_id']
                class2 = cargo2['class_id']
                
                total_pairs += 1
                
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
                else:
                    # Unknown code - treat as warning
                    print(f"WARNING: Unknown segregation code '{seg_code}' for {class1} <-> {class2}")
                    warnings.append(comparison)
                    total_risk_score += rule.get('risk_penalty', 5)
        
        # Calculate risk percentage
        risk_score = self.risk_service.calculate_risk_percentage(
            total_risk_score, len(cargo_list)
        )
        
        risk_level = self.risk_service.get_risk_level(risk_score)
        
        print(f"Assessment complete: {total_pairs} pairs analyzed, Risk score: {risk_score:.1f}%")
        
        return {
            'compliant': compliant,
            'warnings': warnings,
            'violations': violations,
            'risk_score': risk_score,
            'risk_level': risk_level,
            'total_risk_points': total_risk_score,
            'total_comparisons': total_pairs
        }
    
    def get_detailed_analysis(self, cargo_list: List[CargoItem]) -> Dict:
        """
        Extended analysis with class information
        """
        assessment = self.assess_cargo_compatibility(cargo_list)
        
        # Add class-specific details
        class_details = {}
        for item in cargo_list:
            class_info = self.dg_class_repo.get_class_info(item.class_id)
            if class_info:
                class_details[item.class_id] = class_info
        
        assessment['class_details'] = class_details
        return assessment