from pydantic import BaseModel, EmailStr, Field 
from typing import Optional


class EmployeeCreate(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    personal_email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)

    department_id: str  | None=None
    designation_id: int | None=None
    employment_type_id: int|None=None

    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
class EmployeeUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    personal_email: str | None = None
    phone: str | None = None
    department_id: str | None = None
    designation_id: int | None = None
    employment_type_id: int | None = None
    date_of_birth: str | None = None
    gender: str | None = None

class EmployeeActivate(BaseModel):
    token: str
    password: str = Field(..., min_length=8, max_length=72)
class EmployeeLogin(BaseModel):
    employee_id: str
    password: str