from app.repositories.base import BaseRepository
from app.core.config import settings
from typing import Dict
import pandas as pd


class SegregationRepository(BaseRepository):
    def __init__(self):
        super().__init__(settings.SEGREGATION_RULES_FILE)
        self._clean_data()
        print(f"Loaded {len(self.df)} segregation rules")
    
    def _clean_data(self):
        """Clean and standardize class_from and class_to columns"""
        # Convert to string and strip whitespace
        self.df['class_from'] = self.df['class_from'].astype(str).str.strip()
        self.df['class_to'] = self.df['class_to'].astype(str).str.strip()
    
    def get_rule(self, class_from: str, class_to: str) -> Dict:
        """
        Get segregation rule between two classes (bidirectional search)
        """
        # Normalize inputs - convert to string and strip
        class_from = str(class_from).strip()
        class_to = str(class_to).strip()

        # Search both directions
        mask1 = (self.df['class_from'] == class_from) & (self.df['class_to'] == class_to)
        mask2 = (self.df['class_from'] == class_to) & (self.df['class_to'] == class_from)
        rule = self.df[mask1 | mask2]

        if not rule.empty:
            result = rule.iloc[0].to_dict()
            # Convert risk_penalty to int
            result['risk_penalty'] = int(result['risk_penalty'])
            return result

        # Debug: Check if classes exist in dataframe
        has_class_from = self.df[
            (self.df['class_from'] == class_from) | (self.df['class_to'] == class_from)
        ]
        has_class_to = self.df[
            (self.df['class_from'] == class_to) | (self.df['class_to'] == class_to)
        ]

        if len(has_class_from) == 0:
            print(f"WARNING: Class '{class_from}' not found in segregation rules")
        if len(has_class_to) == 0:
            print(f"WARNING: Class '{class_to}' not found in segregation rules")

        # If same class, return X
        if class_from == class_to:
            return {
                'class_from': class_from,
                'class_to': class_to,
                'segregation_code': 'X',
                'segregation_rule': 'Can be stowed together (same class)',
                'risk_penalty': 0  # Already an int
            }

        # Default: no specific rule found
        print(f"WARNING: No rule found for {class_from} <-> {class_to}, defaulting to 'X'")
        return {
            'class_from': class_from,
            'class_to': class_to,
            'segregation_code': 'X',
            'segregation_rule': 'Can be stowed together (no specific rule)',
            'risk_penalty': 0  # Already an int
        }

    def get_all_rules(self) -> list:
        """Get all segregation rules"""
        return self.df.to_dict('records')
    
    def debug_search(self, class_id: str):
        """Debug helper to see all rules for a specific class"""
        class_id = str(class_id).strip()
        matches = self.df[
            (self.df['class_from'] == class_id) | (self.df['class_to'] == class_id)
        ]
        print(f"Rules for class '{class_id}': {len(matches)} found")
        for idx, row in matches.iterrows():
            print(f"  {row['class_from']} <-> {row['class_to']}: Code {row['segregation_code']}")
        return matches.to_dict('records')