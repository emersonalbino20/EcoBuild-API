from api.domain.material_list import MaterialList
from api.domain.ports import MaterialListRepository

async def create_material_list_case(
    material_repo: MaterialListRepository,
    request: MaterialList
) -> MaterialList:

    return await material_repo.create_material_list(request)
