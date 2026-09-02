from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class AssetCreate(BaseModel):
    asset_id: str
    asset_name: str
    asset_category: str
    serial_number: str
    status: str


class AssetResponse(BaseModel):
    asset_id: str
    asset_name: str
    asset_category: str
    serial_number: str
    status: str
    employee_id: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
class AssetUpdate(BaseModel):
    asset_name: Optional[str] = None
    asset_type: Optional[str] = None
    serial_number: Optional[str] = None
    status: Optional[str] = None
class AssetAssign(BaseModel):
    employee_id: str

class AssetReplace(BaseModel):
    new_asset_id: str