from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.core.security import verify_password


def authenticate_employee(
    db: Session,
    employee_id: str,
    password: str
):

    employee = (
        db.query(Employee)
        .filter(Employee.employee_id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=401,
            detail="Invalid employee ID or password."
        )

    if employee.status != "Active":
        raise HTTPException(
            status_code=401,
            detail="Account is not active."
        )

    if not employee.password_hash:
        raise HTTPException(
            status_code=401,
            detail="Account is not activated."
        )

    if not verify_password(password, employee.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid employee ID or password."
        )

    return employee