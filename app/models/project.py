from sqlalchemy import Column, String, Text, DateTime
from app.db.database import Base
from sqlalchemy.orm import relationship, Mapped
from app.models.employee_project import EmployeeProject
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.employee import Employee

class Project(Base):
    __tablename__ = "projects"

    project_id = Column(String, primary_key=True)
    project_name = Column(String, nullable=False)
    project_description = Column(Text, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    employees: Mapped[list["Employee"]] = relationship(
    "Employee",
    secondary="employee_projects",
    back_populates="projects"
)