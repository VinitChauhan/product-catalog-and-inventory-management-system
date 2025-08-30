from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from models import UserRole, ProductStatus, OrderStatus, TransactionType

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.staff

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Category Schemas
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: Optional[bool] = None

class Category(CategoryBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Product Schemas
class ProductBase(BaseModel):
    sku: str
    name: str
    description: Optional[str] = None
    price: float
    cost_price: float
    category_id: int
    brand: Optional[str] = None
    model: Optional[str] = None
    weight: Optional[float] = None
    dimensions: Optional[str] = None
    min_stock_level: int = 0
    max_stock_level: int = 1000

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    sku: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    cost_price: Optional[float] = None
    category_id: Optional[int] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    weight: Optional[float] = None
    dimensions: Optional[str] = None
    status: Optional[ProductStatus] = None
    min_stock_level: Optional[int] = None
    max_stock_level: Optional[int] = None

class Product(ProductBase):
    id: int
    status: ProductStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    category: Category

    class Config:
        from_attributes = True

# Inventory Schemas
class InventoryBase(BaseModel):
    current_stock: int
    reserved_stock: int
    available_stock: int

class InventoryCreate(InventoryBase):
    product_id: int

class InventoryUpdate(BaseModel):
    current_stock: Optional[int] = None
    reserved_stock: Optional[int] = None
    available_stock: Optional[int] = None

class Inventory(InventoryBase):
    id: int
    product_id: int
    last_updated: Optional[datetime] = None
    product: Product

    class Config:
        from_attributes = True

# Supplier Schemas
class SupplierBase(BaseModel):
    name: str
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None

class Supplier(SupplierBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Customer Schemas
class CustomerBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = None

class Customer(CustomerBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Order Item Schemas
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    total_price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    product: Product

    class Config:
        from_attributes = True

# Order Schemas
class OrderBase(BaseModel):
    customer_id: int
    total_amount: float
    notes: Optional[str] = None

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    total_amount: Optional[float] = None
    notes: Optional[str] = None

class Order(OrderBase):
    id: int
    order_number: str
    user_id: int
    status: OrderStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    customer: Customer
    order_items: List[OrderItem]

    class Config:
        from_attributes = True

# Purchase Order Item Schemas
class PurchaseOrderItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_cost: float
    total_cost: float

class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    pass

class PurchaseOrderItem(PurchaseOrderItemBase):
    id: int
    purchase_order_id: int
    product: Product

    class Config:
        from_attributes = True

# Purchase Order Schemas
class PurchaseOrderBase(BaseModel):
    supplier_id: int
    total_amount: float
    expected_delivery: Optional[datetime] = None
    notes: Optional[str] = None

class PurchaseOrderCreate(PurchaseOrderBase):
    items: List[PurchaseOrderItemCreate]

class PurchaseOrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    total_amount: Optional[float] = None
    expected_delivery: Optional[datetime] = None
    notes: Optional[str] = None

class PurchaseOrder(PurchaseOrderBase):
    id: int
    po_number: str
    user_id: int
    status: OrderStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    supplier: Supplier
    purchase_order_items: List[PurchaseOrderItem]

    class Config:
        from_attributes = True

# Inventory Transaction Schemas
class InventoryTransactionBase(BaseModel):
    product_id: int
    transaction_type: TransactionType
    quantity: int
    reference_id: Optional[int] = None
    reference_type: Optional[str] = None
    notes: Optional[str] = None

class InventoryTransactionCreate(InventoryTransactionBase):
    pass

class InventoryTransaction(InventoryTransactionBase):
    id: int
    user_id: int
    previous_stock: int
    new_stock: int
    created_at: datetime
    product: Product
    user: User

    class Config:
        from_attributes = True

# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Response Schemas
class Message(BaseModel):
    message: str

class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    size: int
    pages: int
