from datetime import datetime

from pydantic import BaseModel


class DesignationCreate(BaseModel):
    designation_name: str
    designation_status: str


class DesignationUpdate(BaseModel):
    designation_name: str | None = None
    designation_status: str | None = None


class DesignationResponse(BaseModel):
    id: int
    designation_name: str
    designation_status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True