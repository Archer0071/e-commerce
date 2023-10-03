import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.product import endpoints as product_endpoints
from api.inventory import endpoints as inventory_enpoints
from api.sales import endpoints as sales_enpoints
from db.session import SessionLocal

app = FastAPI()

# Get the value of the environment variable (default to "development" if not set)
environment = os.getenv("ENVIRONMENT", "development")

# Conditionally serve static files only in non-production environments
if environment != "production":
    # Directory containing your static files (assuming uploads directory is in the same directory as main.py)
    static_dir = os.path.join(os.path.dirname(__file__), "uploads")

    # Check if the directory exists before mounting
    if os.path.exists(static_dir):
        # Mount the static files directory
        app.mount("/uploads", StaticFiles(directory=static_dir), name="uploads")
    else:
        print(f"Warning: The directory '{static_dir}' does not exist. Static files will not be served.")

# Routes
app.include_router(product_endpoints.router, tags=["Products"])
app.include_router(inventory_enpoints.router, tags=["Inventory"])
app.include_router(sales_enpoints.router, tags=["Sales"])

if __name__ == '__main__':
    uvicorn.run(app)