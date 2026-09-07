from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID



@dataclass(slots=True)
class MaterialItemDomain:
    name: str
    quantity: float
    unit: str
    id: Optional[UUID] = None


@dataclass(slots=True)
class MaterialListDomain:
    materials: List[MaterialItemDomain]
    id: Optional[UUID] = None
    notes: Optional[str] = None

class AnalysisStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"

@dataclass(frozen=True, slots=True)
class Analysis:
    id: UUID = UUID(int=0)
    plan_id: int = 0
    parent_analysis_id: Optional[UUID] = None
    status: AnalysisStatus = AnalysisStatus.PROCESSING
    material_list_id: Optional[UUID] = None
    material_list: Optional[MaterialListDomain] = None
    created_at: datetime | None = None