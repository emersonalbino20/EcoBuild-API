from dataclasses import dataclass

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.fallback import FallbackModel

from .schemas.estimate_data import MaterialList, SYSTEM_PROMPT
from .utils.fetch import fetch_available_materials
from plan_extractor.agent_extractor import process_architectural_plan, PlanData
from schemas.material import MaterialResponse

model_3_5 = 'google:gemini-3.5-flash'
model_3_5_lite = 'google:gemini-3.5-flash-lite'  
model_3_1_lite = 'google:gemini-3.1-flash-lite'      
model_3_8_lite = 'google:gemini-3.8-flash-lite'  
model_3_6_lite = 'google:gemini-3.6-flash-lite'             
model_3_7_lite = 'google:gemini-3.7-flash-lite'
model_3_6 = 'google:gemini-3.6-flash'
model_3_lite = 'google:gemini-3-flash-lite'            

# 2. Encapsular no FallbackModel
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

google_api_key = os.getenv("GOOGLE_API_KEY")
if google_api_key is None:
    raise RuntimeError("GOOGLE_API_KEY is not set")
os.environ['GOOGLE_API_KEY'] = google_api_key

agent_estimation: Agent[EstimationDeps, MaterialList] = Agent(
        fallback_model,
        output_type=MaterialList,
        system_prompt=(SYSTEM_PROMPT),
    )

@agent_estimation.tool
async def get_plant_info(ctx: RunContext[EstimationDeps]) -> PlanData:
    img_path: Path = ctx.deps.file_path
    format: str = ctx.deps.format

    if not img_path.exists():
        raise FileNotFoundError(
            f"Arquivo de planta não localizado em: {img_path}"
        )

    return  await process_architectural_plan(str(img_path), format)

@agent_estimation.tool_plain
async def get_catalog_materials() -> list[MaterialResponse]:
    """Fetches the official catalog of available construction materials, including prices, currency, waste rates, and specs."""
    materials = await fetch_available_materials('http://127.0.0.1:8000/materials/')
    return materials


async def get_estimation(file_path: str, format: str) -> MaterialList:
    path_obj = Path(file_path)

    prompt = (
        "Calculate the full material estimate for the architectural floor plan "
        "by extracting its data first using the available plant info tool."
    )

    result = await agent_estimation.run(
        prompt, deps=EstimationDeps(file_path=path_obj, format=format)
    )

    return result.output
