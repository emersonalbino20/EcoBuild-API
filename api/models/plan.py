from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db.Base import Base

if TYPE_CHECKING:
    from models.organization import OrganizationModel
    from models.analysis import AnalysisModel

class PlanModel(Base):
    __tablename__ = "plans"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    storage_reference: Mapped[str]
    format: Mapped[str]
    size: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
                         DateTime(timezone=True),
                         default=lambda: datetime.now()
                         )
    
    organization: Mapped["OrganizationModel"] = relationship(back_populates="plans")

    analyses: Mapped["AnalysisModel"] = relationship(
                                                    back_populates="plan",
                                                    cascade="all, delete-orphan")
