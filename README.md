# E-Commerce API

This repository contains the back-end API for an e-commerce application. The API is designed to power a web admin dashboard for e-commerce managers, providing detailed insights into sales, revenue, and inventory status, as well as allowing the registration of new products. The implementation is done using Python and FastAPI.

## Setup Instructions

To run the API using Docker Compose, follow these steps:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Archer0071/e-commerce.git
   cd e-commerce
   ```

2. **Create Environment File:**

   Create a `.env` file in the root directory and define the required environment variables. For example:

   ```plaintext
   DATABASE_URL=mysql+mysqlconnector://user:password@mysql/dbname
   MYSQL_DATABASE=mydatabase
   MYSQL_USER=myuser
   MYSQL_PASSWORD=mypassword
   MYSQL_ROOT_PASSWORD=myrootpassword
   ENVIRONMENT=development
   ```

   Update the values based on your database setup.

3. **Build and Run with Docker Compose:**

   ```bash
   docker-compose up --build
   ```

   This command will build the Docker images and start the containers.

4. **Access the API:**

   The API will be accessible at `http://localhost:8000`.

## Dependencies

The API uses the following libraries and frameworks:

- **FastAPI:** A modern, fast (high-performance), web framework for building APIs with Python.
- **SQLAlchemy:** A SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **MySQL Connector/Python:** A MySQL database connector for Python.
- **Pydantic:** A data validation and settings management library using Python type hints.
- **Uvicorn:** An ASGI server implementation for running FastAPI applications.

## Database Schema

The database schema includes the following tables:

- **products:** Represents products in the inventory.
- **inventory:** Tracks the current state of inventory for each product.
- **inventory_history:** Logs historical changes in inventory.
- **sales:** Records sales transactions.

The relationships between these tables are defined using foreign keys and are crucial for maintaining data integrity.

## API Endpoints

The API provides the following endpoints:

- **Product Endpoints:**
  - `POST /products/create_product`: Create a new product.
  - `DELETE /products/delete/{product_id}`: Delete a product.
  - `POST /products/upload/product_image`: Upload an image for a product.
  - `GET /products`: Get all products.

- **Sales Endpoints:**
  - `POST /sales/`: Create a new sale record.
  - `GET /sales`: Get sales data based on date range, product, and category filters.
  - `GET /sales/revenue/daily`: Analyze daily revenue.
  - `GET /sales/revenue/weekly`: Analyze weekly revenue.
  - `GET /sales/revenue/monthly`: Analyze monthly revenue.
  - `GET /sales/revenue/annual`: Analyze annual revenue.

- **Inventory Endpoints:**
  - `POST /inventory/create_inventory`: Create a new inventory record.
  - `GET /inventory`: Get all inventory records.
  - `GET /inventory/history/{inventory_id}`: Get the history of inventory changes for a specific product.

Feel free to explore and use these endpoints to manage your e-commerce-inventory application efficiently.

For any issues or inquiries, please contact [adilking0071@gmail.com].