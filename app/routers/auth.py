from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import create_access_token
from app.db.database import get_db
from app.schemas.employee import EmployeeLogin
from app.services.auth_service import authenticate_employee


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(
    data: EmployeeLogin,
    db: Session = Depends(get_db)
):
    employee = authenticate_employee(
        db,
        data.employee_id,
        data.password
    )
    access_token=create_access_token(
    {
        "sub": employee.employee_id,
        "role": employee.role
    }
)

    return {
        "message": "Login successful.",
        "access_token": access_token,
    "token_type": "bearer"
    }