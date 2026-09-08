from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

class CreateField(BaseModel):
    name: str = Field(..., min_length=4, max_length=50, examples=["Banco Bai"])
    location: str = Field(..., min_length=8, max_length=50, examples=["street, city"])

class UpdateField(BaseModel):
    name: str = Field(..., min_length=4, max_digits=50, examples=["Banco Bai"])
    location: str = Field(..., min_length=8, max_length=50, examples=["street, city"])

class OrganizationResponse(CreateField):
    id: int = Field(..., gt=0, examples=[1])
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    def serializer_dt(self, dt: datetime):
        return dt.strftime('%Y-%m-%dT%H:%M:%SZ')
