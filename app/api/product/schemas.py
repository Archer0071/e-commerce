# app/api/product/schemas.py

from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True