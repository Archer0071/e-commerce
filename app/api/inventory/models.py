from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.types import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from utils.enums import InventoryStatus
from sqlalchemy.sql import func
from db.base import Base
from db.session import engine

# Define the Inventory model (tracks the current state of inventory for each product)
class Inventory(Base):
    """
    Represents the inventory for a product.

    Attributes:
        id (int): Primary key.
        product_id (int): Foreign key referencing the associated product.
        quantity (int): Current quantity of the product in the inventory.
        last_updated (DateTime): Timestamp of the last update to the inventory.
        status (Enum): Status of the inventory item (e.g., IN_STOCK, OUT_OF_STOCK).

    Relationships:
        - product: One-to-One relationship with the associated product.
        - sales: One-to-Many relationship with sales made for this product.
        - history: One-to-Many relationship with historical changes in inventory.
    """
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(ForeignKey("products.id", ondelete='CASCADE'), unique=True)
    quantity = Column(Integer)
    last_updated = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    status = Column(SQLAlchemyEnum(InventoryStatus), nullable=False)

    product = relationship('Product', back_populates='inventory')
    sales = relationship('Sale', back_populates='inventory')
    history = relationship('InventoryHistory', back_populates='inventory')


# Define the InventoryHistory model (logs historical changes in inventory)
class InventoryHistory(Base):
    """
    Represents the historical changes in inventory.

    Attributes:
        id (int): Primary key.
        inventory_id (int): Foreign key referencing the associated inventory item.
        quantity (int): Quantity at the time of the historical record.
        last_updated (DateTime): Timestamp of the historical record.
        status (Enum): Status of the inventory item at the time of the historical record.

    Relationships:
        - inventory: Many-to-One relationship with the associated inventory item.
    """
    __tablename__ = "inventory_history"
    id = Column(Integer, primary_key=True, index=True)
    inventory_id = Column(ForeignKey("inventory.id", ondelete='CASCADE'))
    quantity = Column(Integer)
    last_updated = Column(DateTime(timezone=True), default=func.now())
    status = Column(SQLAlchemyEnum(InventoryStatus), nullable=False)

    inventory = relationship('Inventory', back_populates='history')


# Try to create tables using the defined models and bind them to the engine
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    # If an exception occurs during table creation, print an error message
    print("Error creating tables:", e)
