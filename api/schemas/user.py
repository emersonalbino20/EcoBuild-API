from pydantic import BaseModel, ConfigDict, EmailStr, field_serializer
from datetime import datetime


class CreateField(BaseModel):
    name: str
    email: EmailStr
    password_hash: str

    @field_serializer('email')
    def serialize_email(self, email: str, _info) -> str: # type: ignore
        return email.strip().lower()

    @field_serializer('name')
    def serialize_name(self, name: str, _info) -> str: # type: ignore
        return name.strip().title()

class UpdateField(BaseModel):
    name: str
    email: EmailStr
    
    @field_serializer('email')
    def serialize_email(self, email: str, _info) -> str: # type: ignore
        return email.strip().lower()

    @field_serializer('name')
    def serialize_name(self, name: str, _info) -> str: # type: ignore
        return name.strip().title()

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    def serializer_dt(self, dt: datetime, _info): # type: ignore
        return dt.strftime('%Y-%m-%dT%H:%M:%SZ')

