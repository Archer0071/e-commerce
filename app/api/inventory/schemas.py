from typing import List,TypeVar,Generic
from pydantic import BaseModel
from api.inventory.models import InventoryStatus
from datetime import datetime


# ----------------------------------- Inventory Schemas ----------------------------------

class CreateInventory(BaseModel):
    """
    schema for creating a new inventory item.

    Attributes:
        product (int): ID of the associated product.
        quantity (int): Initial quantity of the inventory item.
        status (InventoryStatus): Status of the inventory item.
    """
    product: int
    quantity: int
    status: InventoryStatus

class GetInventory(BaseModel):
    """
    schema for getting details of an inventory item.

    Attributes:
        id (int): Unique identifier for the inventory item.
        product (int): ID of the associated product.
        quantity (int): Current quantity of the inventory item.
        last_updated (datetime): Timestamp when the inventory item was last updated.
        status (InventoryStatus): Status of the inventory item.
    """
    id: int
    product: int
    quantity: int
    last_updated: datetime
    status: InventoryStatus

class UpdateInventory(BaseModel):
    """
    schema for updating an inventory item.

    Attributes:
        quantity (int): New quantity for the inventory item.
        status (InventoryStatus): New status for the inventory item.
    """
    quantity: int
    status: InventoryStatus


class GetInventoryHistory(BaseModel):
    id : int
    inventory_id : int
    quantity : int
    last_updated : datetime
    status : InventoryStatus

T = TypeVar('T')
class PaginatedInventory(BaseModel):
    page_number: int
    total_pages: int
    items: List[T]
    