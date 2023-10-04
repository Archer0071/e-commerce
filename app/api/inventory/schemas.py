from typing import List, TypeVar, Generic
from pydantic import BaseModel
from api.inventory.models import InventoryStatus
from datetime import datetime

# ----------------------------------- Inventory Schemas ----------------------------------

class CreateInventory(BaseModel):
    """
    Schema for creating a new inventory item.

    Attributes:
        product_id (int): ID of the associated product.
        quantity (int): Initial quantity of the inventory item.
        status (InventoryStatus): Status of the inventory item.
    """
    product_id: int
    quantity: int
    status: InventoryStatus

class GetInventory(BaseModel):
    """
    Schema for getting details of an inventory item.

    Attributes:
        id (int): Unique identifier for the inventory item.
        product_id (int): ID of the associated product.
        quantity (int): Current quantity of the inventory item.
        last_updated (datetime): Timestamp when the inventory item was last updated.
        status (InventoryStatus): Status of the inventory item.
    """
    id: int
    product_id: int
    quantity: int
    last_updated: datetime
    status: InventoryStatus

class UpdateInventory(BaseModel):
    """
    Schema for updating an inventory item.

    Attributes:
        quantity (int): New quantity for the inventory item.
        status (InventoryStatus): New status for the inventory item.
    """
    quantity: int
    status: InventoryStatus

class GetInventoryHistory(BaseModel):
    """
    Schema for retrieving historical information of an inventory item.

    Attributes:
        id (int): Unique identifier for the historical record.
        inventory_id (int): ID of the associated inventory item.
        quantity (int): Quantity at the time of the historical record.
        last_updated (datetime): Timestamp of the historical record.
        status (InventoryStatus): Status of the inventory item at the time of the historical record.
    """
    id: int
    inventory_id: int
    quantity: int
    last_updated: datetime
    status: InventoryStatus

T = TypeVar('T')
class PaginatedInventory(BaseModel, Generic[T]):
    """
    Schema for paginated inventory items.

    Attributes:
        page_number (int): Current page number.
        total_pages (int): Total number of pages.
        items (List[T]): List of items on the current page.
    """
    page_number: int
    total_pages: int
    items: List[T]
