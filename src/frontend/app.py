from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import requests
import os
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# Backend API URL
BACKEND_URL = os.getenv('BACKEND_URL', 'http://backend:8000')

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'access_token' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    """Home page / Dashboard"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        try:
            response = requests.post(f"{BACKEND_URL}/token", params={
                'username': username,
                'password': password
            })
            
            if response.status_code == 200:
                token_data = response.json()
                session['access_token'] = token_data['access_token']
                session['username'] = username
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password', 'error')
        except requests.exceptions.RequestException:
            flash('Unable to connect to backend service', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard page"""
    return render_template('index.html')

# Products routes
@app.route('/products')
@login_required
def products():
    """Products page"""
    return render_template('products.html')

@app.route('/api/products')
@login_required
def api_products():
    """API endpoint to get products"""
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        response = requests.get(f"{BACKEND_URL}/products/", headers=headers, params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Backend service unavailable'}), 503

@app.route('/api/products/', methods=['POST'])
@login_required
def api_create_product():
    """API endpoint to create product"""
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        response = requests.post(f"{BACKEND_URL}/products/", headers=headers, json=request.json)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Backend service unavailable'}), 503

@app.route('/api/products/<int:product_id>', methods=['PUT'])
@login_required
def api_update_product(product_id):
    """API endpoint to update product"""
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        response = requests.put(f"{BACKEND_URL}/products/{product_id}", headers=headers, json=request.json)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Backend service unavailable'}), 503

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@login_required
def api_delete_product(product_id):
    """API endpoint to delete product"""
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        response = requests.delete(f"{BACKEND_URL}/products/{product_id}", headers=headers)
        return jsonify({'message': 'Product deleted'}), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Backend service unavailable'}), 503

# Categories routes
@app.route('/api/categories')
@login_required
def api_categories():
    """API endpoint to get categories"""
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        response = requests.get(f"{BACKEND_URL}/categories/", headers=headers)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Backend service unavailable'}), 503

# Inventory routes
@app.route('/inventory')
@login_required
def inventory():
    """Inventory page"""
    return render_template('inventory.html')

@app.route('/api/inventory')
@login_required
def api_inventory():
    """API endpoint to get inventory"""
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        response = requests.get(f"{BACKEND_URL}/inventory/", headers=headers, params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Backend service unavailable'}), 503

@app.route('/api/inventory/low-stock')
@login_required
def api_low_stock():
    """API endpoint to get low stock items"""
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        response = requests.get(f"{BACKEND_URL}/inventory/low-stock", headers=headers)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Backend service unavailable'}), 503

# Orders routes
@app.route('/orders')
@login_required
def orders():
    """Orders page"""
    return render_template('orders.html')

@app.route('/api/orders')
@login_required
def api_orders():
    """API endpoint to get orders"""
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        response = requests.get(f"{BACKEND_URL}/orders/", headers=headers, params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Backend service unavailable'}), 503

# Purchase Orders routes
@app.route('/purchase-orders')
@login_required
def purchase_orders():
    """Purchase Orders page"""
    return render_template('purchase_orders.html')

@app.route('/api/purchase-orders')
@login_required
def api_purchase_orders():
    """API endpoint to get purchase orders"""
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        response = requests.get(f"{BACKEND_URL}/purchase-orders/", headers=headers, params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Backend service unavailable'}), 503

# Customers routes
@app.route('/customers')
@login_required
def customers():
    """Customers page"""
    return render_template('customers.html')

@app.route('/api/customers')
@login_required
def api_customers():
    """API endpoint to get customers"""
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        response = requests.get(f"{BACKEND_URL}/customers/", headers=headers, params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Backend service unavailable'}), 503

# Suppliers routes
@app.route('/suppliers')
@login_required
def suppliers():
    """Suppliers page"""
    return render_template('suppliers.html')

@app.route('/api/suppliers')
@login_required
def api_suppliers():
    """API endpoint to get suppliers"""
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        response = requests.get(f"{BACKEND_URL}/suppliers/", headers=headers, params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Backend service unavailable'}), 503

# Users routes
@app.route('/users')
@login_required
def users():
    """Users page"""
    return render_template('users.html')

@app.route('/api/users')
@login_required
def api_users():
    """API endpoint to get users"""
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        response = requests.get(f"{BACKEND_URL}/users/", headers=headers, params=request.args)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Backend service unavailable'}), 503

# Reports routes
@app.route('/reports')
@login_required
def reports():
    """Reports page"""
    return render_template('reports.html')

# Dashboard API routes
@app.route('/api/dashboard/stats')
@login_required
def api_dashboard_stats():
    """API endpoint to get dashboard statistics"""
    try:
        headers = {'Authorization': f"Bearer {session['access_token']}"}
        
        # Get basic stats
        stats = {
            'total_products': 0,
            'total_orders': 0,
            'low_stock_items': 0,
            'total_revenue': 0
        }
        
        # Get products count
        products_response = requests.get(f"{BACKEND_URL}/products/", headers=headers)
        if products_response.status_code == 200:
            products_data = products_response.json()
            if isinstance(products_data, list):
                stats['total_products'] = len(products_data)
            elif isinstance(products_data, dict) and 'total' in products_data:
                stats['total_products'] = products_data['total']
        
        # Get orders count and revenue
        orders_response = requests.get(f"{BACKEND_URL}/orders/", headers=headers)
        if orders_response.status_code == 200:
            orders_data = orders_response.json()
            if isinstance(orders_data, list):
                stats['total_orders'] = len(orders_data)
                stats['total_revenue'] = sum(order.get('total_amount', 0) for order in orders_data)
            elif isinstance(orders_data, dict) and 'total' in orders_data:
                stats['total_orders'] = orders_data['total']
        
        # Get low stock items count
        low_stock_response = requests.get(f"{BACKEND_URL}/inventory/low-stock", headers=headers)
        if low_stock_response.status_code == 200:
            low_stock_data = low_stock_response.json()
            if isinstance(low_stock_data, list):
                stats['low_stock_items'] = len(low_stock_data)
        
        return jsonify(stats), 200
        
    except requests.exceptions.RequestException:
        return jsonify({'error': 'Backend service unavailable'}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
