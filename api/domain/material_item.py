from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class MaterialItem:
    id: UUID = UUID(int=0)
    material_list_id: UUID = UUID(int=0)
    name: str = ""
    quantity: float = 1.0
    unit: str = "kg"
