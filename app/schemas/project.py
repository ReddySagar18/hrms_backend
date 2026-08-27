from datetime import datetime
from pydantic import BaseModel


class ProjectCreate(BaseModel):
    project_id: str
    project_name: str
    project_description: str
    status: str


class ProjectResponse(BaseModel):
    project_id: str
    project_name: str
    project_description: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectUpdate(BaseModel):
    project_name: str | None = None
    project_description: str | None = None
    status: str | None = None