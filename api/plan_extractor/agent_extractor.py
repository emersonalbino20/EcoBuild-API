import os
import sys
import asyncio
from pathlib import Path

from dotenv import load_dotenv
from pydantic_ai import Agent, BinaryContent

root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root))

from api.plan_extractor.utils.optimizer import plant_optimizer
from api.plan_extractor.schemas.plan_data import PlanData, SYSTEM_PROMPT

load_dotenv()
os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")

agent_extractor = Agent(
        'google:gemini-3.5-flash-lite',
        output_type=PlanData,
        system_prompt=(SYSTEM_PROMPT),
    )

async def process_architectural_plan(img_path: str) -> PlanData:
    img_bytes = plant_optimizer(img_path)

    result = await agent_extractor.run([
        "Analyze this architectural floor plan and extract all structural elements into the requested schema.",
        BinaryContent(data=img_bytes, media_type="image/jpeg"),
    ])

    # Pydantic AI validates the response against PlanData before returning it in result.data.
    plant_data: PlanData = result.output
    return plant_data
