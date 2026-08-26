from datetime import datetime
from pydantic import BaseModel


class TeamCreate(BaseModel):
    team_id: str
    team_name: str
    department_id: str
    status: str


class TeamResponse(BaseModel):
    team_id: str
    team_name: str
    department_id: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
class TeamUpdate(BaseModel):
    team_name: str | None = None
    status: str | None = None