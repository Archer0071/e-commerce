from fastapi import APIRouter, Depends, HTTPException,Query
from sqlalchemy.orm import Session,joinedload
from sqlalchemy import func
from db.session import get_db
from api.sales.models import Sale
from api.product.models import Product
from api.sales import crud as sales_crud
from api.inventory import cruds as inventory_cruds
from api.sales.schemas import SaleCreate, SaleResponse
from datetime import date, timedelta,datetime
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
@router.get("/sales")
def read_sale(db: Session = Depends(get_db)):
    """
    Retrieve a sale record.

    Args:
        db (Session): Database session.

    Returns:
        SaleResponse: Sale record with the specified ID.
    """

    return sales_crud.get_all_sale(db)

# Endpoint to analyze revenue on a daily basis
@router.get("/sales/revenue/daily/")
def analyze_daily_revenue(db: Session = Depends(get_db)):
    """
    Analyze daily revenue.

    Args:
        db (Session): Database session.

    Returns:
        float: Daily revenue.
    """
    total_revenue = 0
    today = date.today()
    daily_sales = db.query(Sale).filter(func.DATE(Sale.sale_date) <= today).all()
    for sale in daily_sales:
        inventory_id  = sale.inventory_id
        product = db.query(Product).filter(Product.id == inventory_id).first()
        product_price = product.price
        total_revenue += product_price
    return {"revnue_daily":total_revenue}

# Endpoint to analyze revenue on a weekly basis
@router.get("/sales/revenue/weekly/", response_model=float)
def analyze_weekly_revenue(db: Session = Depends(get_db)):
    """
    Analyze weekly revenue.

    Args:
        db (Session): Database session.

    Returns:
        float: Weekly revenue.
    """
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    weekly_revenue = db.query(Sale).filter(Sale.date >= start_of_week, Sale.date <= end_of_week).with_entities(Sale.total_price).all()
    return sum(weekly_revenue, 0.0)

# Endpoint to analyze revenue on a monthly basis
@router.get("/sales/revenue/monthly/", response_model=float)
def analyze_monthly_revenue(db: Session = Depends(get_db)):
    """
    Analyze monthly revenue.

    Args:
        db (Session): Database session.

    Returns:
        float: Monthly revenue.
    """
    today = date.today()
    start_of_month = today.replace(day=1)
    end_of_month = today.replace(day=28) + timedelta(days=4)
    end_of_month = end_of_month - timedelta(days=end_of_month.day)
    monthly_revenue = db.query(Sale).filter(Sale.date >= start_of_month, Sale.date <= end_of_month).with_entities(Sale.total_price).all()
    return sum(monthly_revenue, 0.0)

# Endpoint to analyze revenue on an annual basis
@router.get("/sales/revenue/annual/", response_model=float)
def analyze_annual_revenue(db: Session = Depends(get_db)):
    """
    Analyze annual revenue.

    Args:
        db (Session): Database session.

    Returns:
        float: Annual revenue.
    """
    today = date.today()
    start_of_year = today.replace(month=1, day=1)
    end_of_year = today.replace(month=12, day=31)
    annual_revenue = db.query(Sale).filter(Sale.date >= start_of_year, Sale.date <= end_of_year).with_entities(Sale.total_price).all()
    return sum(annual_revenue, 0.0)

# Endpoint to compare revenue across different periods and categories (Example: Weekly revenue for different product categories)
@router.get("/sales/revenue/compare/", response_model=dict)
def compare_revenue_periods_and_categories(db: Session = Depends(get_db)):
    """
    Compare revenue across different periods and categories.

    Args:
        db (Session): Database session.

    Returns:
        dict: Dictionary with keys as periods/categories and values as revenue.
    """
    # Example: You can customize this based on your actual data model and requirements
    comparison_data = {
        "Week1": db.query(Sale).filter(Sale.date >= date(2023, 1, 1), Sale.date <= date(2023, 1, 7)).with_entities(Sale.total_price).all(),
        "Week2": db.query(Sale).filter(Sale.date >= date(2023, 1, 8), Sale.date <= date(2023, 1, 14)).with_entities(Sale.total_price).all(),
        "Category1": db.query(Sale).filter(Sale.category == "Category1").with_entities(Sale.total_price).all(),
        "Category2": db.query(Sale).filter(Sale.category == "Category2").with_entities(Sale.total_price).all(),
    }

    # Summing up revenue for each period/category
    result = {key: sum(value, 0.0) for key, value in comparison_data.items()}
    return result

# Endpoint to provide sales data by date range, product, and category
@router.get("/sales/data/", response_model=List[SaleResponse])
def get_sales_data(
    start_date: date = Query(..., description="Start date of the date range"),
    end_date: date = Query(..., description="End date of the date range"),
    product: str = Query(None, description="Filter by product"),
    category: str = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    """
    Get sales data based on date range, product, and category filters.

    Args:
        start_date (date): Start date of the date range.
        end_date (date): End date of the date range.
        product (str): Optional filter by product.
        category (str): Optional filter by category.
        db (Session): Database session.

    Returns:
        List[SaleResponse]: List of sales records based on the specified filters.
    """
    query = db.query(Sale).filter(Sale.date >= start_date, Sale.date <= end_date)

    if product:
        query = query.filter(Sale.product == product)

    if category:
        query = query.filter(Sale.category == category)

    sales_data = query.all()
    return sales_data
