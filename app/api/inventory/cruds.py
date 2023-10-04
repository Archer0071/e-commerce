import math
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from api.inventory import models
from api.inventory.schemas import GetInventoryHistory, PaginatedInventory

# ---------------------------- Inventory Functions ---------------------------------------

# Function to create a new inventory item
def create_inventory(db: Session, inventory_data):
    """
    Create a new inventory item.

    Args:
        db (Session): Database session.
        inventory_data (dict): Data for creating the inventory item.

    Returns:
        Inventory: Created inventory item.
    """
    db_inventory = models.Inventory(**inventory_data)
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    create_inventory_history(db, db_inventory)
    return db_inventory

# Function to retrieve all inventory items
def get_all_inventory(db: Session):
    """
    Retrieve all inventory items.

    Args:
        db (Session): Database session.

    Returns:
        List[Inventory]: List of inventory items.
    """
    return db.query(models.Inventory).all()

# Function to retrieve an inventory item by its ID
def get_inventory_by_id(db: Session, inventory_id: int):
    """
    Retrieve an inventory item by its ID.

    Args:
        db (Session): Database session.
        inventory_id (int): ID of the inventory item.

    Returns:
        Inventory: Retrieved inventory item.
    """
    return db.query(models.Inventory).filter(models.Inventory.id == inventory_id).first()

# Function to retrieve an inventory item history by its ID
def get_inventory_history(db: Session, inventory_id, page, per_page):
    """
    Retrieve the history of an inventory item.

    Args:
        db (Session): Database session.
        inventory_id (int): ID of the inventory item.
        page (int): Page number.
        per_page (int): Items per page.

    Returns:
        PaginatedInventory: Paginated result of inventory item history.
    """
    limit = per_page * page
    offset = (page - 1) * per_page
    items = [GetInventoryHistory(id=item.id, inventory_id=item.inventory_id, quantity=item.quantity,
                                 last_updated=item.last_updated, status=item.status)
             for item in db.scalars(select(models.InventoryHistory).where(models.InventoryHistory.inventory_id == inventory_id)
                                   .limit(limit).offset(offset).order_by(models.InventoryHistory.id.desc()))]
    items_list = db.query(models.InventoryHistory).filter(models.InventoryHistory.inventory_id == inventory_id).all()
    total = math.ceil(len(items_list) / limit)

    return PaginatedInventory(page_number=page, total_pages=total, items=items)

# Function to retrieve an inventory item by the ID of its associated product
def get_inventory_by_product_id(db: Session, product_id: int):
    """
    Retrieve an inventory item by the ID of its associated product.

    Args:
        db (Session): Database session.
        product_id (int): ID of the associated product.

    Returns:
        Inventory: Retrieved inventory item.
    """
    return db.query(models.Inventory).filter(models.Inventory.product_id == product_id)

# Function to update an inventory item
def update_inventory(db: Session, inventory_id, update_data):
    """
    Update an inventory item.

    Args:
        db (Session): Database session.
        inventory_id (int): ID of the inventory item to be updated.
        update_data (dict): Data for updating the inventory item.

    Returns:
        Inventory: Updated inventory item.
    """
    existing_inventory = get_inventory_by_id(db, inventory_id)
    # Update the fields
    existing_inventory.quantity = update_data.quantity
    existing_inventory.status = update_data.status
    create_inventory_history(db, existing_inventory)

    # Save the changes
    db.commit()
    db.refresh(existing_inventory)
    return existing_inventory

# Function to create inventory history
def create_inventory_history(db: Session, inventory):
    """
    Create a new version in the history table for the inventory item.

    Args:
        db (Session): Database session.
        inventory (Inventory): Inventory item for which history is created.

    Returns:
        InventoryHistory: Created inventory history entry.
    """
    history_data = {
        "inventory_id": inventory.id,
        "quantity": inventory.quantity,
        "status": inventory.status,
    }
    db_history = models.InventoryHistory(**history_data)
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history
