from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate , ProjectUpdate


def create_project(db: Session, project: ProjectCreate):

    db_project = Project(
        project_id=project.project_id,
        project_name=project.project_name,
        project_description=project.project_description,
        status=project.status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    try:
        db.add(db_project)
        db.commit()
        db.refresh(db_project)

        return db_project

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Project with this ID already exists."
        )


def get_all_projects(db: Session):

    return db.query(Project).all()


def get_project_by_id(db: Session, project_id: str):

    project = (
        db.query(Project)
        .filter(Project.project_id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project
 #update project 
def update_project(
    db: Session,
    project_id: str,
    project: ProjectUpdate
):

    db_project = (
        db.query(Project)
        .filter(Project.project_id == project_id)
        .first()
    )

    if db_project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    update_data = project.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_project, field, value)

    db_project.updated_at = datetime.utcnow()

    try:
        db.commit()
        db.refresh(db_project)

        return db_project

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to update project."
        )
# project archive 
def archive_project(db: Session, project_id: str):

    db_project = (
        db.query(Project)
        .filter(Project.project_id == project_id)
        .first()
    )

    if db_project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    db_project.status = "Archived"
    db_project.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_project)

    return db_project