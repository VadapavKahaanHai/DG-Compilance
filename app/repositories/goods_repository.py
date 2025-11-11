from app.repositories.base import BaseRepository
from app.core.config import settings
from app.core.exceptions import DataNotFoundException
from typing import List, Dict, Optional


class GoodsRepository(BaseRepository):
    def __init__(self):
        super().__init__(settings.GOODS_FILE)
    
    def search(self, query: str, class_filter: Optional[str] = None) -> List[Dict]:
        """Search goods by UN number or name"""
        filtered = self.df[
            self.df['un_number'].str.contains(query, case=False, na=False) |
            self.df['proper_shipping_name'].str.contains(query, case=False, na=False)
        ]
        
        if class_filter:
            filtered = filtered[filtered['class_id'] == class_filter]
        
        return filtered.to_dict('records')
    
    def get_by_un_number(self, un_number: str) -> Dict:
        """Get good by UN number"""
        result = self.df[self.df['un_number'] == un_number]
        
        if result.empty:
            raise DataNotFoundException(f"Good with UN number {un_number} not found")
        
        return result.iloc[0].to_dict()
    
    def get_all(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Get all goods with pagination"""
        return self.df.iloc[offset:offset+limit].to_dict('records')