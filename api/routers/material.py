from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.adapter_material import AdapterMaterial
from domain.use_cases.material import (create_material_case,
                                        get_materials_case,
                                        delete_material_case,
                                        update_material_case)
from db.Session import get_db
from domain.material import Material
from schemas.material import CreateField, UpdateField, MaterialResponse
from utils.response_util import to_response

router = APIRouter(
    prefix="/materials",
    tags=["material"]
    )

@router.get("/", response_model=list[MaterialResponse])
async def get_materials(db: AsyncSession = Depends(get_db)) -> list[MaterialResponse]:
    adapter = AdapterMaterial(db)
    result = await get_materials_case(adapter)

    return [
      to_response(MaterialResponse, material)
      for material in result
    ]

@router.post(
  "/",
  response_model=MaterialResponse,
  status_code=status.HTTP_201_CREATED
)
async def create_material(
    material: CreateField,
    db: AsyncSession = Depends(get_db)
) -> MaterialResponse:
    adapter = AdapterMaterial(db)
    request = Material(
        name=material.name,
        category=material.category,
        unit=material.unit,
        price=material.price,
        currency=material.currency,
        waste_rate=material.waste_rate,
        co2_factor=material.co2_factor,
        source=material.source
    )
    result = await create_material_case(adapter, request)

    return to_response(MaterialResponse, result)

@router.put("/{id}", response_model=MaterialResponse)
async def update_material(
    id: int,
    material: UpdateField,
    db: AsyncSession = Depends(get_db)
) -> MaterialResponse:
    adapter = AdapterMaterial(db)
    request = Material(
        name=material.name,
        category=material.category,
        unit=material.unit,
        price=material.price,
        currency=material.currency,
        waste_rate=material.waste_rate,
        co2_factor=material.co2_factor,
        source=material.source
    )
    result = await update_material_case(adapter, id, request)

    return to_response(MaterialResponse, result)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_material(id: int, db: AsyncSession = Depends(get_db)) -> None:
    adapter = AdapterMaterial(db)
    await delete_material_case(adapter, id)