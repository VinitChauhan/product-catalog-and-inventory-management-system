# Product Catalog and Inventory Management System

A comprehensive inventory management system built with FastAPI backend, Flask frontend, and MySQL database, all containerized with Docker.

## 🚀 Features

### Core Features
- **Product Management**: Add, edit, delete, and categorize products
- **Inventory Tracking**: Real-time stock levels with low stock alerts
- **Order Management**: Customer orders with status tracking
- **Purchase Orders**: Supplier management and purchase order processing
- **User Management**: Role-based access control (Admin, Manager, Staff)
- **Customer Management**: Customer database and order history
- **Supplier Management**: Supplier information and purchase tracking
- **Reporting**: Dashboard with key metrics and analytics

### Technical Features
- **Modern UI**: Responsive Bootstrap 5 interface with Font Awesome icons
- **Real-time Updates**: Live inventory tracking and status updates
- **Search & Filter**: Advanced search and filtering capabilities
- **Pagination**: Efficient data handling for large datasets
- **Authentication**: JWT-based secure authentication
- **API-First**: RESTful API for all operations
- **Containerized**: Docker Compose for easy deployment

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │    Database     │
│   (Flask)       │◄──►│   (FastAPI)     │◄──►│   (MySQL)       │
│   Port: 5000    │    │   Port: 8000    │    │   Port: 3306    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Prerequisites

- Docker and Docker Compose
- Git

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd product-catalog-and-inventory-management-system
```

### 2. Start the Application
```bash
docker-compose up -d
```

This will start:
- **Frontend**: http://localhost:5000
- **Backend API**: http://localhost:8000
- **MySQL Database**: localhost:3306

### 3. Access the Application
- **Web Interface**: http://localhost:5000
- **API Documentation**: http://localhost:8000/docs

### 4. Default Login Credentials
```
Admin User:
- Username: admin
- Password: admin123

Manager User:
- Username: manager
- Password: manager123

Staff User:
- Username: staff
- Password: staff123
```

## 📁 Project Structure

```
product-catalog-and-inventory-management-system/
├── docker-compose.yml              # Docker Compose configuration
├── README.md                       # This file
├── src/
│   ├── backend/                    # FastAPI Backend
│   │   ├── main.py                 # Main FastAPI application
│   │   ├── models.py               # SQLAlchemy models
│   │   ├── schemas.py              # Pydantic schemas
│   │   ├── auth.py                 # Authentication logic
│   │   ├── data_access.py          # Database operations
│   │   ├── database_connection.py  # Database configuration
│   │   ├── requirements.txt        # Python dependencies
│   │   └── dockerfile              # Backend Dockerfile
│   ├── frontend/                   # Flask Frontend
│   │   ├── app.py                  # Main Flask application
│   │   ├── requirements.txt        # Python dependencies
│   │   ├── dockerfile              # Frontend Dockerfile
│   │   └── templates/              # HTML templates
│   │       ├── base.html           # Base template
│   │       ├── login.html          # Login page
│   │       ├── index.html          # Dashboard
│   │       ├── products.html       # Products management
│   │       ├── inventory.html      # Inventory management
│   │       └── users.html          # User management
│   └── database/
│       └── init.sql                # Database initialization script
```

## 🔧 Configuration

### Environment Variables

The system uses the following environment variables (configured in docker-compose.yml):

#### Database Configuration
- `DB_USER`: Database username (default: user)
- `DB_PASSWORD`: Database password (default: password)
- `DB_HOST`: Database host (default: mysql)
- `DB_PORT`: Database port (default: 3306)
- `DB_NAME`: Database name (default: inventory_management)

#### Backend Configuration
- `SECRET_KEY`: JWT secret key
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time (default: 30)

#### Frontend Configuration
- `BACKEND_URL`: Backend API URL (default: http://backend:8000)

## 📊 Database Schema

### Core Tables
- **users**: System users with role-based access
- **categories**: Product categories
- **products**: Product catalog with detailed information
- **inventory**: Current stock levels and availability
- **customers**: Customer information
- **suppliers**: Supplier information
- **orders**: Customer orders
- **order_items**: Individual items in orders
- **purchase_orders**: Purchase orders from suppliers
- **purchase_order_items**: Items in purchase orders
- **inventory_transactions**: Stock movement history

## 🔐 Authentication & Authorization

### User Roles
1. **Admin**: Full system access
2. **Manager**: Product, inventory, and order management
3. **Staff**: Basic operations and viewing

### JWT Authentication
- Secure token-based authentication
- Automatic token refresh
- Role-based access control

## 🎨 User Interface

### Features
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Bootstrap 5 with custom styling
- **Interactive Elements**: Modals, dropdowns, and tooltips
- **Real-time Updates**: Live data without page refresh
- **Search & Filter**: Advanced filtering capabilities
- **Export Options**: Data export functionality

### Pages
1. **Dashboard**: Overview with key metrics and charts
2. **Products**: Product catalog management
3. **Inventory**: Stock tracking and adjustments
4. **Orders**: Customer order management
5. **Purchase Orders**: Supplier order management
6. **Customers**: Customer database
7. **Suppliers**: Supplier management
8. **Users**: User management
9. **Reports**: Analytics and reporting

## 🔌 API Endpoints

### Authentication
- `POST /token` - User login
- `POST /users/` - Create user

### Products
- `GET /products/` - List products
- `POST /products/` - Create product
- `GET /products/{id}` - Get product details
- `PUT /products/{id}` - Update product
- `DELETE /products/{id}` - Delete product

### Inventory
- `GET /inventory/` - List inventory
- `GET /inventory/low-stock` - Low stock items
- `POST /inventory/transactions` - Create transaction

### Orders
- `GET /orders/` - List orders
- `POST /orders/` - Create order
- `PUT /orders/{id}` - Update order

### Categories
- `GET /categories/` - List categories
- `POST /categories/` - Create category

### Users
- `GET /users/` - List users
- `POST /users/` - Create user
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

## 🚀 Development

### Running in Development Mode
```bash
# Start services with volume mounts for development
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Adding New Features
1. Update backend models in `src/backend/models.py`
2. Add API endpoints in `src/backend/main.py`
3. Create frontend templates in `src/frontend/templates/`
4. Update frontend routes in `src/frontend/app.py`

### Database Migrations
```bash
# Access database
docker-compose exec mysql mysql -u user -p inventory_management

# Run migrations (if using Alembic)
docker-compose exec backend alembic upgrade head
```

## 🧪 Testing

### API Testing
```bash
# Test backend API
curl http://localhost:8000/docs

# Test authentication
curl -X POST "http://localhost:8000/token?username=admin&password=admin123"
```

### Frontend Testing
```bash
# Access frontend
open http://localhost:5000
```

## 📈 Monitoring & Logs

### View Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend
docker-compose logs mysql
```

### Health Checks
- Backend: http://localhost:8000/health
- Frontend: http://localhost:5000
- Database: MySQL connection test

## 🔧 Troubleshooting

### Common Issues

1. **Port Conflicts**
   ```bash
   # Check if ports are in use
   lsof -i :5000
   lsof -i :8000
   lsof -i :3306
   ```

2. **Database Connection Issues**
   ```bash
   # Check database status
   docker-compose exec mysql mysqladmin ping
   ```

3. **Service Not Starting**
   ```bash
   # Check service logs
   docker-compose logs [service-name]
   ```

4. **Permission Issues**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   ```

### Reset Everything
```bash
# Stop and remove everything
docker-compose down -v
docker system prune -f

# Start fresh
docker-compose up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the API docs at http://localhost:8000/docs

## 🔄 Updates

### Version History
- **v1.0.0**: Initial release with core features
- Basic CRUD operations for all entities
- JWT authentication
- Responsive UI
- Docker containerization

### Planned Features
- Advanced reporting and analytics
- Barcode scanning integration
- Email notifications
- Mobile app
- Multi-warehouse support
- Advanced inventory forecasting


### Deploy Kubernetes Dashboard

Kubernetes Dashboard to your Kind cluster

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml

kubernetes-dashboard-admin-user.yaml

apiVersion: v1
kind: ServiceAccount
metadata:
 name: admin-user
 namespace: kubernetes-dashboard
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard


kubectl apply -f kubernetes-dashboard-admin-user.yaml

kubectl proxy

http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/

kubectl -n kubernetes-dashboard create token admin-user

```

### ARGO CD Setup

Installing Argo CD on Docker Desktop for Mac involves deploying it into the Kubernetes cluster that Docker Desktop provides. 
Here's a step-by-step guide: 

• Ensure Docker Desktop Kubernetes is Enabled: 
	• Open Docker Desktop. 
	• Navigate to Settings &gt; Kubernetes. 
	• Ensure the "Enable Kubernetes" checkbox is selected. 

• Install kubectl and argocd CLI: 
	• If not already installed, install kubectl (Kubernetes command-line tool) and the Argo CD CLI using Homebrew: 

        brew install kubectl
        brew install argocd

• Create Argo CD Namespace and Install Resources: 
	• Create a dedicated namespace for Argo CD: 

        kubectl create namespace argocd

• Apply the official Argo CD installation manifest to deploy its components into the argocd namespace: 

        kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

• Access the Argo CD API Server: 
	• By default, the Argo CD API server is not externally exposed. To access the UI, set up port forwarding: [1]  

        kubectl port-forward svc/argocd-server -n argocd 8080:443

This command forwards local port 8080 to the Argo CD server's HTTPS port (443) within the cluster. You can now access the Argo CD UI in your browser at https://localhost:8080. [1]  

• Retrieve Initial Admin Password: 
	• The initial password for the admin user is stored in a Kubernetes secret. Retrieve it and decode it: 

        kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

• Login to Argo CD: 
	• Open your web browser and navigate to https://localhost:8080. 
	• Login with the username admin and the password retrieved in the previous step. 
	• It is recommended to change the admin password after the initial login using the Argo CD UI or CLI. 

You have now successfully installed Argo CD on your local Docker Desktop Kubernetes cluster on Mac. 



