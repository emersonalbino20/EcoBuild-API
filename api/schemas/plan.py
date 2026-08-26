from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

class CreateField(BaseModel):
    organization_id: int = Field(..., gt=0)

class PlanResponse(CreateField):
    id: int
    storage_reference: str
    format: str
    size: int    
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

    def serializer_dt(self, dt: datetime,):
        return dt.strftime('%Y-%m-%dT%H:%M:%SZ')