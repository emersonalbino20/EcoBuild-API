from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True, slots=True)
class Organization:
    id: int | None = None
    user_id: int | None = None
    name: str | None = None
    location: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
