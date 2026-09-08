from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CreateField(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=50)
    unit: str = Field(min_length=1, max_length=20)

    price: Decimal = Field(
        ge=0,
        decimal_places=2,
    )

    currency: str = Field(
        default="AOA",
        min_length=3,
        max_length=3,
    )

    waste_rate: Decimal = Field(
        ge=0,
        le=1,
        decimal_places=4,
    )

    co2_factor: Decimal = Field(
        ge=0,
        decimal_places=6,
    )

    source: str | None = Field(
        default=None,
        max_length=255,
    )


class UpdateField(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    category: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    unit: str | None = Field(
        default=None,
        min_length=1,
        max_length=20,
    )

    price: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=2,
    )

    currency: str | None = Field(
        default=None,
        min_length=3,
        max_length=3,
    )

    waste_rate: Decimal | None = Field(
        default=None,
        ge=0,
        le=1,
        decimal_places=4,
    )

    co2_factor: Decimal | None = Field(
        default=None,
        ge=0,
        decimal_places=6,
    )

    source: str | None = Field(
        default=None,
        max_length=255,
    )


class MaterialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
    unit: str
    price: Decimal
    currency: str
    waste_rate: Decimal
    co2_factor: Decimal
    source: str | None

    created_at: datetime
    updated_at: datetime