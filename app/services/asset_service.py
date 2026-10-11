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
        return None, "Asset not found"

    update_data = asset_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(asset, field, value)

    db.commit()
    db.refresh(asset)

    return asset
# retire asset 
def retire_asset(db: Session, asset_id: str):
    asset = db.query(Asset).filter(Asset.asset_id == asset_id).first()

    if not asset:
        return None, "Asset not found"
    if asset.employee_id is not None:
        return None, "Cannot retire an asset that is currently assigned to an employee"
    if asset.status == "Retired":
        return None, "Asset is already retired"
    asset.status = "Retired"

    db.commit()
    db.refresh(asset)

    return asset,None


def assign_asset_to_employee(
    db,
    asset_id: str,
    employee_id: str
):
    asset = db.query(Asset).filter(
        Asset.asset_id == asset_id
    ).first()

    if asset is None:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    employee = db.query(Employee).filter(
        Employee.employee_id == employee_id
    ).first()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    if asset.employee_id is not None:
        raise HTTPException(
            status_code=400,
            detail="Asset is already assigned to an employee"
        )
    if asset.status != "Active":
        raise HTTPException(
            status_code=400,
            detail="Only Active assets can be assigned"
        )

    asset.employee_id = employee_id
    
    db.commit()
    db.refresh(asset)

    return asset

def return_asset(db: Session, asset_id: str, employee_id: str):
    asset = db.query(Asset).filter(
        Asset.asset_id == asset_id
    ).first()

    if not asset:
        return None, "Asset not found"

    employee = db.query(Employee).filter(
        Employee.employee_id == employee_id
    ).first()

    if not employee:
        return None, "Employee not found"

    if asset.employee_id is None:
        return None, "Asset is not currently assigned"

    if asset.employee_id != employee_id:
        return None, "Asset is not assigned to this employee"

    if asset.status != "Active":
        return None, "Only Active assets can be returned"

    asset.employee_id = None
    asset.status = "Active"

    db.commit()
    db.refresh(asset)

    return asset, None

def replace_asset(
    db: Session,
    old_asset_id: str,
    new_asset_id: str,
    employee_id: str
):
    old_asset = db.query(Asset).filter(
        Asset.asset_id == old_asset_id
    ).first()

    if not old_asset:
        return None, "Old asset not found"

    new_asset = db.query(Asset).filter(
        Asset.asset_id == new_asset_id
    ).first()

    if not new_asset:
        return None, "New asset not found"

    employee = db.query(Employee).filter(
        Employee.employee_id == employee_id
    ).first()

    if not employee:
        return None, "Employee not found"

    if old_asset_id == new_asset_id:
        return None, "Old and new asset cannot be the same"

    if old_asset.status != "Active":
        return None, "Old asset must be Active"

    if old_asset.employee_id is None:
        return None, "Old asset is not currently assigned"

    if old_asset.employee_id != employee_id:
        return None, "Old asset is not assigned to this employee"

    if new_asset.status != "Active":
        return None, "New asset must be Active"

    if new_asset.employee_id is not None:
        return None, "New asset is already assigned"

    try:
        old_asset.employee_id = None
        old_asset.status = "Retired"

        new_asset.employee_id = employee_id
        new_asset.status = "Active"

        db.commit()

        db.refresh(old_asset)
        db.refresh(new_asset)

        return new_asset, None

    except Exception:
        db.rollback()
        raise



def get_employee_assets(
    db: Session,
    employee_id: str
):
    employee = db.query(Employee).filter(
        Employee.employee_id == employee_id
    ).first()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    assets = db.query(Asset).filter(
        Asset.employee_id == employee_id
    ).all()

    return assets