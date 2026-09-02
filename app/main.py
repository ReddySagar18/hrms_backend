from fastapi import FastAPI
from app.routers.home import router as home_router
from app.db.database import Base, engine
from app.routers.auth import router as auth_router
from app.routers.department import router as department_router
from app.routers.project import router as project_router
from app.routers.asset import router as asset_router
# Register all ORM models
import app.models
from app.models.department import Department
from app.models.team import Team 
from app.models.project import Project
from app.models.asset import Asset
from app.routers.home import router as home_router
from app.routers.employees import router as employee_router
from app.routers.team import router as team_router
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HRMS Backend API",
    description="Backend API for the Human Resource Management System",
    version="1.0.0",
)

app.include_router(home_router)
app.include_router(employee_router)
app.include_router(auth_router)
app.include_router(department_router)
app.include_router(team_router)
app.include_router(project_router)
app.include_router(asset_router)
print("EMPLOYEE ROUTES:")

for route in employee_router.routes:
    print(
        route.path,
        route.methods
    )
print("depatment ROUTES:")

for route in department_router.routes:
    print(
        route.path,
        route.methods
    )
