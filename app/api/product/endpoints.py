from fastapi import APIRouter, Depends, HTTPException, UploadFile,File
from sqlalchemy.orm import Session
from db.session import get_db
from api.product.schemas import CreateProduct, GetProduct
from api.inventory.schemas import CreateInventory
from api.inventory.models import InventoryStatus
from api.product import cruds as product_cruds
from api.inventory import cruds as inventory_cruds



router = APIRouter()

# ------------------------------ Product Routes -------------------------------------------------------

@router.post("/create_product", response_model=GetProduct)
async def create_product(product: CreateProduct, db: Session = Depends(get_db)):
    """
    Create a new product.

    Args:
        product (CreateProduct): Data for creating a product.
        db (Session): Database session.

    Returns:
        GetProduct: Created product.
    """
    
    new_product = product_cruds.create_product(db, product.model_dump())

    if new_product is None:
        raise HTTPException(400,detail="Could not create product")
    
    inventory = CreateInventory(product_id=new_product.id,
                                quantity=product.quantity,
                                status=InventoryStatus.AVAILABLE)    
    new_inventory = inventory_cruds.create_inventory(db, inventory.model_dump())

    if new_inventory is None:
        raise HTTPException(400,detail="Could not create inventory")
    
    return new_product

@router.delete('/delete/{product_id}',response_model=GetProduct)
def delete_product(product_id,db:Session = Depends(get_db)):
    """
    Delete a product (deleting the product will also delete corresponding inventory and its history)
    
    Args:
        product_id (int): ID of the product to be deleted
    
    Returns:
        GetProduct: The deleted product details.
    
    Raises:
        HTTException: If the product is not deleted or found
    """
    product = product_cruds.get_product_by_id(db,product_id)
    if product is None:
        raise HTTPException(400,detail="Could not find product")
    product_cruds.delete_product(db,product)
    return product
    
@router.post('/upload/product_image',response_model=GetProduct)
async def upload_product_image(product_id:int,image:UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload an image for a product.

    Args:
        product_id (int): ID of the product.
        image (UploadFile): The image file to upload.
        db (Session): Database session.

    Returns:
        GetProduct: The updated product details.

    Raises:
        HTTPException: If the product is not found.
    """
    product = product_cruds.get_product_by_id(db,product_id)
    if product is None:
        raise HTTPException(400,detail="Could not find product")
    updated_product = product_cruds.upload_product_image(db = db ,image = image,product=product)
    return updated_product

@router.get("/products")
async def get_all_products(db: Session = Depends(get_db)):
    """
    Get all products.

    Args:
        db (Session): Database session.

    Returns:
        List[GetProduct]: List of products.
    """
    return product_cruds.get_all_products(db)
