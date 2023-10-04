import math
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from api.sales.models import Sale
from api.inventory.models import Inventory
from api.product.models import Product
from utils.enums import InventoryStatus
from api.sales.schemas import SaleCreate


# ---------------------------- Sales Functions ---------------------------------------

 # Function to create a new sales 
def create_sale(db: Session,inventory:Inventory, sale: SaleCreate):
     # Update inventory status
    inventory.quantity -= sale.quantity_sold
    if inventory.quantity <= 2:
        inventory.status = InventoryStatus.LOW
    elif inventory.quantity == 0:
        inventory.status = InventoryStatus.OUT_OF_STOCK

    db_sale = Sale(**sale.model_dump())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

# function to get all the sale based on the filtering
def get_all_sale(db:Session,start_date,end_date,product_id,category):
     # Create the base query
    query = db.query(Sale)

    # Apply date range filter, if specified
    if start_date and end_date:
        query = query.filter(func.DATE(Sale.sale_date) >= start_date, func.DATE(Sale.sale_date) <= end_date)

    # Apply product filter, if specified
    if product_id:
        query = query.join(Inventory).join(Product).filter(Product.id == product_id)

    # Apply category filter, if specified
    if category:
        query = query.join(Inventory).join(Product).filter(Product.category == category)

    # Get all sales data based on the specified filters
    sales_data = query.all()

    # Return the sales data
    return sales_data

#function to get all daily sales data based on dates
def analyze_daily_revenue(db:Session):
    try:
        daily_sales_data = (
            db.query(
                func.DATE(Sale.sale_date).label("date"),
                func.sum(Product.price * Sale.quantity_sold).label("total_revenue")
            )
            .join(Inventory, Inventory.id == Sale.inventory_id)
            .join(Product, Product.id == Inventory.product_id)
            .group_by(func.DATE(Sale.sale_date))
            .all()
        )

        result = [
            {"date": str(row.date), "total_revenue": row.total_revenue}
            for row in daily_sales_data
        ]

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# function to get all the weekly sales data abased on date range i.e 7 days
def analyze_weekly_revenue(db:Session):
    try:
        weekly_sales_data = (
            db.query(
                func.WEEK(Sale.sale_date).label("week"),
                func.MIN(func.DATE(Sale.sale_date)).label("start_date"),
                func.MAX(func.DATE(Sale.sale_date)).label("end_date"),
                func.sum(Product.price * Sale.quantity_sold).label("total_revenue")
            )
            .join(Inventory, Inventory.id == Sale.inventory_id)
            .join(Product, Product.id == Inventory.product_id)
            .group_by(func.WEEK(Sale.sale_date))
            .all()
        )

        result = [
            {
                "start_date": str(row.start_date),
                "end_date": str(row.end_date),
                "total_revenue": row.total_revenue
            }
            for row in weekly_sales_data
        ]

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
#function to get all the monthly sales based on 1-month
def analyze_monthly_revenue(db: Session ):
    try:
        monthly_sales_data = (
            db.query(
                func.MONTH(Sale.sale_date).label("month"),
                func.MIN(func.DATE(Sale.sale_date)).label("start_date"),
                func.MAX(func.DATE(Sale.sale_date)).label("end_date"),
                func.sum(Product.price * Sale.quantity_sold).label("total_revenue")
            )
            .join(Inventory, Inventory.id == Sale.inventory_id)
            .join(Product, Product.id == Inventory.product_id)
            .group_by(func.MONTH(Sale.sale_date))
            .all()
        )

        result = [
            {
                "month": row.month,
                "start_date": str(row.start_date),
                "end_date": str(row.end_date),
                "total_revenue": row.total_revenue
            }
            for row in monthly_sales_data
        ]

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def analyze_annual_revenue(db: Session):
    try:
        annual_sales_data = (
            db.query(
                func.YEAR(Sale.sale_date).label("year"),
                func.MIN(func.DATE(Sale.sale_date)).label("start_date"),
                func.MAX(func.DATE(Sale.sale_date)).label("end_date"),
                func.sum(Product.price * Sale.quantity_sold).label("total_revenue")
            )
            .join(Inventory, Inventory.id == Sale.inventory_id)
            .join(Product, Product.id == Inventory.product_id)
            .group_by(func.YEAR(Sale.sale_date))
            .all()
        )

        result = [
            {
                "year": row.year,
                "start_date": str(row.start_date),
                "end_date": str(row.end_date),
                "total_revenue": row.total_revenue
            }
            for row in annual_sales_data
        ]

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



