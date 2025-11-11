from fastapi import APIRouter, HTTPException, Depends
from app.models.cargo import CargoListRequest
from app.models.compliance import ComplianceResponse
from app.services.compliance_service import ComplianceService
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/compliance", tags=["Compliance"])


def get_compliance_service() -> ComplianceService:
    return ComplianceService()


def get_recommendation_service() -> RecommendationService:
    return RecommendationService()


@router.post("/assess", response_model=ComplianceResponse)
async def assess_cargo(
    request: CargoListRequest,
    compliance_service: ComplianceService = Depends(get_compliance_service),
    recommendation_service: RecommendationService = Depends(get_recommendation_service)
):
    """
    Assess cargo compatibility and generate compliance report
    
    - **cargo_items**: List of dangerous goods (minimum 2 items)
    - Returns detailed assessment with violations, warnings, and recommendations
    """
    try:
        # Perform assessment
        assessment = compliance_service.assess_cargo_compatibility(request.cargo_items)
        
        # Generate recommendations
        recommendations = recommendation_service.generate_recommendations(
            assessment, request.cargo_items
        )
        
        # Build summary
        summary = {
            "total_items": len(request.cargo_items),
            "total_comparisons": assessment['total_comparisons'],
            "compliant_count": len(assessment['compliant']),
            "warnings_count": len(assessment['warnings']),
            "violations_count": len(assessment['violations']),
            "overall_status": "FAIL" if assessment['violations'] else "PASS"
        }
        
        return ComplianceResponse(
            assessment=assessment,
            recommendations=recommendations,
            summary=summary
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))