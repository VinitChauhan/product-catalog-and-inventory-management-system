from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models, data_access as data_access, schemas, auth
from models import UserRole

def init_db():
    """Initialize database with tables and sample data."""
    # Create all tables
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if admin user already exists
        admin_user = data_access.get_user_by_username(db, username="admin")
        if not admin_user:
            # Create admin user
            admin_user_data = schemas.UserCreate(
                username="admin",
                email="admin@example.com",
                password="admin123",
                full_name="System Administrator",
                role=UserRole.ADMIN
            )
            hashed_password = auth.get_password_hash(admin_user_data.password)
            data_access.create_user(db=db, user=admin_user_data, hashed_password=hashed_password)
            print("Admin user created successfully")
        
        # Create sample categories
        categories_data = [
            {"name": "Electronics", "description": "Electronic devices and accessories"},
            {"name": "Clothing", "description": "Apparel and fashion items"},
            {"name": "Books", "description": "Books and publications"},
            {"name": "Home & Garden", "description": "Home improvement and garden items"},
        ]
        
        for cat_data in categories_data:
            existing_cat = db.query(models.Category).filter(models.Category.name == cat_data["name"]).first()
            if not existing_cat:
                category = models.Category(**cat_data)
                db.add(category)
                print(f"Category '{cat_data['name']}' created")
        
        db.commit()
        
        # Create sample products
        products_data = [
            {
                "sku": "LAPTOP001",
                "name": "Gaming Laptop",
                "description": "High-performance gaming laptop with RTX graphics",
                "price": 1299.99,
                "cost_price": 899.99,
                "category_id": 1,
                "brand": "GamingTech",
                "model": "GT-5000",
                "weight": 2.5,
                "dimensions": "15.6 x 10.2 x 0.8 inches"
            },
            {
                "sku": "PHONE001",
                "name": "Smartphone",
                "description": "Latest smartphone with advanced camera system",
                "price": 799.99,
                "cost_price": 549.99,
                "category_id": 1,
                "brand": "TechMobile",
                "model": "TM-2024",
                "weight": 0.18,
                "dimensions": "6.1 x 3.0 x 0.3 inches"
            },
            {
                "sku": "SHIRT001",
                "name": "Cotton T-Shirt",
                "description": "Comfortable cotton t-shirt in various colors",
                "price": 24.99,
                "cost_price": 12.99,
                "category_id": 2,
                "brand": "FashionWear",
                "model": "CW-100",
                "weight": 0.2,
                "dimensions": "M"
            }
        ]
        
        for prod_data in products_data:
            existing_prod = data_access.get_product_by_sku(db, sku=prod_data["sku"])
            if not existing_prod:
                product = models.Product(**prod_data)
                db.add(product)
                print(f"Product '{prod_data['name']}' created")
        
        db.commit()
        
        # Create sample suppliers
        suppliers_data = [
            {
                "name": "Tech Supplies Inc.",
                "contact_person": "John Smith",
                "email": "john@techsupplies.com",
                "phone": "+1-555-0123",
                "address": "123 Tech Street, Silicon Valley, CA"
            },
            {
                "name": "Fashion Wholesale Co.",
                "contact_person": "Sarah Johnson",
                "email": "sarah@fashionwholesale.com",
                "phone": "+1-555-0456",
                "address": "456 Fashion Ave, New York, NY"
            }
        ]
        
        for sup_data in suppliers_data:
            existing_sup = db.query(models.Supplier).filter(models.Supplier.name == sup_data["name"]).first()
            if not existing_sup:
                supplier = models.Supplier(**sup_data)
                db.add(supplier)
                print(f"Supplier '{sup_data['name']}' created")
        
        db.commit()
        
        # Create sample customers
        customers_data = [
            {
                "name": "Alice Johnson",
                "email": "alice@example.com",
                "phone": "+1-555-0789",
                "address": "789 Customer St, Anytown, USA"
            },
            {
                "name": "Bob Wilson",
                "email": "bob@example.com",
                "phone": "+1-555-0321",
                "address": "321 Client Ave, Somewhere, USA"
            }
        ]
        
        for cust_data in customers_data:
            existing_cust = db.query(models.Customer).filter(models.Customer.email == cust_data["email"]).first()
            if not existing_cust:
                customer = models.Customer(**cust_data)
                db.add(customer)
                print(f"Customer '{cust_data['name']}' created")
        
        db.commit()
        
        print("Database initialization completed successfully!")
        
    except Exception as e:
        print(f"Error during database initialization: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
