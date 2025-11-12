from app.repositories.base import BaseRepository
from app.core.config import settings
from typing import Dict, Optional


class DGClassRepository(BaseRepository):
    """Repository for DG class information"""
    
    def __init__(self):
        super().__init__(settings.DG_CLASSES_FILE)
    
    def get_class_info(self, class_id: str) -> Optional[Dict]:
        """
        Get detailed information about a DG class
        Equivalent to get_class_info() from your Streamlit app
        """
        info = self.df[self.df['class_id'] == class_id]
        
        if not info.empty:
            return info.iloc[0].to_dict()
        
        return None
    
    def get_all_classes(self) -> list:
        """Get all DG classes"""
        return self.df.to_dict('records')
    
    def search_by_name(self, name: str) -> list:
        """Search classes by name"""
        filtered = self.df[
            self.df['class_name'].str.contains(name, case=False, na=False)
        ]
        return filtered.to_dict('records')