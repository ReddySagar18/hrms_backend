from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.models.project import Project
from app.schemas.project import ProjectCreate , ProjectUpdate
from app.models.employee_project import EmployeeProject


def create_project(db: Session, project: ProjectCreate):

    db_project = Project(
        project_id=project.project_id,
        project_name=project.project_name,
        project_description=project.project_description,
        status=project.status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    try:
        db.add(db_project)
        db.commit()
        db.refresh(db_project)

        return db_project

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Project with this ID already exists."
        )


def get_all_projects(db: Session):

    return db.query(Project).all()


def get_project_by_id(db: Session, project_id: str):

    project = (
        db.query(Project)
        .filter(Project.project_id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project
 #update project 
def update_project(
    db: Session,
    project_id: str,
    project: ProjectUpdate
):

    db_project = (
        db.query(Project)
        .filter(Project.project_id == project_id)
        .first()
    )

    if db_project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    update_data = project.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_project, field, value)

    db_project.updated_at = datetime.utcnow()

    try:
        db.commit()
        db.refresh(db_project)

        return db_project

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Unable to update project."
        )
# project archive 
def archive_project(db: Session, project_id: str):

    db_project = (
        db.query(Project)
        .filter(Project.project_id == project_id)
        .first()
    )

    if db_project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    db_project.status = "Archived"
    db_project.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_project)

    return db_project



def assign_employee_to_project(
    db,
    project_id: str,
    employee_id: str
):
    # Check project exists
    project = db.query(Project).filter(
        Project.project_id == project_id
    ).first()

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    # Check employee exists
    employee = db.query(Employee).filter(
        Employee.employee_id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    # Check whether already assigned
    existing_assignment = db.query(EmployeeProject).filter(
        EmployeeProject.employee_id == employee_id,
        EmployeeProject.project_id == project_id
    ).first()

    if existing_assignment:
        raise HTTPException(
            status_code=400,
            detail="Employee is already assigned to this project"
        )

    # Create assignment
    assignment = EmployeeProject(
        employee_id=employee_id,
        project_id=project_id
    )

    db.add(assignment)
    db.commit()

    return {
        "message": "Employee assigned to project successfully"
    }

def remove_employee_from_project(
    db,
    project_id: str,
    employee_id: str
):
    assignment = db.query(EmployeeProject).filter(
        EmployeeProject.employee_id == employee_id,
        EmployeeProject.project_id == project_id
    ).first()

    if assignment is None:
        raise HTTPException(
            status_code=404,
            detail="Employee is not assigned to this project"
        )

    db.delete(assignment)
    db.commit()

    return {
        "message": "Employee removed from project successfully"
    }
def get_employee_projects(
    db,
    employee_id: str
):
    employee = db.query(Employee).filter(
        Employee.employee_id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee.projects
def get_employee_projects(
    db,
    employee_id: str
):
    employee = db.query(Employee).filter(
        Employee.employee_id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee.projects


def get_project_employees(
    db,
    project_id: str
):
    project = db.query(Project).filter(
        Project.project_id == project_id
    ).first()

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project.employees