from sqlalchemy import Column, String, DateTime 
from app.db.database import Base
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from app.models.employee import Employee

class Department(Base):
    __tablename__ = "departments"
    employees: Mapped[list["Employee"]] = relationship(
    "Employee",
    back_populates="department"
)
    department_id = Column(String, primary_key=True)
    department_name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False) 