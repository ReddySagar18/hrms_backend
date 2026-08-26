from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/",
    tags=["Home"],
    summary="Welcome Endpoint",
    description="Returns a welcome message to verify that the HRMS backend is running."
)
def root():
    return {
        "message": "Welcome to HRMS Backend API"
    }