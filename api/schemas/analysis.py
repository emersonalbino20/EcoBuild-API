from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from api.domain.analysis import AnalysisStatus

from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class CreateField(BaseModel):
    plan_id: int = Field(..., gt=0)

class MaterialItemResponse(BaseModel):
    id: UUID
    name: str
    quantity: float
    unit: str
    price: float

    model_config = ConfigDict(from_attributes=True)

class MaterialListResponse(BaseModel):
    id: UUID
    notes: Optional[str] = None
    waste_percentage: float = Field(
        ..., description="Estimated overall waste percentage (for example, 10.5 for 10.5%)."
    )
    total_cost: float = Field(
        ..., description="Estimated total material cost in the configured currency."
    )
    co2_saved: float = Field(
        ..., description="Estimated CO2 savings in kilograms from sustainable material choices."
    )
    materials: List[MaterialItemResponse] = []

    model_config = ConfigDict(from_attributes=True)

class AnalysisResponse(CreateField):
    id: UUID
    plan_id: int
    parent_analysis_id: Optional[UUID] = None
    status: AnalysisStatus
    result: Optional[MaterialListResponse] = Field(
            default=None, alias="material_list"
        )
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    def serializer_dt(self, dt: datetime,):
        return dt.strftime('%Y-%m-%dT%H:%M:%SZ')
