from sqlalchemy import Column, String, DateTime
from app.db.database import Base


class Department(Base):
    __tablename__ = "departments"

    department_id = Column(String, primary_key=True)
    department_name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False) 