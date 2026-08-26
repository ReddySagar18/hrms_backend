from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.team import Team
from app.schemas.team import TeamCreate, TeamUpdate


def create_team(db: Session, team: TeamCreate):

    db_team = Team(
        team_id=team.team_id,
        team_name=team.team_name,
        department_id=team.department_id,
        status=team.status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    try:
        db.add(db_team)
        db.commit()
        db.refresh(db_team)

        return db_team

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Team with this ID already exists."
        )
    #get all teams 
def get_all_teams(db: Session):

    return db.query(Team).all()

    #get one team 
def get_team_by_id(db: Session, team_id: str):

    team = (
        db.query(Team)
        .filter(Team.team_id == team_id)
        .first()
    )

    if team is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )

    return team
#update team
def update_team(
    db: Session,
    team_id: str,
    team: TeamUpdate
):

    db_team = (
        db.query(Team)
        .filter(Team.team_id == team_id)
        .first()
    )

    if db_team is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )

    update_data = team.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_team, field, value)

    db_team.updated_at = datetime.utcnow()

    try:
        db.commit()
        db.refresh(db_team)

        return db_team

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to update team."
        )