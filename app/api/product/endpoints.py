from fastapi import APIRouter, Depends, HTTPException, UploadFile,File
from sqlalchemy.orm import Session
from db.session import get_db
from product.schemas import CreateProduct, GetProduct
from inventory.schemas import CreateInventory
from inventory.models import InventoryStatus
from product import cruds



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
    
    new_product = cruds.create_product(db, product.model_dump())
    inventory = CreateInventory(product=new_product.id,
                                quantity=product.quantity,
                                status=InventoryStatus.AVAILABLE)
    
    product_id = inventory.product
    product = cruds.get_product_by_id(db, product_id)

    if not product:
        raise HTTPException(404, detail=f"Product with ID {product_id} not found")

    existing_inventory = cruds.get_inventory_by_product_id(db, product.id)
    if existing_inventory:
        raise HTTPException(400, detail=f"Inventory item for Product ID {product_id} already exists")

     
    new_inventory = cruds.create_inventory(db, inventory.model_dump())
    if new_inventory is None:
        raise HTTPException(400,detail="Could not create inventory")
    return new_product

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
    product = cruds.get_product_by_id(db,product_id)
    if product is None:
        raise HTTPException(400,detail="Could not find product")
    updated_product = cruds.upload_product_image(db = db ,image = image,product=product)
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
    return cruds.get_all_products(db)
