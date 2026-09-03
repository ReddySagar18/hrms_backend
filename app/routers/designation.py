from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.designation import (
    DesignationCreate,
    DesignationUpdate,
    DesignationResponse,
)
from app.services.designation_service import (
    create_designation,
    get_all_designations,
    get_designation_by_id,
    update_designation,
    delete_designation,
)
from app.dependencies.auth import require_role


router = APIRouter(
    prefix="/designations",
    tags=["Designations"]
)


@router.post(
    "/",
    response_model=DesignationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_designation_route(
    designation_data: DesignationCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("HR"))
):
    return create_designation(db, designation_data)


@router.get(
    "/",
    response_model=list[DesignationResponse]
)
def get_all_designations_route(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("HR"))
):
    return get_all_designations(db)


@router.get(
    "/{designation_id}",
    response_model=DesignationResponse
)
def get_designation_by_id_route(
    designation_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("HR"))
):
    designation = get_designation_by_id(db, designation_id)

    if not designation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Designation not found"
        )

    return designation


@router.patch(
    "/{designation_id}",
    response_model=DesignationResponse
)
def update_designation_route(
    designation_id: int,
    designation_data: DesignationUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("HR"))
):
    designation = update_designation(
        db,
        designation_id,
        designation_data
    )

    if not designation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Designation not found"
        )

    return designation


@router.delete(
    "/{designation_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_designation_route(
    designation_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("HR"))
):
    designation = delete_designation(db, designation_id)

    if not designation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Designation not found"
        )