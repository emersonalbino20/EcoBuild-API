from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True, slots=True)
class Plan:
    id: int = 0
    organization_id: int = 0
    storage_reference: str = ""
    format: str = ""
    size: int = 0
    created_at: datetime | None = None
