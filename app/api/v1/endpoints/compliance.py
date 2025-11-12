from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import StreamingResponse
from typing import Optional
import io
import pandas as pd
from datetime import datetime

from app.models.cargo import CargoListRequest
from app.models.compliance import ComplianceResponse
from app.services.compliance_service import ComplianceService
from app.services.recommendation_service import RecommendationService

router = APIRouter(prefix="/compliance", tags=["Compliance Assessment"])


def get_compliance_service() -> ComplianceService:
    return ComplianceService()


def get_recommendation_service() -> RecommendationService:
    return RecommendationService()


@router.post("/assess", response_model=ComplianceResponse)
async def assess_cargo(
    request: CargoListRequest,
    detailed: bool = Query(False, description="Include class details"),
    compliance_service: ComplianceService = Depends(get_compliance_service),
    recommendation_service: RecommendationService = Depends(get_recommendation_service)
):
    """
    🎯 MAIN ENDPOINT - Assess cargo compatibility
    
    **This is your main program logic output!**
    
    Returns:
    - Violations: Prohibited combinations (segregation code 3-4)
    - Warnings: Restricted combinations (segregation code 1-2)
    - Compliant: Safe combinations (segregation code X)
    - Risk Score: 0-100 overall risk assessment
    - Recommendations: Actionable steps to resolve issues
    """
    try:
        # 🔍 MAIN LOGIC EXECUTION
        if detailed:
            assessment = compliance_service.get_detailed_analysis(request.cargo_items)
        else:
            assessment = compliance_service.assess_cargo_compatibility(request.cargo_items)
        
        # 📋 Generate recommendations
        recommendations = recommendation_service.generate_recommendations(
            assessment, request.cargo_items
        )
        
        # 📊 Build summary
        summary = {
            "total_items": len(request.cargo_items),
            "total_comparisons": assessment['total_comparisons'],
            "compliant_count": len(assessment['compliant']),
            "warnings_count": len(assessment['warnings']),
            "violations_count": len(assessment['violations']),
            "overall_status": "FAIL" if assessment['violations'] else "PASS",
            "timestamp": datetime.now().isoformat()
        }
        
        return ComplianceResponse(
            assessment=assessment,
            recommendations=recommendations,
            summary=summary
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Assessment failed: {str(e)}")


@router.post("/assess/export-csv")
async def export_assessment_csv(
    request: CargoListRequest,
    compliance_service: ComplianceService = Depends(get_compliance_service)
):
    """
    📄 Export assessment results as CSV (like your Streamlit export button)
    """
    try:
        assessment = compliance_service.assess_cargo_compatibility(request.cargo_items)
        
        # Prepare export data
        export_data = []
        
        for v in assessment['violations']:
            export_data.append({
                'Type': 'VIOLATION',
                'Cargo_1': v['cargo1']['un_number'],
                'Name_1': v['cargo1']['name'],
                'Class_1': v['cargo1']['class_id'],
                'Cargo_2': v['cargo2']['un_number'],
                'Name_2': v['cargo2']['name'],
                'Class_2': v['cargo2']['class_id'],
                'Segregation_Code': v['rule']['segregation_code'],
                'Rule': v['rule']['segregation_rule'],
                'Risk_Penalty': v['rule']['risk_penalty']
            })
        
        for w in assessment['warnings']:
            export_data.append({
                'Type': 'WARNING',
                'Cargo_1': w['cargo1']['un_number'],
                'Name_1': w['cargo1']['name'],
                'Class_1': w['cargo1']['class_id'],
                'Cargo_2': w['cargo2']['un_number'],
                'Name_2': w['cargo2']['name'],
                'Class_2': w['cargo2']['class_id'],
                'Segregation_Code': w['rule']['segregation_code'],
                'Rule': w['rule']['segregation_rule'],
                'Risk_Penalty': w['rule']['risk_penalty']
            })
        
        df_export = pd.DataFrame(export_data)
        
        # Create CSV in memory
        output = io.StringIO()
        df_export.to_csv(output, index=False)
        output.seek(0)
        
        filename = f"dg_compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode()),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")