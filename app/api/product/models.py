from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.types import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from utils.enums import Category
from db.base import Base
from db.session import engine


# Define the Product model (represents products in the inventory)
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255))
    price = Column(Float, index=True)
    category = Column(SQLAlchemyEnum(Category), nullable=False)
    image = Column(String(255), index=True)
# Define the relationship with Inventory
    inventory = relationship('Inventory', cascade='all, delete-orphan')

# Try to create tables using the defined models and bind them to the engine
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    # If an exception occurs during table creation, print an error message
    print("Error creating tables:", e)