from sqlalchemy import Column, String, DateTime , ForeignKey
from app.db.database import Base


class Asset(Base):
    __tablename__ = "assets"

    asset_id = Column(String, primary_key=True)
    asset_name = Column(String, nullable=False)
    asset_category = Column(String, nullable=False)
    serial_number = Column(String, nullable=False)
    status = Column(String, nullable=False)
    employee_id = Column(
        String(20),
        ForeignKey("employees.employee_id"),
        nullable=True
    )
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)