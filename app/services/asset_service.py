from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.models.asset import Asset
from app.schemas.asset import AssetCreate
from app.schemas.asset import AssetUpdate

def create_asset(db: Session, asset: AssetCreate):

    db_asset = Asset(
        asset_id=asset.asset_id,
        asset_name=asset.asset_name,
        asset_category=asset.asset_category,
        serial_number=asset.serial_number,
        status=asset.status,
        employee_id=None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    try:
        db.add(db_asset)
        db.commit()
        db.refresh(db_asset)

        return db_asset

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Asset with this ID already exists."
        )


def get_all_assets(db: Session):

    return db.query(Asset).all()


def get_asset_by_id(db: Session, asset_id: str):

    asset = (
        db.query(Asset)
        .filter(Asset.asset_id == asset_id)
        .first()
    )

    if asset is None:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    return asset
#update asset
def update_asset(db: Session, asset_id: str, asset_data: AssetUpdate):
    asset = db.query(Asset).filter(Asset.asset_id == asset_id).first()

    if not asset:
        return None

    update_data = asset_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(asset, field, value)

    db.commit()
    db.refresh(asset)

    return asset
# retire asset 
def retire_asset(db: Session, asset_id: str):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()

    if not asset:
        return None

    asset.status = "Retired"

    db.commit()
    db.refresh(asset)

    return asset


def assign_asset(db: Session, asset_id: str, employee_id: str):

    asset = db.query(Asset).filter(Asset.id == asset_id).first()

    if not asset:
        return None, "Asset not found"

    employee = (
        db.query(Employee)
        .filter(Employee.employee_id == employee_id)
        .first()
    )

    if not employee:
        return None, "Employee not found"

    if asset.status != "Available":
        return None, "Asset is not available for assignment"

    asset.employee_id = employee_id
    asset.status = "Assigned"

    db.commit()
    db.refresh(asset)

    return asset, None


def return_asset(db: Session, asset_id: str):

    asset = db.query(Asset).filter(Asset.id == asset_id).first()

    if not asset:
        return None, "Asset not found"

    if asset.status != "Assigned":
        return None, "Asset is not currently assigned"

    asset.employee_id = None
    asset.status = "Available"

    db.commit()
    db.refresh(asset)

    return asset, None

def replace_asset(db: Session, old_asset_id: str, new_asset_id: str):

    old_asset = (
        db.query(Asset)
        .filter(Asset.id == old_asset_id)
        .first()
    )

    if not old_asset:
        return None, "Old asset not found"

    if old_asset.status != "Assigned":
        return None, "Old asset is not currently assigned"

    employee_id = old_asset.employee_id

    new_asset = (
        db.query(Asset)
        .filter(Asset.id == new_asset_id)
        .first()
    )

    if not new_asset:
        return None, "New asset not found"

    if new_asset.status != "Available":
        return None, "New asset is not available"

    if old_asset_id == new_asset_id:
        return None, "Old and new asset cannot be the same"

    # Retire old asset
    old_asset.employee_id = None
    old_asset.status = "Retired"

    # Assign new asset
    new_asset.employee_id = employee_id
    new_asset.status = "Assigned"

    db.commit()

    db.refresh(old_asset)
    db.refresh(new_asset)

    return new_asset, None