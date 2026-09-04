from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True, slots=True)
class Material:
    id: int = 0
    name: str = ""
    category: str = ""
    unit: str = ""
    price: float = 0.0
    currency: str = "AOA"
    waste_rate: float = 0.0
    co2_factor: float = 0.0
    source: str = "local_database"
    created_at: datetime | None = None
    updated_at: datetime | None = None