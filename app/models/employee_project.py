from sqlalchemy import Column, String, ForeignKey
from app.db.database import Base


class EmployeeProject(Base):
    __tablename__ = "employee_projects"

    employee_id = Column(
        String(20),
        ForeignKey("employees.employee_id"),
        primary_key=True
    )

    project_id = Column(
        String,
        ForeignKey("projects.project_id"),
        primary_key=True
    )