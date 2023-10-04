import math
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from api.sales import models as sale_model
from api.inventory import models as inventory_model
from api.product import models as product_model
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

# function to get all the sale based on the filtering
def get_all_sale(db:Session,start_date,end_date,product_id,category):
     # Create the base query
    query = db.query(sale_model.Sale)

    # Apply date range filter, if specified
    if start_date and end_date:
        query = query.filter(func.DATE(sale_model.Sale.sale_date) >= start_date, func.DATE(sale_model.Sale.sale_date) <= end_date)

    # Apply product filter, if specified
    if product_id:
        query = query.join(inventory_model.Inventory).join(product_model.Product).filter(product_model.Product.id == product_id)

    # Apply category filter, if specified
    if category:
        query = query.join(inventory_model.Inventory).join(product_model.Product).filter(product_model.Product.category == category)

    # Get all sales data based on the specified filters
    sales_data = query.all()

    # Return the sales data
    return sales_data

def analyze_daily_revenue(db:Session):
    try:
        combined_sales_data = (
            db.query(
                func.DATE(inventory_model.Sale.sale_date).label("date"),
                func.sum(product_model.Product.price * sale_model.Sale.quantity_sold).label("total_revenue")
            )
            .join(inventory_model.Inventory, inventory_model.Inventory.id == sale_model.Sale.inventory_id)
            .join(product_model.Product, product_model.Product.id == inventory_model.Inventory.product_id)
            .group_by(func.DATE(sale_model.Sale.sale_date))
            .all()
        )

        result = [
            {"date": str(row.date), "total_revenue": row.total_revenue}
            for row in combined_sales_data
        ]

        return result

    except Exception as e:
        return []
    
def analyze_weekly_revenue(db:Session):
    return[]

def analyze_monthly_revenue(db: Session ):
    return []

def analyze_annual_revenue(db: Session ):
    return []



