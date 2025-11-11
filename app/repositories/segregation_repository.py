from app.repositories.base import BaseRepository
from app.core.config import settings
from typing import Dict


class SegregationRepository(BaseRepository):
    def __init__(self):
        super().__init__(settings.SEGREGATION_RULES_FILE)
    
    def get_rule(self, class_from: str, class_to: str) -> Dict:
        """Get segregation rule between two classes"""
        # Check both directions
        rule = self.df[
            ((self.df['class_from'] == class_from) & (self.df['class_to'] == class_to)) |
            ((self.df['class_from'] == class_to) & (self.df['class_to'] == class_from))
        ]
        
        if not rule.empty:
            return rule.iloc[0].to_dict()
        
        # Default: can be stowed together
        return {
            'segregation_code': 'X',
            'segregation_rule': 'Can be stowed together',
            'risk_penalty': 0
        }
    
    def get_all_rules(self) -> list:
        """Get all segregation rules"""
        return self.df.to_dict('records')