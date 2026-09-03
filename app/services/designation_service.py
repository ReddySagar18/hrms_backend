from sqlalchemy.orm import Session

from app.models.designation import Designation
from app.schemas.designation import DesignationCreate, DesignationUpdate


def create_designation(
    db: Session,
    designation_data: DesignationCreate
):
    designation = Designation(
        designation_name=designation_data.designation_name,
        designation_status=designation_data.designation_status
    )

    db.add(designation)
    db.commit()
    db.refresh(designation)

    return designation


def get_all_designations(db: Session):
    return db.query(Designation).all()


def get_designation_by_id(
    db: Session,
    designation_id: int
):
    return (
        db.query(Designation)
        .filter(Designation.id == designation_id)
        .first()
    )


def update_designation(
    db: Session,
    designation_id: int,
    designation_data: DesignationUpdate
):
    designation = (
        db.query(Designation)
        .filter(Designation.id == designation_id)
        .first()
    )

    if not designation:
        return None

    update_data = designation_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(designation, field, value)

    db.commit()
    db.refresh(designation)

    return designation


def delete_designation(
    db: Session,
    designation_id: int
):
    designation = (
        db.query(Designation)
        .filter(Designation.id == designation_id)
        .first()
    )

    if not designation:
        return None

    db.delete(designation)
    db.commit()

    return designation