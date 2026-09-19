import httpx

from api.schemas.material import MaterialResponse

async def fetch_available_materials(url: str) -> list[MaterialResponse]:
    """Fetch the registered materials and their costs and rates from the API."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        
        # Pydantic validates the list of dictionaries against MaterialResponse.
        data = response.json()
        return [MaterialResponse(**item) for item in data]
