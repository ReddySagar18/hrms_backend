from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.department import Department
from app.schemas.department import (DepartmentCreate,DepartmentUpdate)

def get_all_departments(db: Session):

    return db.query(Department).all()
def create_department(db: Session, department: DepartmentCreate):

    db_department = Department(
        department_id=department.department_id,
        department_name=department.department_name,
        status=department.status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    try:
        db.add(db_department)
        db.commit()
        db.refresh(db_department)

        return db_department

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Department with this ID already exists."
        )
def get_department_by_id(db: Session, department_id: str):

    department = (
        db.query(Department)
        .filter(Department.department_id == department_id)
        .first()
    )

    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    return department


# update department 
def update_department(
    db: Session,
    department_id: str,
    department: DepartmentUpdate
):

    db_department = (
        db.query(Department)
        .filter(Department.department_id == department_id)
        .first()
    )

    if db_department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    update_data = department.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_department, field, value)

    db_department.updated_at = datetime.utcnow()

    try:
        db.commit()
        db.refresh(db_department)

        return db_department

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to update department."
        )