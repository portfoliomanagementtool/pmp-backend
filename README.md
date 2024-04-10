---

# Project Name: PMP Backend

This repository contains the backend codebase for PMP (Portfolio Management Tool). It is built using Django and Django REST Framework, with PostgreSQL as the primary database and TimescaleDB for time-series data storage. The application is containerized with Docker for easier deployment and scalability.

## Installation

To get started with the backend development environment, follow these steps:

1. **Clone this repository:**
   ```
   git clone https://github.com/portfoliomanagementtool/pmp-backend.git
   ```

2. **Navigate to the project directory:**
   ```
   cd pmp-backend
   ```

3. **Create a virtual environment:**
   ```
   python -m venv env
   ```

4. **Activate the virtual environment:**
   - On Windows:
     ```
     env\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source env/bin/activate
     ```

5. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

6. **Set up the database:**
   - Ensure Docker is installed on your system.
   - Start the application using Docker Compose:
     ```
     docker-compose up -d
     ```

7. **Apply database migrations:**
   ```
   python manage.py migrate
   ```

8. **Start the development server:**
   ```
   python manage.py runserver
   ```

## API Endpoints

### Assets:

#### 1. Asset List/Create
- **URL**: `/assets/`
- **Description**: List and create assets.
- **Methods**: GET (List), POST (Create)
- **Parameters**: None (For POST request, provide JSON payload with asset details)
- **Example Usage**: 
  - To list all assets: `GET /assets/`
  - To create a new asset: `POST /assets/`

#### 2. Asset Retrieve/Update/Delete
- **URL**: `/assets/<str:pk>/`
- **Description**: Retrieve, update, or delete a specific asset by its primary key.
- **Methods**: GET (Retrieve), PUT (Update), DELETE (Delete)
- **Parameters**: `<str:pk>` (Primary key of the asset)
- **Example Usage**: 
  - To retrieve details of an asset: `GET /assets/<str:pk>/`
  - To update details of an asset: `PUT /assets/<str:pk>/`
  - To delete an asset: `DELETE /assets/<str:pk>/`

#### 3. Bulk Insert Assets
- **URL**: `/assets/bulk_insert`
- **Description**: Bulk insert assets from a CSV file.
- **Methods**: POST
- **Parameters**: CSV file containing asset data
- **Example Usage**: 
  - To bulk insert assets from a CSV file: `POST /assets/bulk_insert`

### Asset Pricing:

#### 1. Asset Pricing List/Create
- **URL**: `/asset_pricing/create`
- **Description**: List and create asset pricings.
- **Methods**: GET (List), POST (Create)
- **Parameters**: None (For POST request, provide JSON payload with asset pricing details)
- **Example Usage**: 
  - To list all asset pricings: `GET /asset_pricing/create`
  - To create a new asset pricing: `POST /asset_pricing/create`

### Users:

#### 1. List Users
- **URL**: `/users/list`
- **Description**: List all users.
- **Methods**: GET
- **Parameters**: None
- **Example Usage**: 
  - To list all users: `GET /users/list`

#### 2. Create User
- **URL**: `/users/create`
- **Description**: Create a new user.
- **Methods**: POST
- **Parameters**: JSON payload with user details (name, email, phone)
- **Example Usage**: 
  - To create a new user: `POST /users/create`

#### 3. Delete User
- **URL**: `/users/<str:pk>/delete/`
- **Description**: Delete a specific user by their primary key.
- **Methods**: DELETE
- **Parameters**: `<str:pk>` (Primary key of the user)
- **Example Usage**: 
  - To delete a user: `DELETE /users/<str:pk>/delete/`

## Configuration



## Deployment



---
