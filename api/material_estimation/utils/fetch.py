import httpx

from api.schemas.material import MaterialResponse

async def fetch_available_materials(url: str) -> list[MaterialResponse]:
    """Busca a lista de materiais cadastrados e seus custos/taxas na API local."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        
        # O Pydantic valida a lista de dicionários automaticamente para o modelo MaterialResponse
        data = response.json()
        return [MaterialResponse(**item) for item in data]
