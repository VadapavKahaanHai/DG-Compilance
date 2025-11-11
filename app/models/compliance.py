from pydantic import BaseModel, Field
from typing import List, Dict, Any
from enum import Enum


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ComplianceAssessment(BaseModel):
    compliant: List[Dict[str, Any]] = Field(default_factory=list)
    warnings: List[Dict[str, Any]] = Field(default_factory=list)
    violations: List[Dict[str, Any]] = Field(default_factory=list)
    risk_score: float = Field(..., ge=0, le=100)
    risk_level: RiskLevel
    total_risk_points: float
    total_comparisons: int


class Recommendation(BaseModel):
    priority: str = Field(..., description="CRITICAL, HIGH, MEDIUM, LOW")
    action: str
    detail: str


class ComplianceResponse(BaseModel):
    assessment: ComplianceAssessment
    recommendations: List[Recommendation]
    summary: Dict[str, Any]