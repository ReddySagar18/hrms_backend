from datetime import datetime
from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    department_id: str
    department_name: str
    status: str


class DepartmentResponse(BaseModel):
    department_id: str
    department_name: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
class DepartmentUpdate(BaseModel):
    department_name: str | None = None
    status: str | None = None