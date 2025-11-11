from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "DG Compliance API"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Data paths
    DATA_DIR: str = "data"
    DG_CLASSES_FILE: str = "data/dg_classes.csv"
    SEGREGATION_RULES_FILE: str = "data/segregation_rules.csv"
    GOODS_FILE: str = "data/sample_goods.csv"
    
    # Risk thresholds
    RISK_LOW_THRESHOLD: float = 20.0
    RISK_MEDIUM_THRESHOLD: float = 50.0
    RISK_HIGH_THRESHOLD: float = 75.0
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()