from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from database_connection import Base
import enum

class UserRole(enum.Enum):
    admin = "admin"
    manager = "manager"
    staff = "staff"

class ProductStatus(enum.Enum):
    active = "active"
    inactive = "inactive"
    discontinued = "discontinued"

class OrderStatus(enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class TransactionType(enum.Enum):
    purchase = "purchase"
    sale = "sale"
    return_item = "return"
    adjustment = "adjustment"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.staff)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    orders = relationship("Order", back_populates="user")
    transactions = relationship("InventoryTransaction", back_populates="user")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    products = relationship("Product", back_populates="category")
    subcategories = relationship("Category", backref=backref("parent", remote_side=[id]))

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    cost_price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    brand = Column(String(100))
    model = Column(String(100))
    weight = Column(Float)
    dimensions = Column(String(100))
    status = Column(Enum(ProductStatus), default=ProductStatus.active)
    min_stock_level = Column(Integer, default=0)
    max_stock_level = Column(Integer, default=1000)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    category = relationship("Category", back_populates="products")
    inventory = relationship("Inventory", back_populates="product", uselist=False)
    order_items = relationship("OrderItem", back_populates="product")
    transactions = relationship("InventoryTransaction", back_populates="product")

class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), unique=True, nullable=False)
    current_stock = Column(Integer, default=0, nullable=False)
    reserved_stock = Column(Integer, default=0, nullable=False)
    available_stock = Column(Integer, default=0, nullable=False)
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    product = relationship("Product", back_populates="inventory")

class Supplier(Base):
    __tablename__ = "suppliers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    contact_person = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    address = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(20))
    address = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    orders = relationship("Order", back_populates="customer")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, index=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    total_amount = Column(Float, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    customer = relationship("Customer", back_populates="orders")
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    
    # Relationships
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    
    id = Column(Integer, primary_key=True, index=True)
    po_number = Column(String(50), unique=True, index=True, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    total_amount = Column(Float, nullable=False)
    expected_delivery = Column(DateTime(timezone=True))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    supplier = relationship("Supplier", back_populates="purchase_orders")
    user = relationship("User")
    purchase_order_items = relationship("PurchaseOrderItem", back_populates="purchase_order")

class PurchaseOrderItem(Base):
    __tablename__ = "purchase_order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    purchase_order_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_cost = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)
    
    # Relationships
    purchase_order = relationship("PurchaseOrder", back_populates="purchase_order_items")
    product = relationship("Product")

class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    quantity = Column(Integer, nullable=False)
    previous_stock = Column(Integer, nullable=False)
    new_stock = Column(Integer, nullable=False)
    reference_id = Column(Integer)  # Order ID, Purchase Order ID, etc.
    reference_type = Column(String(50))  # 'order', 'purchase_order', 'adjustment'
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    product = relationship("Product", back_populates="transactions")
    user = relationship("User", back_populates="transactions")
