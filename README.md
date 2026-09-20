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
│   │   ├── seriaizers.py
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
│   ├── manage.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

## API Endpoints

### Authentication

| Method | Endpoint              | Description                          |
| ------ | --------------------- | ------------------------------------ |
| POST   | `/accounts/register/` | Register a new user                  |
| POST   | `/accounts/login/`    | Obtain JWT access and refresh tokens |
| POST   | `/accounts/refresh/`  | Refresh an access token              |

### Products

| Method    | Endpoint                | Description              |
| --------- | ----------------------- | ------------------------ |
| GET       | `/products/categories/` | List categories          |
| GET       | `/products/`            | List products            |
| GET       | `/products/<id>/`       | Retrieve product details |
| PUT/PATCH | `/products/edit/<id>/`  | Edit product             |
| DELETE    | `/products/edit/<id>/`  | Delete product           |

The product list API supports:

* Category filtering
* Availability filtering
* Searching by product name and description
* Ordering by price
* Ordering by creation date
* Minimum price filtering
* Maximum price filtering

Example:

```text
/products/?category=1
/products/?is_available=true
/products/?search=phone
/products/?ordering=price
/products/?min_price=100
/products/?max_price=1000
```

### Cart

| Method | Endpoint             | Description               |
| ------ | -------------------- | ------------------------- |
| POST   | `/cart/add/`         | Add product to cart       |
| GET    | `/cart/`             | View cart                 |
| PATCH  | `/cart/update/<id>/` | Update cart item quantity |
| DELETE | `/cart/remove/<id>/` | Remove cart item          |
| DELETE | `/cart/clear/`       | Clear cart                |

Cart endpoints require authentication.

Example request for adding an item:

```json
{
    "product_id": 1,
    "quantity": 2
}
```

### Orders

| Method | Endpoint            | Description               |
| ------ | ------------------- | ------------------------- |
| POST   | `/orders/checkout/` | Create an order from cart |
| GET    | `/orders/`          | View user's orders        |
| GET    | `/orders/<id>/`     | View order details        |

Order endpoints require authentication.

### Payments

| Method | Endpoint                | Description             |
| ------ | ----------------------- | ----------------------- |
| POST   | `/api/payments/create/` | Create Razorpay payment |
| POST   | `/api/payments/verify/` | Verify Razorpay payment |

Payment endpoints require authentication.

## Authentication

The API uses **JWT authentication** through `djangorestframework-simplejwt`.

After successful login, the API returns:

* Access token
* Refresh token

For protected endpoints, include the access token in the request:

```text
Authorization: Bearer <access_token>
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/sivasurya101010-lab/Ecommerce-backend.git
cd Ecommerce-backend
```

### 2. Go to the Django project directory

```bash
cd myproject
```

### 3. Create a virtual environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file inside the `myproject` directory.

Example:

```env
SECRET_KEY=your-secret-key
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret
```

Do not commit the `.env` file to GitHub.

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Create an admin user

```bash
python manage.py createsuperuser
```

### 8. Start the development server

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

## Checkout Flow

The checkout process works as follows:

```text
User adds products to cart
          ↓
       View cart
          ↓
      Checkout
          ↓
      Create Order
          ↓
   Reduce product stock
          ↓
       Clear cart
```

## Payment Flow

The payment process is designed around Razorpay:

```text
Create Order
      ↓
Create Razorpay Payment
      ↓
Complete Payment
      ↓
Verify Payment
      ↓
Update Payment Status
      ↓
Update Order Status
```

## Database

The project currently uses **SQLite** for development.

The database can be changed to PostgreSQL or another relational database by updating Django's `DATABASES` configuration.

## Security

Sensitive credentials are stored using environment variables.

The following files and directories should not be committed:

```text
.env
db.sqlite3
venv/
__pycache__/
```

These are already included in `.gitignore`.

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
* Pagination
* Advanced filtering
* Email notifications
* Inventory management

## Author

**Surya Prakash**

Backend Developer | Python | Django | Django REST Framework

GitHub: `https://github.com/sivasurya101010-lab`

LinkedIn: `https://linkedin.com/in/surya-prakash-7665aa2a1`
