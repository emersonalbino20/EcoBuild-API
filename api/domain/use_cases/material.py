from api.domain.errors import NOT_FOUND
from api.domain.material import Material
from api.domain.ports import MaterialRepository

async def get_materials_case(
    material_repo: MaterialRepository,
) -> list[Material]:

    return await material_repo.get_materials()

async def get_material_by_id_case(
    material_repo: MaterialRepository,
    id: int
) -> Material:
    
    return await material_repo.get_material_by_id(id)

async def create_material_case(
    material_repo: MaterialRepository,
    request: Material
) -> Material:

    return await material_repo.create_material(request)

async def update_material_case(
    material_repo: MaterialRepository,
    id: int,
    request: Material
) -> Material:

    is_material = await material_repo.get_material_by_id(id)

    if not is_material:
        raise NOT_FOUND(detail="Material not found")

    return await material_repo.update_material(id, request)

async def delete_material_case(
    material_repo: MaterialRepository,
    id: int
) -> None:

    is_material = await material_repo.get_material_by_id(id)

    if not is_material:
        raise NOT_FOUND(detail="Material not found")

    return await material_repo.delete_material(id)