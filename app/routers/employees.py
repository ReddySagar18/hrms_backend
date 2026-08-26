from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.employee import EmployeeCreate ,EmployeeUpdate
from app.services.employee_service import (create_employee,get_all_employees, get_employee_by_id, update_employee,  delete_employee, activate_employee_account,)
from app.schemas.employee import EmployeeActivate
from app.schemas.employee import EmployeeLogin
from app.services.auth_service import  authenticate_employee
from app.dependencies.auth import get_current_user , require_role
router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)

#get all employees 
# Get all employees
@router.get("/")
def get_employees(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("HR"))
):
    return get_all_employees(db)

# Get my profile
@router.get("/me")
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return get_employee_by_id(
        db,
        current_user["employee_id"]
    )

# Activate employee account
@router.post("/activate")
def activate_employee(
    data: EmployeeActivate,
    db: Session = Depends(get_db)
):
    return activate_employee_account(
        db,
        data.token,
        data.password
    )


# Create employee
@router.post("/")
def create_new_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("HR"))
):
    return create_employee(db, employee)


# Get employee by ID
@router.get("/{employee_id}")
def get_employee(
    employee_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("HR"))
):
    return get_employee_by_id(db, employee_id)


# Update employee
@router.patch("/{employee_id}")
def update_existing_employee(
    employee_id: str,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("HR"))
):
    return update_employee(
        db,
        employee_id,
        employee,
    )


# Delete employee
@router.delete("/{employee_id}")
def delete_existing_employee(
    employee_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("HR"))
):
    return delete_employee(
        db,
        employee_id,
    )