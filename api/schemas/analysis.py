from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from domain.analysis import AnalysisStatus

class CreateField(BaseModel):
    plan_id: int = Field(..., gt=0)
    parent_analysis_id: int = Field(0, ge=0)

class AnalysisResponse(CreateField):
    id: int
    version: int
    estimated_cost: int
    waste_percentage: int
    co2_saved: int
    status: AnalysisStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    def serializer_dt(self, dt: datetime,):
        return dt.strftime('%Y-%m-%dT%H:%M:%SZ')