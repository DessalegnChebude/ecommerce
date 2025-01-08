# E-Commerce Application

### Overview

#### This is a Django-based e-commerce application that provides a platform for managing products, categories, orders, user authentication, product reviews, discounts, and promotions. The application is built using Django Rest Framework (DRF) and includes token-based authentication using JWT.

### Features

1. User Management:

    - User registration and login using JWT tokens.

    - Authentication for protected routes.

2. Product Management:

    - Add, update, delete, and list products.

    - Support for multiple product images.

3. Order Management:

    - Place orders and reduce stock quantities accordingly.

    - Update or cancel orders with stock adjustments.

4. Product Reviews:

    - Submit reviews and ratings for products.

    - Retrieve reviews for each product.

5. Discounts and Promotions:

    - Add discounts to products.

    - Automatically calculate discounted prices.

# Technologies Used
- Backend: Django, Django Rest Framework

- Authentication: JWT

- Database: SQLite (default, can be switched to PostgreSQL or MySQL)

- Media Management: Django File Storage for product images

### Installation

#### Clone the Repository:

#### git clone <repository_url>
#### cd ecommerce

#### Set up a Virtual Environment:

#### python -m venv env
#### source env/bin/activate  # On Windows: env\Scripts\activate

#### Install Dependencies:

#### pip install -r requirements.txt

#### Apply Migrations:

#### python manage.py makemigrations
#### python manage.py migrate

#### Run the Development Server

#### python manage.py runserver

## API Endpoints

### User Authentication

##### Register, update and list and delate : POST/GET/PUT/DELETE http://127.0.0.1:8000/api/users/ 

## Product Management
##### Register, update and list and delate : POST/GET/PUT/DELETE http://127.0.0.1:8000/api/products/
#### Retrieve Order: GET /api/products/<id>/


## Product Images

#### Register, update and list and delate : POST/GET/PUT/DELETE http://127.0.0.1:8000/api/product-images/
#### Retrieve Order: GET /api/product-images/<id>/


## Order Management

#### Register, update and list and delate : POST/GET/PUT/DELETE http://127.0.0.1:8000/api/orders/
#### Retrieve Order: GET /api/orders/<id>/

## Product Reviews

#### Register, update and list and delate : POST/GET/PUT/DELETE http://127.0.0.1:8000/api/reviews/
#### Retrieve Order: GET /api/reviews/<id>/


## Discounts and Promotions
#### Register, update and list and delate : POST/GET/PUT/DELETE http://127.0.0.1:8000/api/disounts/
#### Retrieve Order: GET /api/discounts/<id>/
