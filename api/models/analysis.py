from datetime import datetime
from uuid import uuid4, UUID

from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import DateTime, Float, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from api.domain.analysis import AnalysisStatus
from api.db.Base import Base

if TYPE_CHECKING:
    from models.plan import PlanModel

class AnalysisModel(Base):
    __tablename__ = "analyses"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )

    plan_id: Mapped[int] = mapped_column(
        ForeignKey("plans.id", ondelete="CASCADE"), nullable=False
    )

    parent_analysis_id: Mapped[Optional[UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("analyses.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Chave Estrangeira OPCIONAL (Permite salvar instantaneamente como PROCESSING)
    material_list_id: Mapped[Optional[UUID]] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("material_lists.id", ondelete="SET NULL"),
        nullable=True,
    )

    status: Mapped[AnalysisStatus] = mapped_column(
        String(20), nullable=False, default=AnalysisStatus.PROCESSING
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(),
    )

    # Relacionamentos
    plan: Mapped["PlanModel"] = relationship(back_populates="analyses")

    material_list: Mapped[Optional["MaterialListModel"]] = relationship(
        "MaterialListModel",
        back_populates="analysis",
        cascade="all, delete-orphan",
        single_parent=True,
    )

    parent_analysis: Mapped[Optional["AnalysisModel"]] = relationship(
        "AnalysisModel", remote_side=[id], back_populates="child_analyses"
    )

    child_analyses: Mapped[List["AnalysisModel"]] = relationship(
        "AnalysisModel", back_populates="parent_analysis"
    )


class MaterialListModel(Base):
    __tablename__ = "material_lists"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )

    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relacionamento 1:1 com a análise
    analysis: Mapped[Optional["AnalysisModel"]] = relationship(
        "AnalysisModel", back_populates="material_list"
    )

    # Relacionamento 1:N com os itens individuais
    materials: Mapped[List["MaterialItemModel"]] = relationship(
        "MaterialItemModel",
        back_populates="material_list",
        cascade="all, delete-orphan",
    )


class MaterialItemModel(Base):
    __tablename__ = "material_items"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )

    material_list_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("material_lists.id", ondelete="CASCADE"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(50), nullable=False)

    material_list: Mapped["MaterialListModel"] = relationship(
        "MaterialListModel", back_populates="materials"
    )