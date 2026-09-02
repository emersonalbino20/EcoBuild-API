import os
import sys
import asyncio
from pathlib import Path

from dotenv import load_dotenv
from pydantic_ai import Agent, BinaryContent

root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root))

from schemas.estimate_data import MaterialList, SYSTEM_PROMPT
from api.plan_extractor.agent_extractor import process_architectural_plan, PlanData

load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")

agent_estimation = Agent(
        'google:gemini-3.5-flash-lite',
        output_type=MaterialList,
        system_prompt=(SYSTEM_PROMPT),
    )

@agent_estimation.tool_plain
async def get_plant_info() -> PlanData:
    img_path = Path('plant.jpeg')
    plan_data: PlanData = await process_architectural_plan(img_path)
    return plan_data

async def get_estimation() -> MaterialList:

    prompt = "Calculate the full material estimate for the current floor plan by extracting its data first."

    result = await agent_estimation.run(prompt)

    material_data: MaterialList = result.output
    return material_data

output = asyncio.run(get_estimation())

print(output)
