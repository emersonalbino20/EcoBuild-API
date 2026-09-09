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
    name: str = Field(min_length=1, max_length=100, examples=["Cement"])
    category: str = Field(min_length=1, max_length=50, examples=["Concrete"])
    unit: str = Field(min_length=1, max_length=20, examples=["m²", "kg", "l"])
    price: Decimal = Field(ge=0, decimal_places=2, examples=["0.00"])
    currency: str = Field(min_length=3, max_length=3, examples=["AOA"])
    waste_rate: Decimal = Field(ge=0, le=1, decimal_places=4, examples=["0.0000"])
    co2_factor: Decimal = Field(ge=0, decimal_places=6, examples=["0.000000"])
    source: str | None = Field(default=None, max_length=255, examples=["https://example.com/materials/cement"])
    created_at: datetime
    updated_at: datetime