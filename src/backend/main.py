from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import timedelta
import models, schemas, data_access, auth
from database_connection import engine, get_db
from auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, authenticate_user

app = FastAPI(
    title="Inventory Management System API",
    description="A comprehensive API for product catalog and inventory management",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication endpoints
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    username: str = Query(...),
    password: str = Query(...),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# User endpoints
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = data_access.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = data_access.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    hashed_password = auth.get_password_hash(user.password)
    return data_access.create_user(db=db, user=user, hashed_password=hashed_password)

@app.get("/users/", response_model=List[schemas.User])
def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    users = data_access.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_user = data_access.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_user = data_access.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_user = data_access.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# Category endpoints
@app.post("/categories/", response_model=schemas.Category)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return data_access.create_category(db=db, category=category)

@app.get("/categories/", response_model=List[schemas.Category])
def read_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    categories = data_access.get_categories(db, skip=skip, limit=limit)
    return categories

@app.get("/categories/{category_id}", response_model=schemas.Category)
def read_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    db_category = data_access.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@app.put("/categories/{category_id}", response_model=schemas.Category)
def update_category(
    category_id: int,
    category_update: schemas.CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_category = data_access.update_category(db, category_id=category_id, category_update=category_update)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@app.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_category = data_access.delete_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}

# Product endpoints
@app.post("/products/", response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_product = data_access.get_product_by_sku(db, sku=product.sku)
    if db_product:
        raise HTTPException(status_code=400, detail="SKU already exists")
    return data_access.create_product(db=db, product=product)

@app.get("/products/", response_model=List[schemas.Product])
def read_products(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if search:
        products = data_access.search_products(db, search_term=search, skip=skip, limit=limit)
    else:
        products = data_access.get_products(db, skip=skip, limit=limit, category_id=category_id)
    return products

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    db_product = data_access.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: int,
    product_update: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_product = data_access.update_product(db, product_id=product_id, product_update=product_update)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_product = data_access.delete_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

# Inventory endpoints
@app.get("/inventory/", response_model=List[schemas.Inventory])
def read_inventory(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    inventory = data_access.get_all_inventory(db, skip=skip, limit=limit)
    return inventory

@app.get("/inventory/{product_id}", response_model=schemas.Inventory)
def read_product_inventory(
    product_id: int,
    db: Session = Depends(get_db)
):
    db_inventory = data_access.get_inventory(db, product_id=product_id)
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return db_inventory

@app.put("/inventory/{product_id}", response_model=schemas.Inventory)
def update_inventory(
    product_id: int,
    inventory_update: schemas.InventoryUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_inventory = data_access.update_inventory(db, product_id=product_id, inventory_update=inventory_update)
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return db_inventory

@app.get("/inventory/low-stock/", response_model=List[schemas.Inventory])
def get_low_stock_products(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return data_access.get_low_stock_products(db)

# Supplier endpoints
@app.post("/suppliers/", response_model=schemas.Supplier)
def create_supplier(
    supplier: schemas.SupplierCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return data_access.create_supplier(db=db, supplier=supplier)

@app.get("/suppliers/", response_model=List[schemas.Supplier])
def read_suppliers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    suppliers = data_access.get_suppliers(db, skip=skip, limit=limit)
    return suppliers

@app.get("/suppliers/{supplier_id}", response_model=schemas.Supplier)
def read_supplier(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    db_supplier = data_access.get_supplier(db, supplier_id=supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier

@app.put("/suppliers/{supplier_id}", response_model=schemas.Supplier)
def update_supplier(
    supplier_id: int,
    supplier_update: schemas.SupplierUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_supplier = data_access.update_supplier(db, supplier_id=supplier_id, supplier_update=supplier_update)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return db_supplier

@app.delete("/suppliers/{supplier_id}")
def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_supplier = data_access.delete_supplier(db, supplier_id=supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return {"message": "Supplier deleted successfully"}

# Customer endpoints
@app.post("/customers/", response_model=schemas.Customer)
def create_customer(
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return data_access.create_customer(db=db, customer=customer)

@app.get("/customers/", response_model=List[schemas.Customer])
def read_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    customers = data_access.get_customers(db, skip=skip, limit=limit)
    return customers

@app.get("/customers/{customer_id}", response_model=schemas.Customer)
def read_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    db_customer = data_access.get_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.put("/customers/{customer_id}", response_model=schemas.Customer)
def update_customer(
    customer_id: int,
    customer_update: schemas.CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_customer = data_access.update_customer(db, customer_id=customer_id, customer_update=customer_update)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@app.delete("/customers/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_customer = data_access.delete_customer(db, customer_id=customer_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted successfully"}

# Order endpoints
@app.post("/orders/", response_model=schemas.Order)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return data_access.create_order(db=db, order=order, user_id=current_user.id)

@app.get("/orders/", response_model=List[schemas.Order])
def read_orders(
    skip: int = 0,
    limit: int = 100,
    customer_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    orders = data_access.get_orders(db, skip=skip, limit=limit, customer_id=customer_id)
    return orders

@app.get("/orders/{order_id}", response_model=schemas.Order)
def read_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_order = data_access.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@app.put("/orders/{order_id}", response_model=schemas.Order)
def update_order(
    order_id: int,
    order_update: schemas.OrderUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_order = data_access.update_order(db, order_id=order_id, order_update=order_update)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@app.delete("/orders/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_order = data_access.delete_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}

# Purchase Order endpoints
@app.post("/purchase-orders/", response_model=schemas.PurchaseOrder)
def create_purchase_order(
    po: schemas.PurchaseOrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    return data_access.create_purchase_order(db=db, po=po, user_id=current_user.id)

@app.get("/purchase-orders/", response_model=List[schemas.PurchaseOrder])
def read_purchase_orders(
    skip: int = 0,
    limit: int = 100,
    supplier_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    pos = data_access.get_purchase_orders(db, skip=skip, limit=limit, supplier_id=supplier_id)
    return pos

@app.get("/purchase-orders/{po_id}", response_model=schemas.PurchaseOrder)
def read_purchase_order(
    po_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_po = data_access.get_purchase_order(db, po_id=po_id)
    if db_po is None:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    return db_po

@app.put("/purchase-orders/{po_id}", response_model=schemas.PurchaseOrder)
def update_purchase_order(
    po_id: int,
    po_update: schemas.PurchaseOrderUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_po = data_access.update_purchase_order(db, po_id=po_id, po_update=po_update)
    if db_po is None:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    return db_po

@app.delete("/purchase-orders/{po_id}")
def delete_purchase_order(
    po_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_po = data_access.delete_purchase_order(db, po_id=po_id)
    if db_po is None:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    return {"message": "Purchase order deleted successfully"}

# Inventory Transaction endpoints
@app.post("/inventory-transactions/", response_model=schemas.InventoryTransaction)
def create_inventory_transaction(
    transaction: schemas.InventoryTransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    db_transaction = data_access.create_inventory_transaction(db=db, transaction=transaction, user_id=current_user.id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_transaction

@app.get("/inventory-transactions/", response_model=List[schemas.InventoryTransaction])
def read_inventory_transactions(
    skip: int = 0,
    limit: int = 100,
    product_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    transactions = data_access.get_inventory_transactions(db, skip=skip, limit=limit, product_id=product_id)
    return transactions

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Inventory Management System API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
