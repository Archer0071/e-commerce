import os
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session
from api.product import models

# ------------------------------ Product Functions ------------------------------------------

# Function to create a new product
def create_product(db: Session, product_data):
    """
    Create a new product.

    Args:
        db (Session): Database session.
        product_data (dict): Data for creating the product.

    Returns:
        Product: Created product.
    """
    product_data.pop('quantity')  # Remove 'quantity' from product_data
    db_product = models.Product(**product_data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Function to delete a product
def delete_product(db: Session, product: models.Product):
    """
    Delete a product.

    Args:
        db (Session): Database session.
        product (Product): Product to be deleted.

    Returns:
        dict: Result of the deletion.
    """
    db.delete(product)
    db.commit()
    return {"ok": True}

# Function to upload a product image
def upload_product_image(db: Session, image: UploadFile, product: models.Product):
    """
    Upload a product image.

    Args:
        db (Session): Database session.
        image (UploadFile): Uploaded image file.
        product (Product): Product to associate with the image.

    Returns:
        Product: Updated product with the image path.
    """
    if image:
        upload_dir = "uploads/products"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, image.filename)
        with open(file_path, "wb") as file:
            file.write(image.file.read())
        product.image = file_path
        db.commit()
        db.refresh(product)
        return product

# Function to retrieve all products
def get_all_products(db: Session):
    """
    Get all products.

    Args:
        db (Session): Database session.

    Returns:
        List[Product]: List of all products.
    """
    return db.query(models.Product).all()

# Function to retrieve a product by its ID
def get_product_by_id(db: Session, product_id: int):
    """
    Get a product by its ID.

    Args:
        db (Session): Database session.
        product_id (int): ID of the product.

    Returns:
        Product: Retrieved product.
    """
    return db.query(models.Product).filter(models.Product.id == product_id).first()
