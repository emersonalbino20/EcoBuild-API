from pydantic import BaseModel, Field

class MaterialItem(BaseModel):
    name: str = Field(
        ...,
        description="Name of the construction material (e.g., 'Cimento (50kg)', 'Tijolo de 6 furos', 'Areia fina', 'Aço CA-50 10mm').",
    )
    quantity: float = Field(
        ...,
        gt=0,
        description="Estimated quantity required for the construction project.",
    )
    unit: str = Field(
        ...,
        description="Unit of measurement for the material (e.g., 'saco', 'm³', 'unidade', 'kg', 'm²').",
    )


class MaterialList(BaseModel):
    materials: list[MaterialItem] = Field(
        default_factory=list,
        description="Comprehensive list of estimated raw materials based on architectural quantities.",
    )
    notes: str | None = Field(
        default=None,
        description="Brief engineering technical note or observations about the estimate.",
    )

SYSTEM_PROMPT = """
You are an expert civil engineering cost estimator.
Your job is to generate a full material estimate based on architectural floor plans.
ALWAYS call the `get_plant_info` tool first to retrieve the structured plan data (PlanData) before calculating quantities.
"""
