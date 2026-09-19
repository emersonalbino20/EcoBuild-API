import sys
from pathlib import Path
import asyncio

import httpx


root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root))

from api.schemas.material import MaterialResponse

async def fetch_available_materials() -> list[MaterialResponse]:
    """Fetch the registered materials and their costs and rates from the API."""
    async with httpx.AsyncClient() as client:
        response = await client.get('http://127.0.0.1:8000/materials/')
        response.raise_for_status()
        
        # Pydantic validates the list of dictionaries against MaterialResponse.
        data = response.json()
        return [MaterialResponse(**item) for item in data]

output = asyncio.run(fetch_available_materials())

print(output)
