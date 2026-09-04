
from sqlalchemy.orm import Session

from app.models.employment_type import EmploymentType
from app.schemas.employment_type import EmploymentTypeCreate


def create_employment_type(
    db: Session,
    employment_type: EmploymentTypeCreate
):
    db_employment_type = EmploymentType(
        employment_type_name=employment_type.employment_type_name,
        employment_type_status=employment_type.employment_type_status
    )

    db.add(db_employment_type)
    db.commit()
    db.refresh(db_employment_type)

    return db_employment_type


def get_employment_type(
    db: Session,
    employment_type_id: int
):
    return db.query(EmploymentType).filter(
        EmploymentType.id == employment_type_id
    ).first()


def get_all_employment_types(db: Session):
    return db.query(EmploymentType).all()

