from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.project import (ProjectCreate, ProjectResponse , ProjectUpdate)
from app.services.project_service import (
    create_project,
    get_all_projects,
    get_project_by_id,
    update_project,
    archive_project
)
from app.dependencies.auth import require_role


router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post("/", response_model=ProjectResponse)
def create_new_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("HR"))
):
    return create_project(db, project)


@router.get("/", response_model=list[ProjectResponse])
def get_projects(
    db: Session = Depends(get_db)
):
    return get_all_projects(db)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: str,
    db: Session = Depends(get_db)
):
    return get_project_by_id(db, project_id)

#update the project 
@router.patch(
    "/{project_id}",
    response_model=ProjectResponse
)
def update_existing_project(
    project_id: str,
    project: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("HR"))
):
    return update_project(
        db,
        project_id,
        project
    )
#archive the project 
@router.patch("/{project_id}/archive", response_model=ProjectResponse)
def archive_existing_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("HR"))
):
    return archive_project(
        db,
        project_id
    )