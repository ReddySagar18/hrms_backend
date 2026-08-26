from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.department import DepartmentCreate, DepartmentResponse ,DepartmentUpdate
from app.services.department_service import (create_department,get_all_departments, get_department_by_id ,update_department)
from app.dependencies.auth import require_role


router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)
@router.get("/", response_model=list[DepartmentResponse])
def get_departments(
    db: Session = Depends(get_db),
   
):
    return get_all_departments(db)

@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(
    department_id: str,
    db: Session = Depends(get_db)
):
    return get_department_by_id(
        db,
        department_id
    )
@router.post("/", response_model=DepartmentResponse)
def create_new_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("HR"))
):
    return create_department(db, department)
@router.patch(
    "/{department_id}",
    response_model=DepartmentResponse
)
def update_existing_department(
    department_id: str,
    department: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("HR"))
):
    return update_department(
        db,
        department_id,
        department
    )
