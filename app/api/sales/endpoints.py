from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from db.session import get_db
from api.sales.models import Sale
from api.product.models import Product
from api.sales import crud as sales_crud
from api.inventory import cruds as inventory_cruds
from api.sales.schemas import SaleCreate, SaleResponse
from api.inventory.models import Inventory
from datetime import date
from utils.enums import Category
from typing import List

router = APIRouter()

# ------------------------ Sales Routes -----------------------------------------------------------

# Endpoint to create a sale
@router.post("/sales/", response_model=SaleResponse)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    """
    Create a new sale record.

    Args:
        sale (SaleCreate): Sale creation data.
        db (Session): Database session.

    Returns:
        SaleResponse: Created sale record.
    """
    # Fetch the corresponding inventory item
    inventory = inventory_cruds.get_inventory_by_id(db,sale.inventory_id)

    if not inventory or inventory.quantity < sale.quantity_sold:
        raise HTTPException(status_code=400, detail="Invalid sale request")
    
    return sales_crud.create_sale(db=db,inventory=inventory, sale=sale)

# Endpoint to retrieve sales
@router.get("/sales", response_model=List[SaleResponse])
def get_sales_data(
    start_date: date = Query(None, description="Start date of the date range (YYYY-MM-DD)"),
    end_date: date = Query(None, description="End date of the date range (YYYY-MM-DD)"),
    product_id: int = Query(None, description="Filter by product ID"),
    category: Category = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    """
    Get sales data based on date range, product, and category filters.

    Args:
        start_date (date): Start date of the date range (optional).
        end_date (date): End date of the date range (optional).
        product (str): Optional filter by product ID.
        category (Category): Optional filter by category.
        db (Session): Database session.

    Returns:
        List[SaleResponse]: List of sales records based on the specified filters.
    """
    return sales_crud.get_all_sale(db,start_date,end_date,product_id,category)
   
# Endpoint to analyze revenue on a daily basis
@router.get("/sales/revenue/daily/")
def analyze_daily_revenue(db: Session = Depends(get_db)):
    """
    Analyze daily revenue.

    Args:
        db (Session): Database session.

    Returns:
        List[Dict[str, Union[str, float]]]: List of daily revenue entries.
    """
    return sales_crud.analyze_daily_revenue(db)

@router.get("/sales/revenue/weekly/")
def analyze_weekly_revenue(db: Session = Depends(get_db)):
    """
    Analyze weekly revenue.

    Args:
        db (Session): Database session.

    Returns:
        List[Dict[str, Union[str, float]]]: List of weekly revenue entries.
    """
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

# Endpoint to analyze revenue on a monthly basis
@router.get("/sales/revenue/monthly/")
def analyze_monthly_revenue(db: Session = Depends(get_db)):
    """
    Analyze monthly revenue.

    Args:
        db (Session): Database session.

    Returns:
        List[Dict[str, Union[str, float]]]: List of monthly revenue entries.
    """
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

# Endpoint to analyze revenue on an annual basis
@router.get("/sales/revenue/annual/")
def analyze_annual_revenue(db: Session = Depends(get_db)):
    """
    Analyze annual revenue.

    Args:
        db (Session): Database session.

    Returns:
        List[Dict[str, Union[str, float]]]: List of annual revenue entries.
    """
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
