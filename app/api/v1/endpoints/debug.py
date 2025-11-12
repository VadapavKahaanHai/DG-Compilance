from fastapi import APIRouter, Depends
from app.repositories.segregation_repository import SegregationRepository
from app.repositories.goods_repository import GoodsRepository

router = APIRouter(prefix="/debug", tags=["Debug"])


@router.get("/segregation-rules")
async def list_all_rules(repo: SegregationRepository = Depends(lambda: SegregationRepository())):
    """List all segregation rules for debugging"""
    return {
        "total_rules": len(repo.df),
        "rules": repo.get_all_rules()
    }


@router.get("/check-rule/{class1}/{class2}")
async def check_specific_rule(
    class1: str,
    class2: str,
    repo: SegregationRepository = Depends(lambda: SegregationRepository())
):
    """Check a specific segregation rule"""
    rule = repo.get_rule(class1, class2)
    return {
        "class_from": class1,
        "class_to": class2,
        "rule": rule
    }


@router.get("/test-assessment")
async def test_assessment():
    """Test with known cargo items"""
    from app.services.compliance_service import ComplianceService
    from app.models.cargo import CargoItem
    
    cargo_items = [
        CargoItem(
            un_number="UN1090",
            name="Acetone",
            class_id="3.0",
            packing_group="II",
            quantity=5000
        ),
        CargoItem(
            un_number="UN1428",
            name="Sodium",
            class_id="4.3",
            packing_group="I",
            quantity=2000
        ),
        CargoItem(
            un_number="UN1005",
            name="Ammonia",
            class_id="2.3",
            packing_group="N/A",
            quantity=3000
        )
    ]
    
    service = ComplianceService()
    result = service.assess_cargo_compatibility(cargo_items)
    
    return result


# In app/api/v1/endpoints/debug.py

@router.get("/check-csv-file")
async def check_csv_file():
    """Check which CSV file is being loaded and its contents"""
    import os
    from app.core.config import settings
    
    file_path = settings.SEGREGATION_RULES_FILE
    
    # Check if file exists
    exists = os.path.exists(file_path)
    
    # Get absolute path
    abs_path = os.path.abspath(file_path)
    
    # Read raw file
    if exists:
        with open(file_path, 'r') as f:
            first_20_lines = [f.readline().strip() for _ in range(20)]
    else:
        first_20_lines = []
    
    # Check for class '3' specifically
    class_3_lines = []
    if exists:
        with open(file_path, 'r') as f:
            for i, line in enumerate(f):
                if line.startswith('3,') or ',3,' in line:
                    class_3_lines.append(f"Line {i+1}: {line.strip()}")
    
    return {
        "file_path": file_path,
        "absolute_path": abs_path,
        "exists": exists,
        "first_20_lines": first_20_lines,
        "class_3_lines": class_3_lines,
        "total_class_3_lines": len(class_3_lines)
    }