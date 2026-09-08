from sqlalchemy.ext.asyncio import AsyncSession

from domain.ports import MaterialItemRepository
from domain.material_item import MaterialItem
from models.analysis import MaterialItemModel

class AdapterMaterialItem(MaterialItemRepository):

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_material_item(
        self, requests: list[MaterialItem]
    ) -> list[MaterialItem]:
        """Cria múltiplos itens de materiais em uma única transação (Bulk Insert)."""
        if not requests:
            return []

        # 1. Instancia todos os modelos ORM de uma só vez
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

        # 2. Adiciona a lista inteira à sessão do SQLAlchemy
        self.db.add_all(db_items)

        # 3. Executa o commit de todos os itens em uma única transação
        await self.db.commit()

        # 4. Retorna os objetos persistidos
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
