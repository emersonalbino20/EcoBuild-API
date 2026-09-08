import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pydantic_ai import Agent, BinaryContent
from pydantic_ai.models.fallback import FallbackModel

root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root))

from plan_extractor.schemas.plan_data import PlanData, SYSTEM_PROMPT

model_3_5 = 'google:gemini-3.5-flash'
model_3_5_lite = 'google:gemini-3.5-flash-lite'  
model_3_1_lite = 'google:gemini-3.1-flash-lite'      
model_3_8_lite = 'google:gemini-3.8-flash-lite'  
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
google_api_key = os.getenv("GOOGLE_API_KEY")
if google_api_key is None:
    raise RuntimeError("GOOGLE_API_KEY is not configured")
os.environ['GOOGLE_API_KEY'] = google_api_key

agent_extractor = Agent(
        fallback_model,
        output_type=PlanData,
        system_prompt=(SYSTEM_PROMPT),
    )


async def process_architectural_plan(img_path: str, format: str) -> PlanData:
    with open(img_path, "rb") as image:
        img_bytes = image.read()

    if not format:
        raise Exception("Format not set.")

    result = await agent_extractor.run([
        "Analyze this architectural floor plan and extract all structural elements into the requested schema.",
        BinaryContent(data=img_bytes, media_type=format),
    ])

    return result.output
