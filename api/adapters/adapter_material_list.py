from sqlalchemy.ext.asyncio import AsyncSession

from domain.ports import MaterialListRepository
from domain.material_list import MaterialList
from models.analysis import MaterialListModel

class AdapterMaterialList(MaterialListRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_material_list(self, request: MaterialList) -> MaterialList:
        db_material_list = MaterialListModel(
            id=request.id,
            notes=request.notes,
        )
        self.db.add(db_material_list)
        await self.db.commit()
        await self.db.refresh(db_material_list)

        return MaterialList(
            db_material_list.id,
            db_material_list.notes,
        )
