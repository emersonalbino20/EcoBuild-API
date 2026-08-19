from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.Base import Base

if TYPE_CHECKING:
    from .organization import OrganizationModel


class UserModel(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
                         DateTime(timezone=True),
                         default=lambda: datetime.now()
                         )
    updated_at: Mapped[datetime] = mapped_column(
                         DateTime(timezone=True),
                         default=lambda: datetime.now(),
                         onupdate=lambda: datetime.now()
                         )

    orgs: Mapped[list["OrganizationModel"]] = relationship(
					back_populates="user",
					cascade="all, delete-orphan")
