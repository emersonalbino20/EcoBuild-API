from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.ports import MaterialRepository
from domain.material import Material
from models.material import MaterialModel


class AdapterMaterial(MaterialRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_materials(self) -> list[Material]:
        query = select(MaterialModel)
        result = await self.db.execute(query)
        materials = result.scalars().all()

        return [
            Material(
                material.id,
                material.name,
                material.category,
                material.unit,
                material.price,
                material.currency,
                material.waste_rate,
                material.co2_factor,
                material.source,
                material.created_at,
                material.updated_at
            )
            for material in materials
        ]

    async def get_material_by_id(self, id: int) -> Material:
        query = select(MaterialModel).where(MaterialModel.id == id)
        result = await self.db.execute(query)
        material = result.scalar_one_or_none()

        return Material(
            material.id,
            material.name,
            material.category,
            material.unit,
            material.price,
            material.currency,
            material.waste_rate,
            material.co2_factor,
            material.source,
            material.created_at,
            material.updated_at
        )

    async def create_material(self, request: Material) -> Material:
        db_material = MaterialModel(
            name=request.name,
            category=request.category,
            unit=request.unit,
            price=request.price,
            currency=request.currency,
            waste_rate=request.waste_rate,
            co2_factor=request.co2_factor,
            source=request.source
        )
        self.db.add(db_material)
        await self.db.commit()
        await self.db.refresh(db_material)

        return Material(
            db_material.id,
            db_material.name,
            db_material.category,
            db_material.unit,
            db_material.price,
            db_material.currency,
            db_material.waste_rate,
            db_material.co2_factor,
            db_material.source,
            db_material.created_at,
            db_material.updated_at
        )

    async def update_material(self, id: int, request: Material) -> Material:
        query = select(MaterialModel).where(MaterialModel.id == id)
        result = await self.db.execute(query)
        db_material = result.scalar_one_or_none()

        await self.db.commit()
        await self.db.refresh(db_material)

        return Material(
            db_material.id,
            db_material.name,
            db_material.category,
            db_material.unit,
            db_material.price,
            db_material.currency,
            db_material.waste_rate,
            db_material.co2_factor,
            db_material.source,
            db_material.created_at,
            db_material.updated_at
        )

    async def delete_material(self, id: int) -> None:
        query = select(MaterialModel).where(MaterialModel.id == id)
        result = await self.db.execute(query)
        db_material = result.scalar_one_or_none()

        await self.db.delete(db_material)
        await self.db.commit()