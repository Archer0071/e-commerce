from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.types import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from utils.enums import Category
from db.base import Base
from db.session import engine
from datetime import datetime

# Define the Sale model (represents sales records)
class Sale(Base):
    """
    Represents a sales record.

    Attributes:
        id (int): Primary key.
        inventory_id (int): Foreign key referencing the associated inventory item.
        quantity_sold (int): Quantity of the product sold.
        sale_date (DateTime): Timestamp of the sale.

    Relationships:
        - inventory: Many-to-One relationship with the associated inventory item.
    """
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(Integer, ForeignKey("inventory.id"))
    quantity_sold = Column(Integer)
    sale_date = Column(DateTime(timezone=True), server_default=func.now())
    inventory = relationship('Inventory', back_populates='sales')

# Try to create tables using the defined models and bind them to the engine
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    # If an exception occurs during table creation, print an error message
    print("Error creating tables:", e)
