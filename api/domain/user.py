from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True, slots=True)
class User:
    id: int | None = None
    name: str | None = None
    email: str | None = None
    password_hash: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
