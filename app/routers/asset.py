from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.asset import AssetCreate, AssetResponse , AssetUpdate , AssetAssign , AssetReplace
from app.services.asset_service import (
    create_asset,
    get_all_assets,
    get_asset_by_id,
    update_asset,
    retire_asset,
    assign_asset,
    return_asset,
    replace_asset
    
)
from app.dependencies.auth import require_role


router = APIRouter(
    prefix="/assets",
    tags=["Assets"]
)

#post assets 
@router.post("/", response_model=AssetResponse)
def create_new_asset(
    asset: AssetCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("HR"))
):
    return create_asset(db, asset)

#get all assets 
@router.get("/", response_model=list[AssetResponse])
def get_assets(
    db: Session = Depends(get_db)
):
    return get_all_assets(db)

#get asset by id 
@router.get("/{asset_id}", response_model=AssetResponse)
def get_asset(
    asset_id: str,
    db: Session = Depends(get_db)
):
    return get_asset_by_id(db, asset_id)

#update asset
@router.patch("/{asset_id}", response_model=AssetResponse)
def update_asset_route(
    asset_id: int,
    asset_data: AssetUpdate,
    db: Session = Depends(get_db),
    current_user: dict=Depends(require_role("HR"))
):
    asset = update_asset(db, asset_id, asset_data)

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    return asset
# retire asset
@router.patch("/{asset_id}/retire", response_model=AssetResponse)
def retire_asset_route(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("HR"))
):
    asset = retire_asset(db, asset_id)

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    return asset
@router.post("/{asset_id}/assign", response_model=AssetResponse)
def assign_asset_route(
    asset_id: str,
    data: AssetAssign,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("HR"))
):
    asset, error = assign_asset(
        db,
        asset_id,
        data.employee_id
    )

    if error == "Asset not found":
        raise HTTPException(
            status_code=404,
            detail=error
        )

    if error == "Employee not found":
        raise HTTPException(
            status_code=404,
            detail=error
        )

    if error == "Asset is not available for assignment":
        raise HTTPException(
            status_code=400,
            detail=error
        )

    return asset


@router.post("/{asset_id}/return", response_model=AssetResponse)
def return_asset_route(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("HR"))
):
    asset, error = return_asset(db, asset_id)

    if error == "Asset not found":
        raise HTTPException(
            status_code=404,
            detail=error
        )

    if error == "Asset is not currently assigned":
        raise HTTPException(
            status_code=400,
            detail=error
        )

    return asset
#asset replace 
@router.post("/{asset_id}/replace", response_model=AssetResponse)
def replace_asset_route(
    asset_id: int,
    data: AssetReplace,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("HR"))
):
    asset, error = replace_asset(
        db,
        asset_id,
        data.new_asset_id
    )

    if error in [
        "Old asset not found",
        "New asset not found"
    ]:
        raise HTTPException(
            status_code=404,
            detail=error
        )

    if error in [
        "Old asset is not currently assigned",
        "New asset is not available",
        "Old and new asset cannot be the same"
    ]:
        raise HTTPException(
            status_code=400,
            detail=error
        )

    return asset