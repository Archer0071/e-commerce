from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db.session import get_db
from api.inventory import cruds as inventory_cruds
from api.inventory.schemas import GetInventory, UpdateInventory, PaginatedInventory

router = APIRouter()

# ------------------------ Inventory Routes -----------------------------------------------------------

@router.get("/inventory")
async def get_all_inventory(db: Session = Depends(get_db)):
    """
    Get all inventory items.

    Args:
        db (Session): Database session.

    Returns:
        List[GetInventory]: List of inventory items.
    """
    return inventory_cruds.get_all_inventory(db)

@router.get("/inventory_history/{inventory_id}", response_model=PaginatedInventory)
async def get_inventory_history(
    inventory_id: int,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    """
    Get all inventory history items.

    Args:
        inventory_id (int): ID of the inventory item.
        page (int): Page number.
        per_page (int): Items per page.
        db (Session): Database session.

    Returns:
        PaginatedInventory: List of paginated inventory history items.
    """
    return inventory_cruds.get_inventory_history(db, inventory_id, page, per_page)

@router.patch("/inventory/{inventory_id}", response_model=GetInventory)
async def update_inventory(
    inventory_id: int,
    update_data: UpdateInventory,
    db: Session = Depends(get_db)
):
    """
    Update an inventory item.

    Args:
        inventory_id (int): ID of the inventory item to update.
        update_data (UpdateInventory): Data for updating the inventory item.
        db (Session): Database session.

    Returns:
        GetInventory: Updated inventory item.
    """
    existing_inventory = inventory_cruds.get_inventory_by_id(db, inventory_id)

    if not existing_inventory:
        raise HTTPException(404, detail="Inventory not found")

    updated_inventory = inventory_cruds.update_inventory(db, inventory_id, update_data)
    return updated_inventory
