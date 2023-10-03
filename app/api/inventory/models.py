from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.types import Enum as SQLAlchemyEnum
from enum import Enum
from sqlalchemy.sql import func
from db.base import Base
from db.session import engine


# Define an enumeration for inventory statuses
class InventoryStatus(Enum):
    AVAILABLE = "Available"
    OUT_OF_STOCK = "Out of Stock"
    IN_TRANSIT = "In Transit"
    DAMAGED = "Damaged"
    RESERVED = "Reserved"
    DISCONTINUED = "Discontinued"
    LOW = "Low"

# Define the Inventory model (tracks the current state of inventory for each product)
class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    product = Column(ForeignKey("products.id"))
    quantity = Column(Integer)
    last_updated = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    status = Column(SQLAlchemyEnum(InventoryStatus), nullable=False)

# Define the InventoryHistory model (logs historical changes in inventory)
class InventoryHistory(Base):
    __tablename__ = "inventory_history"
    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(ForeignKey("inventory.id"))
    quantity = Column(Integer)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    status = Column(SQLAlchemyEnum(InventoryStatus), nullable=False)

# Try to create tables using the defined models and bind them to the engine
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    # If an exception occurs during table creation, print an error message
    print("Error creating tables:", e)