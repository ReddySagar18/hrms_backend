
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.employment_type import (
    EmploymentTypeCreate,
    EmploymentTypeResponse
)
from app.services.employment_type_service import (
    create_employment_type,
    get_employment_type,
    get_all_employment_types
)
from app.dependencies.auth import require_role


router = APIRouter(
    prefix="/employment-types",
    tags=["Employment Type"]
)


@router.post("/", response_model=EmploymentTypeResponse)
def create(
    employment_type: EmploymentTypeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("HR"))
):
    return create_employment_type(db, employment_type)


@router.get("/", response_model=list[EmploymentTypeResponse])
def get_all(
    db: Session = Depends(get_db)
):
    return get_all_employment_types(db)


@router.get("/{employment_type_id}", response_model=EmploymentTypeResponse)
def get_by_id(
    employment_type_id: int,
    db: Session = Depends(get_db)
):
    employment_type = get_employment_type(db, employment_type_id)

    if not employment_type:
        raise HTTPException(
            status_code=404,
            detail="Employment type not found"
        )

    return employment_type
