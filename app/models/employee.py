from datetime import date , datetime 
from sqlalchemy import ForeignKey
from sqlalchemy import Date,DateTime, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from app.db.database import Base
from typing import TYPE_CHECKING


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    employee_id: Mapped[str | None] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )
    
    
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)

    last_name: Mapped[str] = mapped_column(String(100), nullable=False)

    personal_email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(String(15), nullable=False)

    department_id: Mapped[str] = mapped_column(
    ForeignKey("departments.department_id"),
    nullable=False
)

    department: Mapped["Department"] = relationship(
    "Department",
    back_populates="employees"
)
    
    designation_id: Mapped[int] = mapped_column(
    ForeignKey("designations.id"),
    nullable=True
    )
    designation: Mapped["Designation"] = relationship(
    "Designation",
    back_populates="employees" 
    ) 
    employment_type_id: Mapped[int] = mapped_column(
    ForeignKey("employment_types.id"),
    nullable=True
)

    employment_type: Mapped["EmploymentType"] = relationship(
    "EmploymentType",
    back_populates="employees"
)

   
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)

    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    password_hash: Mapped[str | None] = mapped_column(
    String(255),
    nullable=True
    )
    activation_token: Mapped[str | None] = mapped_column(
    String(255),
    unique=True,
    nullable=True
)

    activation_expiry: Mapped[datetime | None] = mapped_column(
    DateTime,
    nullable=True
)
    role: Mapped[str] = mapped_column(
    String(20),
    nullable=False,
    default="Employee"
)
    

    status: Mapped[str] = mapped_column(
    String(30),
    default="Pending Activation",
    nullable=False
)
if TYPE_CHECKING:
    from app.models.designation import Designation
    from app.models.employment_type import EmploymentType
    from app.models.department import Department