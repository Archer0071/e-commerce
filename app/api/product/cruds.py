import os
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from api.product import models

# ------------------------------ Product Functions ------------------------------------------

# Function to create a new product
def create_product(db: Session, product_data):
    product_data.pop('quantity')
    db_product = models.Product(**product_data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product:models.Product):
    db.delete(product)
    db.commit()
    return {"ok": True}




# Function to create a product image
def upload_product_image(db:Session,image:UploadFile,product:models.Product):
    if image:
        upload_dir = "uploads/products"
        os.makedirs(upload_dir,exist_ok=True)
        file_path = os.path.join(upload_dir, image.filename)
        with open(file_path, "wb") as file:
            file.write(image.file.read())
        product.image = file_path
        db.commit()
        db.refresh(product)
        return product
# Function to retrieve all products
def get_all_products(db: Session):
    return db.query(models.Product).all()

# Function to retrieve a product by its ID
def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

