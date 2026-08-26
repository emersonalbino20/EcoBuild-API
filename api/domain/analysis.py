from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class AnalysisStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"

@dataclass(frozen=True, slots=True)
class Analysis:
    id: int = 0
    plan_id: int = 0
    parent_analysis_id: int = 0
    version: int = 0
    estimated_cost: int = 0
    waste_percentage: int = 0
    co2_saved: int = 0
    status: AnalysisStatus = AnalysisStatus.PROCESSING
    created_at: datetime | None = None