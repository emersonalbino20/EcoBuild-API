from datetime import datetime
from decimal import Decimal

from typing import TYPE_CHECKING
from sqlalchemy import DateTime, Numeric, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.analysis import AnalysisStatus
from db.Base import Base

if TYPE_CHECKING:
    from models.plan import PlanModel


class AnalysisModel(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(primary_key=True)

    plan_id: Mapped[int] = mapped_column(
        ForeignKey("plans.id", ondelete="CASCADE"),
        nullable=False,
    )

    parent_analysis_id: Mapped[int | None] = mapped_column(
        ForeignKey("analyses.id", ondelete="SET NULL"),
        nullable=True,
    )

    version: Mapped[int] = mapped_column(
        nullable=False,
        default=1,
    )

    estimated_cost: Mapped[Decimal | None] = mapped_column(
        Numeric(15, 2),
        nullable=True,
    )

    waste_percentage: Mapped[Decimal | None] = mapped_column(
        Numeric(5, 2),
        nullable=True,
    )

    co2_saved: Mapped[Decimal | None] = mapped_column(
        Numeric(15, 2),
        nullable=True,
    )

    status: Mapped[AnalysisStatus] = mapped_column(
        String(20),
        nullable=False,
        default=AnalysisStatus.PROCESSING,
    )

    created_at: Mapped[datetime] = mapped_column(
                         DateTime(timezone=True),
                         default=lambda: datetime.now()
                         )

    plan: Mapped["PlanModel"] = relationship(back_populates="analyses")

    parent_analysis = relationship(
        "AnalysisModel",
        remote_side=[id],
        back_populates="child_analyses",
    )

    child_analyses = relationship(
        "AnalysisModel",
        back_populates="parent_analysis",
    )