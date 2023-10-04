from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.types import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from utils.enums import Category
from db.base import Base
from db.session import engine
from datetime import datetime


class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True, index=True)
    
    # Modify ForeignKey to reference the correct column in Inventory
    inventory_id = Column(Integer, ForeignKey("inventory.id"))

    quantity_sold = Column(Integer)
    sale_date = Column(DateTime(timezone=True), server_default=func.now())

    # Define the relationship with Inventory
    inventory = relationship('Inventory', back_populates='sales')

# Try to create tables using the defined models and bind them to the engine
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    # If an exception occurs during table creation, print an error message
    print("Error creating tables:", e)