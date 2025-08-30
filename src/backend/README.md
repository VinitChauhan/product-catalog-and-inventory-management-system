# Inventory Management System Backend

A comprehensive FastAPI backend for product catalog and inventory management with MySQL database support.

## Features

- **User Management**: Authentication, authorization, and role-based access control
- **Product Catalog**: Complete CRUD operations for products with categories
- **Inventory Management**: Real-time stock tracking with transactions
- **Supplier Management**: Manage suppliers and purchase orders
- **Customer Management**: Customer information and order tracking
- **Order Management**: Sales orders with inventory integration
- **Purchase Orders**: Supplier purchase order management
- **Inventory Transactions**: Complete audit trail of stock movements

## Database Schema

### Core Tables
- **users**: User accounts with roles (admin, manager, staff)
- **categories**: Product categories with hierarchical support
- **products**: Product catalog with SKU, pricing, and specifications
- **inventory**: Real-time stock levels (current, reserved, available)
- **suppliers**: Supplier information and contact details
- **customers**: Customer information and contact details
- **orders**: Sales orders with customer and user tracking
- **order_items**: Individual items in sales orders
- **purchase_orders**: Supplier purchase orders
- **purchase_order_items**: Items in purchase orders
- **inventory_transactions**: Complete audit trail of stock movements

## Setup Instructions

### Prerequisites
- Python 3.11+
- MySQL 8.0+
- pip

### Installation

1. **Clone the repository**
   ```bash
   cd src/backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env_example.txt .env
   # Edit .env with your database credentials
   ```

4. **Create MySQL database**
   ```sql
   CREATE DATABASE inventory_management;
   ```

5. **Initialize the database**
   ```bash
   python init_db.py
   ```

6. **Run the application**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Interactive API docs**: `http://localhost:8000/docs`
- **ReDoc documentation**: `http://localhost:8000/redoc`

## Authentication

The API uses JWT tokens for authentication. To get a token:

```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

Use the returned token in the Authorization header:
```
Authorization: Bearer <your-token>
```

## Default Admin User

After running `init_db.py`, you can log in with:
- **Username**: admin
- **Password**: admin123
- **Role**: ADMIN

## API Endpoints

### Authentication
- `POST /token` - Get access token

### Users
- `POST /users/` - Create user
- `GET /users/` - List users
- `GET /users/{user_id}` - Get user details
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

### Categories
- `POST /categories/` - Create category
- `GET /categories/` - List categories
- `GET /categories/{category_id}` - Get category details
- `PUT /categories/{category_id}` - Update category
- `DELETE /categories/{category_id}` - Delete category

### Products
- `POST /products/` - Create product
- `GET /products/` - List products (with search and filtering)
- `GET /products/{product_id}` - Get product details
- `PUT /products/{product_id}` - Update product
- `DELETE /products/{product_id}` - Delete product

### Inventory
- `GET /inventory/` - List all inventory
- `GET /inventory/{product_id}` - Get product inventory
- `PUT /inventory/{product_id}` - Update inventory
- `GET /inventory/low-stock/` - Get low stock products

### Suppliers
- `POST /suppliers/` - Create supplier
- `GET /suppliers/` - List suppliers
- `GET /suppliers/{supplier_id}` - Get supplier details
- `PUT /suppliers/{supplier_id}` - Update supplier
- `DELETE /suppliers/{supplier_id}` - Delete supplier

### Customers
- `POST /customers/` - Create customer
- `GET /customers/` - List customers
- `GET /customers/{customer_id}` - Get customer details
- `PUT /customers/{customer_id}` - Update customer
- `DELETE /customers/{customer_id}` - Delete customer

### Orders
- `POST /orders/` - Create order
- `GET /orders/` - List orders
- `GET /orders/{order_id}` - Get order details
- `PUT /orders/{order_id}` - Update order
- `DELETE /orders/{order_id}` - Delete order

### Purchase Orders
- `POST /purchase-orders/` - Create purchase order
- `GET /purchase-orders/` - List purchase orders
- `GET /purchase-orders/{po_id}` - Get purchase order details
- `PUT /purchase-orders/{po_id}` - Update purchase order
- `DELETE /purchase-orders/{po_id}` - Delete purchase order

### Inventory Transactions
- `POST /inventory-transactions/` - Create inventory transaction
- `GET /inventory-transactions/` - List inventory transactions

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DB_USER` | MySQL username | root |
| `DB_PASSWORD` | MySQL password | password |
| `DB_HOST` | MySQL host | localhost |
| `DB_PORT` | MySQL port | 3306 |
| `DB_NAME` | Database name | inventory_management |
| `SECRET_KEY` | JWT secret key | your-secret-key-here |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | 30 |

## Docker Support

The application includes a Dockerfile for containerized deployment:

```bash
# Build the image
docker build -t inventory-backend .

# Run the container
docker run -p 8000:8000 inventory-backend
```

## Security Features

- **Password Hashing**: BCrypt for secure password storage
- **JWT Authentication**: Stateless authentication with tokens
- **Role-based Access**: Different permissions for admin, manager, and staff
- **Input Validation**: Pydantic models for request validation
- **SQL Injection Protection**: SQLAlchemy ORM with parameterized queries

## Error Handling

The API includes comprehensive error handling:
- **400 Bad Request**: Invalid input data
- **401 Unauthorized**: Missing or invalid authentication
- **404 Not Found**: Resource not found
- **422 Validation Error**: Request validation failed

## Development

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest
```

### Code Formatting
```bash
# Install black
pip install black

# Format code
black .
```

## License

This project is licensed under the MIT License.
