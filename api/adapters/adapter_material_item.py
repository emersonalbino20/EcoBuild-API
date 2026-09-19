from sqlalchemy.ext.asyncio import AsyncSession

from api.domain.ports import MaterialItemRepository
from api.domain.material_item import MaterialItem
from api.models.analysis import MaterialItemModel

class AdapterMaterialItem(MaterialItemRepository):

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_material_item(
        self, requests: list[MaterialItem]
    ) -> list[MaterialItem]:
        """Create multiple material items in a single transaction (bulk insert)."""
        if not requests:
            return []

        # 1. Instantiate all ORM models in one operation.
        db_items = [
            MaterialItemModel(
                id=item.id,
                material_list_id=item.material_list_id,
                name=item.name,
                quantity=item.quantity,
                unit=item.unit,
            )
            for item in requests
        ]

        # 2. Add the complete list to the SQLAlchemy session.
        self.db.add_all(db_items)

        # 3. Commit all items in a single transaction.
        await self.db.commit()

        # 4. Return the persisted objects.
        return [
            MaterialItem(
                id=item.id,
                material_list_id=item.material_list_id,
                name=item.name,
                quantity=item.quantity,
                unit=item.unit,
            )
            for item in db_items
        ]
