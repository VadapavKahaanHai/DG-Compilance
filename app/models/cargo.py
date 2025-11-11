from pydantic import BaseModel, Field, validator
from typing import Optional, List


class CargoItem(BaseModel):
    un_number: str = Field(..., description="UN Number (e.g., UN1090)")
    name: str = Field(..., description="Proper shipping name")
    class_id: str = Field(..., description="DG Class (e.g., 3)")
    packing_group: str = Field(..., description="Packing group (I, II, III)")
    quantity: float = Field(..., gt=0, description="Quantity in kg")
    flash_point: Optional[str] = None
    
    @validator('un_number')
    def validate_un_number(cls, v):
        if not v.startswith('UN'):
            raise ValueError('UN number must start with "UN"')
        return v.upper()


class CargoListRequest(BaseModel):
    cargo_items: List[CargoItem] = Field(..., min_items=2, description="List of cargo items (minimum 2)")


class SegregationPairRequest(BaseModel):
    class_from: str = Field(..., description="First DG class")
    class_to: str = Field(..., description="Second DG class")