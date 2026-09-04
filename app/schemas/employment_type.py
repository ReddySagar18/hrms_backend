from datetime import datetime
from pydantic import BaseModel, ConfigDict


class EmploymentTypeCreate(BaseModel):
    employment_type_name: str
    employment_type_status: str


class EmploymentTypeResponse(BaseModel):
    id: int
    employment_type_name: str
    employment_type_status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

