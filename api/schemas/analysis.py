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
        ..., description="Percentual estimado de desperdício global (ex: 10.5 para 10.5%)"
    )
    total_cost: float = Field(
        ..., description="Custo total estimado dos materiais na moeda local"
    )
    co2_saved: float = Field(
        ..., description="Estimativa de CO2 economizado em kg através de escolhas sustentáveis"
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
