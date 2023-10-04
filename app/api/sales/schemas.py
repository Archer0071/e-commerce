from pydantic import BaseModel
from datetime import datetime

# SaleCreate schema for creating a new sale record
class SaleCreate(BaseModel):
    """
    Schema for creating a new sale record.

    Attributes:
        inventory_id (int): ID of the associated inventory item.
        quantity_sold (int): Quantity of the product sold in the sale record.
    """
    inventory_id: int
    quantity_sold: int

# SaleResponse schema for retrieving details of a sale record
class SaleResponse(BaseModel):
    """
    Schema for getting details of a sale record.

    Attributes:
        id (int): Unique identifier for the sale record.
        inventory_id (int): ID of the associated inventory item.
        quantity_sold (int): Quantity of the product sold in the sale record.
        sale_date (datetime): Timestamp of the sale record.
    """
    id: int
    inventory_id: int
    quantity_sold: int
    sale_date: datetime
