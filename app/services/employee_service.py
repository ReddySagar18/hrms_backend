import secrets
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.core.security import hash_password
from datetime import datetime, timedelta
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate
from app.models import designation
from app.models.designation import Designation
from app.models.employment_type import EmploymentType
from sqlalchemy import text
from app.models.department import Department
def create_employee(db: Session, employee: EmployeeCreate):
    designation = db.query(Designation).filter(
        Designation.id == employee.designation_id
    ).first()

    if designation is None:
        raise HTTPException(
            status_code=404,
            detail="Designation not found"
        )
    employee_number = db.execute(
    text("SELECT nextval('employee_id_seq')")
    ).scalar()
    employee_id = f"EMP{employee_number:06d}"

    db_employee = Employee(
        employee_id=employee_id,
        first_name=employee.first_name,
        last_name=employee.last_name,
        personal_email=employee.personal_email,
        phone=employee.phone,
        department_id=employee.department_id,
        designation_id=employee.designation_id,
        employment_type_id=employee.employment_type_id,
        date_of_birth=employee.date_of_birth,
        gender=employee.gender,
        password_hash= None ,
        status="Pending Activation"
        
    )


    try:
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
       

        db_employee.activation_token = secrets.token_urlsafe(32)
        db_employee.activation_expiry = (
            datetime.utcnow() + timedelta(hours=24)
)       
        db.commit()
        db.refresh(db_employee)

        
        activation_link = (
            f"http://127.0.0.1:8000/activate?"
            f"token={db_employee.activation_token}"
)
        print("\n" + "=" * 70)
        print("EMPLOYEE CREATED SUCCESSFULLY")
        print(f"Employee ID     : {db_employee.employee_id}")
        print(f"Activation Link : {activation_link}")
        print("=" * 70 + "\n")

        # 8. Response to HR
        return {
            "message": "Employee created successfully.",
            "employee_id": db_employee.employee_id,
            "status": db_employee.status
        }

        
    except IntegrityError as e:
        db.rollback()
        print("=" * 80)
        print(e)
        print("=" * 80)

        raise
def get_all_employees(db: Session):
    return db.query(Employee).all()

def get_employee_by_id(db: Session, employee_id: str):

    employee = (
        db.query(Employee)
        .filter(Employee.employee_id == employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee
def update_employee(
    db: Session,
    employee_id: str,
    employee: EmployeeCreate,
):
    # 1. Find employee first
    db_employee = (
        db.query(Employee)
        .filter(Employee.employee_id == employee_id)
        .first()
    )

    if db_employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    # 2. Department
    if employee.department_id is not None:
        department = db.query(Department).filter(
            Department.department_id == employee.department_id
        ).first()

        if department is None:
            raise HTTPException(
                status_code=404,
                detail="Department not found"
            )

        db_employee.department_id = employee.department_id

    # 3. Designation
    if employee.designation_id is not None:
        designation = db.query(Designation).filter(
            Designation.id == employee.designation_id
        ).first()

        if designation is None:
            raise HTTPException(
                status_code=404,
                detail="Designation not found"
            )

        db_employee.designation_id = employee.designation_id

    # 4. Employment Type
    if employee.employment_type_id is not None:
        employment_type = db.query(EmploymentType).filter(
            EmploymentType.id == employee.employment_type_id
        ).first()

        if employment_type is None:
            raise HTTPException(
                status_code=404,
                detail="Employment Type not found"
            )

        db_employee.employment_type_id = employee.employment_type_id

  

    if db_employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    update_data=employee.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_employee, field, value)

    try:
        db.commit()
        db.refresh(db_employee)
        return db_employee

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Employee with this email already exists."
        )
# deletion of employee
def delete_employee(db: Session, employee_id: str):

    db_employee = (
        db.query(Employee)
        .filter(Employee.employee_id == employee_id)
        .first()
    )

    if db_employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    db_employee.status = "Inactive"

    db.commit()
    db.refresh(db_employee)

    return {
        "message": "Employee deactivated successfully.",
        "employee_id": db_employee.employee_id,
        "status": db_employee.status
    }
def activate_employee_account(db: Session, token: str, password: str):

    employee = (
        db.query(Employee)
        .filter(Employee.activation_token == token)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=400,
            detail="Invalid activation link."
        )

    if employee.activation_expiry < datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="Activation link has expired."
        )

    if employee.status != "Pending Activation":
        raise HTTPException(
            status_code=400,
            detail="Employee account is already activated."
        )

    employee.password_hash = hash_password(password)

    employee.status = "Active"

    employee.activation_token = None

    employee.activation_expiry = None

    db.commit()
    db.refresh(employee)

    return {
        "message": "Account activated successfully.",
        "employee_id": employee.employee_id
    }