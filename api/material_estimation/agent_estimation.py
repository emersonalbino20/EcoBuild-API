import os
import sys
import asyncio
from pathlib import Path

from dotenv import load_dotenv
from pydantic_ai import Agent

root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root))

BASE_DIR = Path(__file__).resolve().parent.parent

from schemas.estimate_data import MaterialList, SYSTEM_PROMPT
from api.material_estimation.utils.fetch import fetch_available_materials
from api.plan_extractor.agent_extractor import process_architectural_plan, PlanData
from api.schemas.material import MaterialResponse

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
if google_api_key is None:
    raise RuntimeError("GOOGLE_API_KEY is not set")
os.environ['GOOGLE_API_KEY'] = google_api_key

agent_estimation = Agent(
        'google:gemini-3.5-flash',
        output_type=MaterialList,
        system_prompt=(SYSTEM_PROMPT),
    )

@agent_estimation.tool_plain
async def get_plant_info() -> PlanData:
    img_path = BASE_DIR / "uploads" / "plant.jpeg"

    # 1. Validação de segurança antes de chamar o OpenCV
    if not img_path.exists():
        print(f"[ERRO] Imagem não encontrada no caminho absoluto: {img_path}")
        # Evite sys.exit(1) dentro de rotas/agentes para não derrubar o servidor FastAPI inteiro!
        raise FileNotFoundError(
            f"Arquivo de planta não localizado em: {img_path}"
        )

    try:
        plan_data: PlanData = await process_architectural_plan(img_path)
    except Exception as e:
        sys.exit(1)

    return plan_data

@agent_estimation.tool_plain
async def get_catalog_materials() -> list[MaterialResponse]:
    """Fetches the official catalog of available construction materials, including prices, currency, waste rates, and specs."""
    materials = await fetch_available_materials('http://127.0.0.1:8000/materials/')
    return materials

async def get_estimation() -> MaterialList:

    prompt = "Calculate the full material estimate for the current floor plan by extracting its data first."

    try:
        result = await agent_estimation.run(prompt)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    material_data: MaterialList = result.output
    return material_data

output = asyncio.run(get_estimation())

print(output)
