from domain.material_item import MaterialItem
from domain.ports import MaterialItemRepository

async def create_material_item_case(
    material_repo: MaterialItemRepository, requests: list[MaterialItem]
) -> list[MaterialItem]:

    return await material_repo.create_material_item(requests)
