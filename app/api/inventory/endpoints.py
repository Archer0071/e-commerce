from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.inventory.cruds import *
from app.api.inventory.schemas import GetInventory,UpdateInventory


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
    return get_all_inventory(db)

@router.get("/inventory/{inventory_id}")
async def get_inventory_history_by_id(inventory_id:int,db: Session = Depends(get_db)):
    """
    Get all inventory history items.

    Args:
        db (Session): Database session.

    Returns:
        List[GetInventory]: List of inventory history items.
    """
    inventory = get_inventory_history_by_id(db,inventory_id)
    print(inventory)
    if inventory is None:
        raise HTTPException(404, detail="Inventory not found")

    return inventory

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
    existing_inventory = get_inventory_by_id(db, inventory_id)

    if not existing_inventory:
        raise HTTPException(404, detail="Inventory not found")

    updated_inventory = update_inventory(db, inventory_id, update_data)
    return updated_inventory