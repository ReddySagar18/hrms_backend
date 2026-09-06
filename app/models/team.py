from sqlalchemy import Column, String, DateTime
from app.db.database import Base
from sqlalchemy.orm import Mapped, relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.employee import Employee
class Team(Base):
    __tablename__ = "teams"

    team_id = Column(String, primary_key=True)
    team_name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    employees: Mapped[list["Employee"]] = relationship(
    "Employee",
    back_populates="team"
)