from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.team import (TeamCreate, TeamResponse, TeamUpdate)
from app.services.team_service import (
    create_team,
    get_all_teams,
    get_team_by_id,
    update_team
)
from app.dependencies.auth import require_role


router = APIRouter(
    prefix="/teams",
    tags=["Teams"]
)


@router.post("/", response_model=TeamResponse)
def create_new_team(
    team: TeamCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("HR"))
):
    return create_team(db, team)


@router.get("/", response_model=list[TeamResponse])
def get_teams(
    db: Session = Depends(get_db)
):
    return get_all_teams(db)


@router.get("/{team_id}", response_model=TeamResponse)
def get_team(
    team_id: str,
    db: Session = Depends(get_db)
):
    return get_team_by_id(db, team_id)
@router.patch(
    "/{team_id}",
    response_model=TeamResponse
)
def update_existing_team(
    team_id: str,
    team: TeamUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("HR"))
):
    return update_team(
        db,
        team_id,
        team
    )