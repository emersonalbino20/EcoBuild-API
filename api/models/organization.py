from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.Base import Base

from TYPE_CHECKING:
    from models.user import UserModel

class OrganizationModel(Base):
    __tablename__ = "organizations"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str]
    location: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
                         DateTime(timezone=True),
                         default=lambda: datetime.now()
                         )
    updated_at: Mapped[datetime] = mapped_column(
                         DateTime(timezone=True),
                         default=lambda: datetime.now(),
                         onupdate=lambda: datetime.now()
                         )
    
    user: Mapped["UserModel"] = relationship(back_populates="orgs")
