import math
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from api.sales import models as sale_model
from api.inventory import models as inventory_model
from utils.enums import InventoryStatus
from api.sales.schemas import SaleCreate


# ---------------------------- Sales Functions ---------------------------------------

 # Function to create a new sales 
def create_sale(db: Session,inventory:inventory_model.Inventory, sale: SaleCreate):
     # Update inventory status
    inventory.quantity -= sale.quantity_sold
    if inventory.quantity <= 2:
        inventory.status = InventoryStatus.LOW
    elif inventory.quantity == 0:
        inventory.status = InventoryStatus.OUT_OF_STOCK

    db_sale = sale_model.Sale(**sale.model_dump())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def get_all_sale(db:Session):
    return db.query(sale_model.Sale).all()

