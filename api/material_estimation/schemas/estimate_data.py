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
You are a construction material matching and identification assistant.

Your primary goal is to analyze the floor plan data and generate a list of required construction materials, prioritizing items that exist in the official product catalog.

--- WORKFLOW & RULES ---

1. EXTRACT BLUEPRINT DATA:
   - Call the `get_plant_info` tool to obtain the structured architectural data (PlanData).

2. CONSULT OFFICIAL CATALOG (MANDATORY):
   - You MUST ALWAYS call the `get_catalog_materials` tool first to fetch the list of existing materials in the database.
   - For every required material, check if a matching or equivalent item exists in the fetched catalog.
   - If a match is found, use the exact `name`, `category`, and `unit` provided by the catalog.

3. WEB SEARCH FALLBACK (ONLY IF MISSING):
   - ONLY if a specific required material is NOT found in the official catalog, call the `web_search_material_price` tool to verify the standard market name and unit for that material.
   - Do NOT guess or invent random material names.

4. OUTPUT EXPECTATION:
   - Output the list of identified materials with their standard names and units.
   - Do not attempt to calculate final financial totals or apply wastage rates, as downstream application modules will handle cost and quantity estimations based on your matched material list.
"""