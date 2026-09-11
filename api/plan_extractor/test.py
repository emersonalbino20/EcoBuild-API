import sys
from pathlib import Path
import asyncio

import httpx


root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root))

from api.schemas.material import MaterialResponse

async def fetch_available_materials() -> list[MaterialResponse]:
    """Busca a lista de materiais cadastrados e seus custos/taxas na API local."""
    async with httpx.AsyncClient() as client:
        response = await client.get('http://127.0.0.1:8000/materials/')
        response.raise_for_status()
        
        # O Pydantic valida a lista de dicionários automaticamente para o modelo MaterialResponse
        data = response.json()
        return [MaterialResponse(**item) for item in data]

output = asyncio.run(fetch_available_materials())

print(output)
