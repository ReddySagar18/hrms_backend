from sqlalchemy import Column, String, DateTime
from app.db.database import Base


class Team(Base):
    __tablename__ = "teams"

    team_id = Column(String, primary_key=True)
    team_name = Column(String, nullable=False)
    department_id = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
