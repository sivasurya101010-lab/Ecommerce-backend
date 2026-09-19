# E-commerce Backend API

A backend REST API for an e-commerce application built with **Python, Django, and Django REST Framework**.

The project provides APIs for user authentication, product and category management, shopping cart operations, order management, checkout, and Razorpay payment integration.

## Features

* User registration
* JWT-based authentication
* JWT access and refresh tokens
* Product and category management
* Product search, filtering, and ordering
* Shopping cart management
* Add, update, remove, and clear cart items
* Order creation and order history
* Checkout functionality
* Razorpay payment integration
* Payment verification
* Django Admin for backend management
* SQLite database for development

## Tech Stack

* **Python**
* **Django 6**
* **Django REST Framework**
* **Simple JWT**
* **Django Filter**
* **SQLite**
* **Razorpay**
* **Git & GitHub**
* **Postman** for API testing

## Project Structure

```text
Ecommerce-backend/
│
├── myproject/
│   ├── accounts/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests.py
│   │
│   ├── products/
│   │   ├── models.py
│   │   ├── serialiser.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests.py
│   │
│   ├── cart/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests.py
│   │
│   ├── orders/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests.py
│   │
│   ├── payments/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── tests.py
│   │
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   └── manage.py
│
├── .gitignore
└── README.md
```

## API Modules

### Authentication

| Method | Endpoint              | Description                          |
| ------ | --------------------- | ------------------------------------ |
| POST   | `/accounts/register/` | Register a new user                  |
| POST   | `/accounts/login/`    | Obtain JWT access and refresh tokens |
| POST   | `/accounts/refresh/`  | Refresh an access token              |

### Products

| Method    | Endpoint                   | Description              |
| --------- | -------------------------- | ------------------------ |
| GET       | `/products/categories/`    | List categories          |
| GET       | `/products/productList/`   | List products            |
| GET       | `/products/productDetail/` | Retrieve product details |
| PUT/PATCH | `/products/productEdit/`   | Edit product information |

Product listing supports filtering, searching, and ordering through Django REST Framework filter backends.

### Cart

The cart module provides functionality for:

* Adding products to the cart
* Viewing cart items
* Updating cart quantities
* Removing individual cart items
* Clearing the cart

### Orders

The order module provides:

* Checkout
* Creating orders from cart items
* Viewing the user's orders
* Viewing order details

### Payments

The payment module integrates with **Razorpay** and provides endpoints for:

* Creating a payment
* Verifying a payment

## Authentication

The API uses **JWT authentication** through `djangorestframework-simplejwt`.

After successful login, the API returns an access token and refresh token.

For protected endpoints, include the access token in the request:

```text
Authorization: Bearer <access_token>
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ecommerce-backend.git
cd ecommerce-backend
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project directory.

Example:

```env
SECRET_KEY=your-secret-key
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret
```

Do not commit the `.env` file to GitHub.

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create an admin user

```bash
python manage.py createsuperuser
```

### 7. Start the development server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/
```

Django Admin:

```text
http://127.0.0.1:8000/admin/
```

## API Testing

The APIs can be tested using **Postman**.

Typical authentication flow:

```text
Register
   ↓
Login
   ↓
Receive JWT access token
   ↓
Send access token with protected requests
   ↓
Refresh token when access token expires
```

## Payment Flow

The payment process is designed around Razorpay:

```text
User Checkout
      ↓
Create Order
      ↓
Create Razorpay Payment
      ↓
Complete Payment
      ↓
Verify Payment
      ↓
Update Payment / Order Status
```

## Database

The project currently uses **SQLite** for development.

The database can be changed to PostgreSQL or another relational database by updating Django's `DATABASES` configuration.

## Security

Sensitive credentials should be stored using environment variables.

The following files should not be committed:

```text
.env
db.sqlite3
venv/
__pycache__/
```

## Future Improvements

Possible future improvements include:

* PostgreSQL database
* Docker containerization
* Redis caching
* Celery background tasks
* API documentation with Swagger/OpenAPI
* Automated testing with pytest
* CI/CD pipeline
* Production deployment
* Improved product image handling
* Pagination and advanced filtering
* Email notifications
* Inventory management

## Author

**Surya Prakash**

Backend Developer | Python | Django | Django REST Framework

GitHub: `https://github.com/sivasurya101010-lab`

LinkedIn: `https://linkedin.com/in/surya-prakash-7665aa2a1`
