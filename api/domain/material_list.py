from typing import Optional
from dataclasses import dataclass, field
from uuid import UUID


from domain.material_item import MaterialItem


@dataclass(frozen=True, slots=True)
class MaterialList:
    id: UUID = UUID(int=0)
    notes: Optional[str] = None
    materials: list[MaterialItem] = field(
        default_factory=list[MaterialItem]
    )
