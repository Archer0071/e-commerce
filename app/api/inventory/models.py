from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.types import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from utils.enums import InventoryStatus
from sqlalchemy.sql import func
from db.base import Base
from db.session import engine

# Define the Inventory model (tracks the current state of inventory for each product)
class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(ForeignKey("products.id", ondelete='CASCADE'), unique=True)  # Ensure unique constraint for one-to-one
    quantity = Column(Integer)
    last_updated = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    status = Column(SQLAlchemyEnum(InventoryStatus), nullable=False)

    # Define the relationship with Product
    product = relationship('Product', back_populates='inventory')

    # Define the relationship with Sale (One-to-Many relationship)
    sales = relationship('Sale', back_populates='inventory')

    # Define the relationship with InventoryHistory (One-to-Many relationship)
    history = relationship('InventoryHistory', back_populates='inventory')


# Define the InventoryHistory model (logs historical changes in inventory)
class InventoryHistory(Base):
    __tablename__ = "inventory_history"
    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(ForeignKey("inventory.id", ondelete='CASCADE'))
    quantity = Column(Integer)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    status = Column(SQLAlchemyEnum(InventoryStatus), nullable=False)

    # Define the relationship with Inventory
    inventory = relationship('Inventory', back_populates='history')


# Try to create tables using the defined models and bind them to the engine
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    # If an exception occurs during table creation, print an error message
    print("Error creating tables:", e)