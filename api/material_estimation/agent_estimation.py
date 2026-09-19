from dataclasses import dataclass

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.fallback import FallbackModel

from api.config import require_google_api_key, settings
from api.material_estimation.schemas.estimate_data import MaterialList, SYSTEM_PROMPT
from api.material_estimation.utils.fetch import fetch_available_materials
from api.plan_extractor.agent_extractor import PlanData, process_architectural_plan
from api.schemas.material import MaterialResponse

model_3_5 = 'google:gemini-3.5-flash'
model_3_5_lite = 'google:gemini-3.5-flash-lite'  
model_3_1_lite = 'google:gemini-3.1-flash-lite'      
model_3_8_lite = 'google:gemini-3.8-flash-lite'  
model_3_6_lite = 'google:gemini-3.6-flash-lite'             
model_3_7_lite = 'google:gemini-3.7-flash-lite'
model_3_6 = 'google:gemini-3.6-flash'
model_3_lite = 'google:gemini-3-flash-lite'            

# Use a fallback model for provider resilience.
fallback_model = FallbackModel(
    model_3_6,
    model_3_5,
    model_3_5_lite,
    model_3_1_lite,
    model_3_8_lite,
    model_3_7_lite,
    model_3_lite
)

load_dotenv()


@dataclass
class EstimationDeps:
    file_path: Path
    format: str


google_api_key = require_google_api_key()
os.environ["GOOGLE_API_KEY"] = google_api_key

agent_estimation: Agent[EstimationDeps, MaterialList] = Agent(
        fallback_model,
        output_type=MaterialList,
        system_prompt=(SYSTEM_PROMPT),
    )

@agent_estimation.tool
async def get_plan_info(ctx: RunContext[EstimationDeps]) -> PlanData:
    img_path: Path = ctx.deps.file_path
    format: str = ctx.deps.format

    print("=== GET PLAN INFO ===", flush=True)
    print(f"img_path: {img_path}", flush=True)
    print(f"exists: {img_path.exists()}", flush=True)

    if not img_path.exists():
        raise FileNotFoundError(
            f"Architectural plan file not found: {img_path}"
        )

    return  await process_architectural_plan(str(img_path), format)

@agent_estimation.tool_plain
async def get_catalog_materials() -> list[MaterialResponse]:
    """Fetches the official catalog of available construction materials, including prices, currency, waste rates, and specs."""
    materials_url = f"{settings.API_BASE_URL.rstrip('/')}/materials/"
    materials = await fetch_available_materials('https://ecobuild-ai.onrender.com/materials/')
    return materials


async def get_estimation(file_path: str, format: str) -> MaterialList:
    print("=== GET ESTIMATION ===", flush=True)
    print(f"file_path: {file_path}", flush=True)

    path_obj = Path(file_path)

    prompt = (
        "You are a professional construction cost estimator. Perform a complete material estimation:\n"
        "1. First, call the plan information extraction tool to analyze the architectural floor plan.\n"
        "2. Call `get_catalog_materials` to retrieve the official catalog containing exact material names, units, and prices.\n"
        "3. Match every estimated item exclusively against an item in the retrieved catalog.\n"
        "4. Copy the exact `price` and `unit` from the matched catalog item into each `MaterialItem`.\n"
        "5. Calculate the `total_cost` as the sum of (quantity * unit price) for all materials."
    )

    result = await agent_estimation.run(
    prompt, deps=EstimationDeps(file_path=path_obj, format=format)
)

    output: MaterialList = result.output

    recalculated_total = sum(item.quantity * item.price for item in output.materials)
    output.total_cost = round(recalculated_total, 2)

    return output
