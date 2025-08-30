-- Initialize database with tables and sample data for Inventory Management System

-- Create tables
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role ENUM('admin', 'manager', 'staff') DEFAULT 'staff',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    parent_id INT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES categories(id)
);

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    cost_price DECIMAL(10,2) NOT NULL,
    category_id INT NOT NULL,
    brand VARCHAR(100),
    model VARCHAR(100),
    weight DECIMAL(8,2),
    dimensions VARCHAR(100),
    status ENUM('active', 'inactive', 'discontinued') DEFAULT 'active',
    min_stock_level INT DEFAULT 0,
    max_stock_level INT DEFAULT 1000,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    INDEX idx_sku (sku)
);

CREATE TABLE IF NOT EXISTS inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT UNIQUE NOT NULL,
    current_stock INT DEFAULT 0 NOT NULL,
    reserved_stock INT DEFAULT 0 NOT NULL,
    available_stock INT DEFAULT 0 NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE IF NOT EXISTS suppliers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    address TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email)
);

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    customer_id INT NOT NULL,
    user_id INT NOT NULL,
    status ENUM('pending', 'confirmed', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    total_amount DECIMAL(10,2) NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_order_number (order_number)
);

CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE IF NOT EXISTS purchase_orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    po_number VARCHAR(50) UNIQUE NOT NULL,
    supplier_id INT NOT NULL,
    user_id INT NOT NULL,
    status ENUM('pending', 'confirmed', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    total_amount DECIMAL(10,2) NOT NULL,
    expected_delivery TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    INDEX idx_po_number (po_number)
);

CREATE TABLE IF NOT EXISTS purchase_order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    purchase_order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_cost DECIMAL(10,2) NOT NULL,
    total_cost DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (purchase_order_id) REFERENCES purchase_orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE IF NOT EXISTS inventory_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    user_id INT NOT NULL,
    transaction_type ENUM('purchase', 'sale', 'return', 'adjustment') NOT NULL,
    quantity INT NOT NULL,
    previous_stock INT NOT NULL,
    new_stock INT NOT NULL,
    reference_id INT,
    reference_type VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Insert sample data
INSERT INTO categories (name, description, is_active) VALUES
('Electronics', 'Electronic devices and accessories', true),
('Clothing', 'Apparel and fashion items', true),
('Books', 'Books and publications', true),
('Home & Garden', 'Home improvement and garden supplies', true),
('Sports', 'Sports equipment and accessories', true),
('Toys', 'Toys and games', true);

INSERT INTO users (username, email, hashed_password, full_name, role, is_active) VALUES
('admin', 'admin@inventory.com', '$2b$12$r3jyZoZ0qXQUyBAO28uWfe/eTw5dMCzr0NXHS8BMiyr/cFamOr3G6', 'System Administrator', 'admin', true),
('manager', 'manager@inventory.com', '$2b$12$pYPR1WFv9YemNt5Q67YR/OqGw3/Q4q1edilH.SQqT2AZrb/6XSJsa', 'Store Manager', 'manager', true),
('staff', 'staff@inventory.com', '$2b$12$5AwhD/I11LqBjbr6CPeuTuHzQ9tI4HOIYp2vexpFCVUPbh03b3yGm', 'Store Staff', 'staff', true);

INSERT INTO products (sku, name, description, price, cost_price, category_id, brand, model, weight, dimensions, min_stock_level, max_stock_level, status) VALUES
('LAPTOP001', 'Dell Inspiron 15', '15-inch laptop with Intel i5 processor', 899.99, 650.00, 1, 'Dell', 'Inspiron 15-3000', 2.2, '14.96 x 10.15 x 0.89 inches', 5, 50, 'active'),
('PHONE001', 'iPhone 14', 'Latest iPhone with A15 Bionic chip', 999.99, 750.00, 1, 'Apple', 'iPhone 14', 0.17, '5.78 x 2.82 x 0.31 inches', 10, 100, 'active'),
('TSHIRT001', 'Cotton T-Shirt', 'Comfortable cotton t-shirt', 19.99, 8.00, 2, 'Generic', 'Basic Cotton', 0.2, 'M', 20, 200, 'active'),
('BOOK001', 'Python Programming', 'Learn Python programming language', 49.99, 25.00, 3, 'Tech Books', 'Python Guide', 0.8, '8.5 x 11 inches', 15, 100, 'active'),
('TOOL001', 'Hammer Set', 'Professional hammer set', 29.99, 15.00, 4, 'HomePro', 'Professional', 1.5, '12 inches', 8, 50, 'active'),
('BALL001', 'Soccer Ball', 'Professional soccer ball', 39.99, 20.00, 5, 'SportMax', 'Professional', 0.4, 'Size 5', 12, 80, 'active'),
('TOY001', 'LEGO Set', 'Creative building blocks', 59.99, 30.00, 6, 'LEGO', 'City Set', 0.5, 'Various', 10, 60, 'active');

INSERT INTO inventory (product_id, current_stock, reserved_stock, available_stock) VALUES
(1, 25, 2, 23),
(2, 45, 5, 40),
(3, 150, 10, 140),
(4, 35, 3, 32),
(5, 20, 1, 19),
(6, 30, 4, 26),
(7, 15, 2, 13);

INSERT INTO customers (name, email, phone, address, is_active) VALUES
('John Doe', 'john.doe@email.com', '+1-555-0101', '123 Main St, City, State 12345', true),
('Jane Smith', 'jane.smith@email.com', '+1-555-0102', '456 Oak Ave, City, State 12345', true),
('Bob Johnson', 'bob.johnson@email.com', '+1-555-0103', '789 Pine Rd, City, State 12345', true),
('Alice Brown', 'alice.brown@email.com', '+1-555-0104', '321 Elm St, City, State 12345', true);

INSERT INTO suppliers (name, contact_person, email, phone, address, is_active) VALUES
('Tech Supplies Inc', 'Mike Wilson', 'mike@techsupplies.com', '+1-555-0201', '100 Tech Blvd, Tech City, TC 54321', true),
('Fashion Wholesale', 'Sarah Davis', 'sarah@fashionwholesale.com', '+1-555-0202', '200 Fashion Ave, Style City, SC 54322', true),
('Book Distributors', 'Tom Miller', 'tom@bookdist.com', '+1-555-0203', '300 Book St, Read City, RC 54323', true),
('Hardware Plus', 'Lisa Garcia', 'lisa@hardwareplus.com', '+1-555-0204', '400 Tool Rd, Build City, BC 54324', true);

INSERT INTO orders (order_number, customer_id, user_id, status, total_amount, notes) VALUES
('ORD-2024-001', 1, 2, 'delivered', 919.98, 'Customer requested express delivery'),
('ORD-2024-002', 2, 3, 'shipped', 59.97, 'Standard shipping'),
('ORD-2024-003', 3, 2, 'confirmed', 39.99, 'Customer pickup'),
('ORD-2024-004', 4, 3, 'pending', 119.98, 'Awaiting payment confirmation');

INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES
(1, 1, 1, 899.99, 899.99),
(1, 3, 1, 19.99, 19.99),
(2, 3, 3, 19.99, 59.97),
(3, 6, 1, 39.99, 39.99),
(4, 7, 2, 59.99, 119.98);

INSERT INTO purchase_orders (po_number, supplier_id, user_id, status, total_amount, expected_delivery, notes) VALUES
('PO-2024-001', 1, 2, 'confirmed', 5000.00, '2024-02-15', 'Electronics restock'),
('PO-2024-002', 2, 2, 'pending', 1500.00, '2024-02-20', 'Spring clothing collection'),
('PO-2024-003', 3, 3, 'shipped', 800.00, '2024-02-18', 'New book releases');

INSERT INTO purchase_order_items (purchase_order_id, product_id, quantity, unit_cost, total_cost) VALUES
(1, 1, 5, 650.00, 3250.00),
(1, 2, 10, 750.00, 7500.00),
(2, 3, 50, 8.00, 400.00),
(3, 4, 20, 25.00, 500.00);

INSERT INTO inventory_transactions (product_id, user_id, transaction_type, quantity, previous_stock, new_stock, reference_id, reference_type, notes) VALUES
(1, 2, 'purchase', 5, 20, 25, 1, 'purchase_order', 'Initial stock from PO-2024-001'),
(2, 2, 'purchase', 10, 35, 45, 1, 'purchase_order', 'Initial stock from PO-2024-001'),
(3, 2, 'purchase', 50, 100, 150, 2, 'purchase_order', 'Spring collection restock'),
(4, 3, 'purchase', 20, 15, 35, 3, 'purchase_order', 'New book releases'),
(1, 2, 'sale', -1, 25, 24, 1, 'order', 'Sale from ORD-2024-001'),
(3, 2, 'sale', -1, 150, 149, 1, 'order', 'Sale from ORD-2024-001'),
(3, 3, 'sale', -3, 149, 146, 2, 'order', 'Sale from ORD-2024-002'),
(6, 2, 'sale', -1, 30, 29, 3, 'order', 'Sale from ORD-2024-003'),
(7, 3, 'sale', -2, 15, 13, 4, 'order', 'Sale from ORD-2024-004');