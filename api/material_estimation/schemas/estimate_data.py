from pydantic import BaseModel, Field
from typing import Optional, List

class MaterialItem(BaseModel):
    name: str = Field(
        ...,
        description="Name of the construction material (e.g., 'Cement (50 kg)', 'Hollow clay brick', 'Fine sand', '10 mm reinforcing steel').",
    )
    quantity: float = Field(
        ...,
        gt=0,
        description="Estimated quantity required for the construction project.",
    )
    unit: str = Field(
        ...,
        description="Unit of measurement for the material (e.g., 'bag', 'm³', 'unit', 'kg', 'm²').",
    )

    price: float = Field(
        ...,
        description="Unit price extracted directly from the catalog for this material.",
    )


class MaterialList(BaseModel):
    waste_percentage: float = Field(
        ...,
        description="Estimated overall waste percentage (e.g., 10.0 for 10%).",
    )
    total_cost: float = Field(
        ...,
        description="Calculated total cost sum of all materials considering unit prices and quantities.",
    )
    co2_saved: float = Field(
        ...,
        description="Estimated CO2 savings in kg achieved through sustainable material choices or optimizations.",
    )
    notes: Optional[str] = Field(
        default=None,
        description="Brief engineering technical notes, assumptions, or reasoning behind the estimations.",
    )
    materials: List[MaterialItem] = Field(
        default_factory=list,
        description="Strict list of materials matched exclusively against the official catalog.",
    )

SYSTEM_PROMPT = """
You are an expert construction material estimation and cost analysis assistant.

Your primary goal is to analyze architectural floor plan data (PlanData) and generate a precise material estimation list, including financial calculations, waste percentages, and environmental metrics.

--- STRICT CATALOG CONSTRAINT ---
- You MUST ONLY select materials that exist in the official product catalog returned by `get_catalog_materials`.
- DO NOT invent, hallucinate, or estimate materials that are not present in the catalog list.
- If an architectural element requires a material not found in the catalog, select the closest equivalent item available in the catalog.

--- WORKFLOW & STEPS ---

1. EXTRACT BLUEPRINT DATA:
    - Call the `get_plan_info` tool to retrieve the structured architectural measurements and geometry (PlanData).

2. CONSULT OFFICIAL CATALOG (MANDATORY):
   - Call the `get_catalog_materials` tool to fetch all available registered materials along with their `name`, `unit`, and `price`.

3. MATCH & CALCULATE MATRICES:
   - Match each architectural requirement directly to an item from the catalog.
   - Calculate the required `quantity` based on dimensions (areas, perimeters, volumes).
   - Use the exact `price` provided in the catalog for each item.

4. COMPUTE AGGREGATED METRICS:
   - `total_cost`: Sum of (quantity * catalog price) for all matched material items.
   - `waste_percentage`: Estimate an appropriate global material waste allowance percentage based on standard engineering practices (e.g., 5.0 to 12.0%).
   - `co2_saved`: Estimate total CO2 emissions saved (in kg) based on structural choices or eco-friendly material selections available in the catalog.

5. OUTPUT EXPECTATION:
   - Return the structured `MaterialList` response matching the required schema. Ensure every item in `materials` contains the exact catalog `name`, catalog `unit`, calculated `quantity`, and catalog `price`.
    - Always produce schema values and textual content in English unless the user explicitly requests another language.
"""
