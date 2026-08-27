from sqlalchemy import Column, String, Text, DateTime
from app.db.database import Base


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(String, primary_key=True)
    project_name = Column(String, nullable=False)
    project_description = Column(Text, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)