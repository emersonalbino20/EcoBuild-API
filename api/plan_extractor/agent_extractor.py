import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pydantic_ai import Agent, BinaryContent

root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root))

from api.plan_extractor.utils.optimizer import plant_optimizer
from api.plan_extractor.schemas.plan_data import PlanData, SYSTEM_PROMPT

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
if google_api_key is None:
    raise RuntimeError("GOOGLE_API_KEY is not configured")
os.environ['GOOGLE_API_KEY'] = google_api_key

agent_extractor = Agent(
        'google:gemini-3.5-flash',
        output_type=PlanData,
        system_prompt=(SYSTEM_PROMPT),
    )

async def process_architectural_plan(img_path: str) -> PlanData:
    img_bytes = plant_optimizer(img_path)

    try:
        result = await agent_extractor.run([
            "Analyze this architectural floor plan and extract all structural elements into the requested schema.",
            BinaryContent(data=img_bytes, media_type="image/jpeg"),
        ])
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Pydantic AI validates the response against PlanData before returning it in result.data.
    plant_data: PlanData = result.output
    return plant_data
