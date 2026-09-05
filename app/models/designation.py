from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column ,relationship

from app.db.database import Base
from typing import TYPE_CHECKING

class Designation(Base):
    __tablename__ = "designations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    designation_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    designation_status: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    employees: Mapped[list["Employee"]] = relationship(
    "Employee",
    back_populates="designation"
)

if TYPE_CHECKING:
    from app.models.employee import Employee