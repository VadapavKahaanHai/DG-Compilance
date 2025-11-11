from abc import ABC
import pandas as pd
from functools import lru_cache


class BaseRepository(ABC):
    """Base repository with caching"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._df = None
    
    @property
    def df(self) -> pd.DataFrame:
        """Lazy load and cache dataframe"""
        if self._df is None:
            self._df = pd.read_csv(self.file_path)
        return self._df
    
    def refresh_cache(self):
        """Clear cache and reload data"""
        self._df = None