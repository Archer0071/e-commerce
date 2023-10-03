from sqlalchemy.orm import Session
from inventory import models


# ---------------------------- Inventory Functions ---------------------------------------

# Function to create a new inventory item
def create_inventory(db: Session, inventory_data):
    db_inventory = models.Inventory(**inventory_data)
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    create_inventory_history(db, db_inventory)
    return db_inventory


# Function to retrieve all inventory items
def get_all_inventory(db: Session):
    return db.query(models.Inventory).all()

# Function to retrieve an inventory item by its ID
def get_inventory_by_id(db: Session, inventory_id: int):
    return db.query(models.Inventory).filter(models.Inventory.id == inventory_id).first()

# function to retrieve an inventory item history by its Id
def get_inventory_history_by_id(db:Session, inventory_id):
    return db.query(models.InventoryHistory).filter(models.InventoryHistory.inventory_id == inventory_id).all()

# Function to retrieve an inventory item by the ID of its associated product
def get_inventory_by_product_id(db: Session, product_id: int):
    return db.query(models.Inventory).filter(models.Inventory.product == product_id).first()

# Function to update an inventory item (TODO: Add parameters for update)
def update_inventory(db: Session, inventory_id, update_data):
    existing_inventory = get_inventory_by_id(db,inventory_id)
    # Update the fields
    existing_inventory.quantity = update_data.quantity
    existing_inventory.status = update_data.status
    create_inventory_history(db, existing_inventory)
   
    # Save the changes
    db.commit()
    db.refresh(existing_inventory)
    return existing_inventory

def create_inventory_history(db: Session, inventory):
    # Create a new version in the history table
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