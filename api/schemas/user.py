import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from api.utils.security import generate_pass_hash

class CreateField(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, examples=["John"])
    email: str = Field(..., min_length=5, max_length=100, examples=["john@example.com"], pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    password_hash: str = Field(..., min_length=8, max_length=200, examples=["Password123"], exclude=True)

    @field_serializer('email')
    def serialize_email(self, email: str) -> str:
        return email.strip().lower()

    @field_serializer('name')
    def serialize_name(self, name: str) -> str:
        return name.strip().title()

    @field_serializer('password_hash')
    def serialize_password_hash(self, password_hash: str) -> str:
        """Ensure password has at least one uppercase letter, one lowercase letter, and one number."""
        if not re.search(r'[A-Z]', password_hash):
            raise ValueError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', password_hash):
            raise ValueError('Password must contain at least one lowercase letter.')
        if not re.search(r'\d', password_hash):
            raise ValueError('Password must contain at least one number.')
        return generate_pass_hash(password_hash)


class UpdateField(CreateField):
    pass

class UserResponse(CreateField):
    id: int = Field(..., gt=0, examples=[1])
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    def serializer_dt(self, dt: datetime):
        return dt.strftime('%Y-%m-%dT%H:%M:%SZ')

