from pydantic import BaseModel
from datetime import datetime

class SaleCreate(BaseModel):
    inventory_id: int
    quantity_sold: int

class SaleResponse(BaseModel):
    id: int
    inventory_id: int
    quantity_sold: int
    sale_date: datetime