import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.product import endpoints as product_endpoints
from api.inventory import enpoints as inventory_enpoints
from api.sales import endpoints as sales_endpoints

app = FastAPI()

# directory containing your static files
static_dir = os.path.join(os.getcwd(), "uploads")

# Mount the static files directory
app.mount("/uploads", StaticFiles(directory=static_dir), name="uploads")

# Routes
app.include_router(product_endpoints.router, prefix="/products", tags=["products"])
app.include_router(inventory_enpoints.router,prefix="/inventory",tags=["inventory"])
app.include_router(sales_endpoints.router,prefix="/inventory",tags=["inventory"])
