from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional
import models, schemas
from datetime import datetime
import uuid

# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# Category CRUD operations
def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category_update: schemas.CategoryUpdate):
    db_category = get_category(db, category_id)
    if db_category:
        update_data = category_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_category, field, value)
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category

# Product CRUD operations
def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product_by_sku(db: Session, sku: str):
    return db.query(models.Product).filter(models.Product.sku == sku).first()

def get_products(db: Session, skip: int = 0, limit: int = 100, category_id: Optional[int] = None):
    query = db.query(models.Product)
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    return query.offset(skip).limit(limit).all()

def search_products(db: Session, search_term: str, skip: int = 0, limit: int = 100):
    return db.query(models.Product).filter(
        or_(
            models.Product.name.contains(search_term),
            models.Product.sku.contains(search_term),
            models.Product.description.contains(search_term)
        )
    ).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # Create inventory record for the product
    db_inventory = models.Inventory(
        product_id=db_product.id,
        current_stock=0,
        reserved_stock=0,
        available_stock=0
    )
    db.add(db_inventory)
    db.commit()
    
    return db_product

def update_product(db: Session, product_id: int, product_update: schemas.ProductUpdate):
    db_product = get_product(db, product_id)
    if db_product:
        update_data = product_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_product, field, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

# Inventory CRUD operations
def get_inventory(db: Session, product_id: int):
    return db.query(models.Inventory).filter(models.Inventory.product_id == product_id).first()

def get_all_inventory(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Inventory).offset(skip).limit(limit).all()

def get_low_stock_products(db: Session):
    return db.query(models.Inventory).join(models.Product).filter(
        models.Inventory.current_stock <= models.Product.min_stock_level
    ).all()

def update_inventory(db: Session, product_id: int, inventory_update: schemas.InventoryUpdate):
    db_inventory = get_inventory(db, product_id)
    if db_inventory:
        update_data = inventory_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_inventory, field, value)
        db_inventory.available_stock = db_inventory.current_stock - db_inventory.reserved_stock
        db.commit()
        db.refresh(db_inventory)
    return db_inventory

# Supplier CRUD operations
def get_supplier(db: Session, supplier_id: int):
    return db.query(models.Supplier).filter(models.Supplier.id == supplier_id).first()

def get_suppliers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Supplier).offset(skip).limit(limit).all()

def create_supplier(db: Session, supplier: schemas.SupplierCreate):
    db_supplier = models.Supplier(**supplier.dict())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

def update_supplier(db: Session, supplier_id: int, supplier_update: schemas.SupplierUpdate):
    db_supplier = get_supplier(db, supplier_id)
    if db_supplier:
        update_data = supplier_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_supplier, field, value)
        db.commit()
        db.refresh(db_supplier)
    return db_supplier

def delete_supplier(db: Session, supplier_id: int):
    db_supplier = get_supplier(db, supplier_id)
    if db_supplier:
        db.delete(db_supplier)
        db.commit()
    return db_supplier

# Customer CRUD operations
def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Customer).offset(skip).limit(limit).all()

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: int, customer_update: schemas.CustomerUpdate):
    db_customer = get_customer(db, customer_id)
    if db_customer:
        update_data = customer_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_customer, field, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int):
    db_customer = get_customer(db, customer_id)
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return db_customer

# Order CRUD operations
def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100, customer_id: Optional[int] = None):
    query = db.query(models.Order)
    if customer_id:
        query = query.filter(models.Order.customer_id == customer_id)
    return query.offset(skip).limit(limit).all()

def create_order(db: Session, order: schemas.OrderCreate, user_id: int):
    # Generate order number
    order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
    
    db_order = models.Order(
        order_number=order_number,
        customer_id=order.customer_id,
        user_id=user_id,
        total_amount=order.total_amount,
        notes=order.notes
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Create order items
    for item in order.items:
        db_order_item = models.OrderItem(
            order_id=db_order.id,
            **item.dict()
        )
        db.add(db_order_item)
        
        # Update inventory
        inventory = get_inventory(db, item.product_id)
        if inventory:
            inventory.reserved_stock += item.quantity
            inventory.available_stock = inventory.current_stock - inventory.reserved_stock
    
    db.commit()
    return db_order

def update_order(db: Session, order_id: int, order_update: schemas.OrderUpdate):
    db_order = get_order(db, order_id)
    if db_order:
        update_data = order_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_order, field, value)
        db.commit()
        db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id)
    if db_order:
        # Release reserved inventory
        for item in db_order.order_items:
            inventory = get_inventory(db, item.product_id)
            if inventory:
                inventory.reserved_stock -= item.quantity
                inventory.available_stock = inventory.current_stock - inventory.reserved_stock
        
        db.delete(db_order)
        db.commit()
    return db_order

# Purchase Order CRUD operations
def get_purchase_order(db: Session, po_id: int):
    return db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == po_id).first()

def get_purchase_orders(db: Session, skip: int = 0, limit: int = 100, supplier_id: Optional[int] = None):
    query = db.query(models.PurchaseOrder)
    if supplier_id:
        query = query.filter(models.PurchaseOrder.supplier_id == supplier_id)
    return query.offset(skip).limit(limit).all()

def create_purchase_order(db: Session, po: schemas.PurchaseOrderCreate, user_id: int):
    # Generate PO number
    po_number = f"PO-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
    
    db_po = models.PurchaseOrder(
        po_number=po_number,
        supplier_id=po.supplier_id,
        user_id=user_id,
        total_amount=po.total_amount,
        expected_delivery=po.expected_delivery,
        notes=po.notes
    )
    db.add(db_po)
    db.commit()
    db.refresh(db_po)
    
    # Create PO items
    for item in po.items:
        db_po_item = models.PurchaseOrderItem(
            purchase_order_id=db_po.id,
            **item.dict()
        )
        db.add(db_po_item)
    
    db.commit()
    return db_po

def update_purchase_order(db: Session, po_id: int, po_update: schemas.PurchaseOrderUpdate):
    db_po = get_purchase_order(db, po_id)
    if db_po:
        update_data = po_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_po, field, value)
        db.commit()
        db.refresh(db_po)
    return db_po

def delete_purchase_order(db: Session, po_id: int):
    db_po = get_purchase_order(db, po_id)
    if db_po:
        db.delete(db_po)
        db.commit()
    return db_po

# Inventory Transaction CRUD operations
def create_inventory_transaction(db: Session, transaction: schemas.InventoryTransactionCreate, user_id: int):
    # Get current inventory
    inventory = get_inventory(db, transaction.product_id)
    if not inventory:
        return None
    
    previous_stock = inventory.current_stock
    
    # Update inventory based on transaction type
    if transaction.transaction_type == models.TransactionType.PURCHASE:
        inventory.current_stock += transaction.quantity
    elif transaction.transaction_type == models.TransactionType.SALE:
        inventory.current_stock -= transaction.quantity
        inventory.reserved_stock -= transaction.quantity
    elif transaction.transaction_type == models.TransactionType.RETURN:
        inventory.current_stock += transaction.quantity
    elif transaction.transaction_type == models.TransactionType.ADJUSTMENT:
        inventory.current_stock = transaction.quantity
    
    inventory.available_stock = inventory.current_stock - inventory.reserved_stock
    
    # Create transaction record
    db_transaction = models.InventoryTransaction(
        product_id=transaction.product_id,
        user_id=user_id,
        transaction_type=transaction.transaction_type,
        quantity=transaction.quantity,
        previous_stock=previous_stock,
        new_stock=inventory.current_stock,
        reference_id=transaction.reference_id,
        reference_type=transaction.reference_type,
        notes=transaction.notes
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    return db_transaction

def get_inventory_transactions(db: Session, skip: int = 0, limit: int = 100, product_id: Optional[int] = None):
    query = db.query(models.InventoryTransaction)
    if product_id:
        query = query.filter(models.InventoryTransaction.product_id == product_id)
    return query.order_by(models.InventoryTransaction.created_at.desc()).offset(skip).limit(limit).all()
