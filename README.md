# Product Management Application

## Table of Contents

1. [Group 7](#group-7)
2. [Project Objectives](#project-objectives)
3. [What We've Implemented](#what-weve-implemented)
4. [Project Structure](#project-structure)
   - [Services](#services)
5. [How to Run the Application](#how-to-run-the-application)
   - [Option 1: Docker Compose](#option-1-docker-compose-recommended)
   - [Option 2: Manual Build](#option-2-manual-build-of-each-service)
   - [Option 3: Local Development](#option-3-local-development-without-docker)
6. [Environment Variables](#environment-variables)
7. [Architecture](#architecture)
8. [Communication Flow](#communication-flow)
9. [Advantages of This Architecture](#advantages-of-this-architecture)
10. [AWS Deployment](#aws-deployment)

## Group 7
- Members:
-   Joel Navarro
-   Matteo Carreiro
-   Arnau Oller
-   Jordi Costa
-   Pau Pujol
-   Nora Raghai

## Project objectives

- Step 1: Create a basic database to store product metadata related to food industry.
- Step 2: Create another database and connect to the first one
- Step 3: Make some algorithm to manage DB and product basic operations
- Step 4: Extend DBs

## What we've implemented?
- We've added new API routes to help the management of product metadata (add, delete, modify, etc..). 
- We created the first database to store product information

## Project Structure

El proyecto está dividido en dos servicios independientes en **carpetas separadas**:

```
AOS-Web/
├── api/              # Backend (API REST)
│   ├── models/
│   ├── routes/
│   ├── main.py
│   ├── app.py
│   ├── db.py
│   └── requirements.txt
├── web/              # Frontend (interfaz web)
│   ├── static/
│   ├── templates/
│   ├── main.py
│   ├── app.py
│   └── requirements.txt
├── Dockerfile.api    # Imagen Docker del API
├── Dockerfile.web    # Imagen Docker del Frontend
└── docker-compose.yml
```

### Services

#### 1. API (Backend) - Carpeta `api/`
- **Puerto**: 8000
- **Dockerfile**: `Dockerfile.api`
- **Punto de entrada**: `api/main.py`
- **Responsabilidades**:
  - Endpoints REST JSON (`/productos`, `/health`, `/ready`, etc.)
  - Conexión a base de datos PostgreSQL
  - Lógica de negocio y operaciones CRUD

#### 2. Web (Frontend) - Carpeta `web/`
- **Puerto**: 3000
- **Dockerfile**: `Dockerfile.web`
- **Punto de entrada**: `web/main.py`
- **Responsabilidades**:
  - Servir la interfaz HTML (templates Jinja2)
  - Servir archivos estáticos (CSS, JS)
  - Actuar como proxy entre el navegador y el API backend

#### 3. DB (Base de datos)
- **Puerto**: 5432 (interno)
- **Imagen**: `postgres:15`
- **Usado por**: Servicio API

## How to run the application

### Option 1: Docker Compose (Recommended)

```bash
# Build and start all services
docker compose up --build

# Or in detached mode (background)
docker compose up --build -d

# View logs
docker compose logs -f

# View logs of a specific service
docker compose logs -f api
docker compose logs -f web

# Stop services
docker compose down
```

Once the services are running:

- **Web Interface**: http://localhost:3000
- **API Direct**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **Health checks**:
  - API: http://localhost:8000/health
  - Frontend: http://localhost:3000/health

### Option 2: Manual Build of Each Service

```bash
# Build API image
docker build -t aos-api:latest -f Dockerfile.api .

# Build Frontend image
docker build -t aos-web:latest -f Dockerfile.web .

# Create custom network
docker network create aos-network

# Run database
docker run -d \
  --name aos-db \
  --network aos-network \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=aosdb \
  postgres:15

# Run API
docker run -d \
  --name aos-api \
  --network aos-network \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://postgres:postgres@aos-db:5432/aosdb \
  aos-api:latest

# Run Frontend
docker run -d \
  --name aos-web \
  --network aos-network \
  -p 3000:3000 \
  -e API_URL=http://aos-api:8000 \
  aos-web:latest
```

### Option 3: Local Development (without Docker)

#### Prerequisites
- PostgreSQL running locally (or skip `DATABASE_URL` to use in-memory mode)
- Python 3.8+

#### Running the API

**From the project root directory** (`/home/ppujol/AOS-Web/`):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r api/requirements.txt

# Run from the root directory with the module syntax
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Or set DATABASE_URL if you want to use PostgreSQL
export DATABASE_URL=postgresql://user:password@localhost:5432/aosdb
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

#### Running the Web Frontend

**From the project root directory** (`/home/ppujol/AOS-Web/`), in a **new terminal**:

```bash
source venv/bin/activate  # Use the same venv from above

pip install -r web/requirements.txt

# Set API URL to point to the local API
export API_URL=http://localhost:8000

# Run from the root directory with the module syntax
python -m uvicorn web.main:app --reload --host 0.0.0.0 --port 3000
```

#### Accessing the Application

Once both services are running:
- **Web Interface**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs

> **Important**: Always run from the **project root directory** using `python -m uvicorn`, not from inside the `api/` or `web/` folders. This ensures the `api` and `web` modules are correctly recognized in the Python path.

## Environment Variables

### API Service (`api`)
- `DATABASE_URL`: PostgreSQL connection URL (e.g., `postgresql://user:pass@host:5432/dbname`)
- `PYTHONUNBUFFERED`: Disables Python output buffering

### Web Service (`web`)
- `API_URL`: Internal URL of the API service (e.g., `http://api:8000`)
- `PYTHONUNBUFFERED`: Disables Python output buffering

### DB Service (`db`)
- `POSTGRES_USER`: PostgreSQL user
- `POSTGRES_PASSWORD`: PostgreSQL password
- `POSTGRES_DB`: Database name

## Architecture

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ http://localhost:3000
       ▼
┌─────────────────┐
│  Web (Frontend) │ :3000
│  - Templates    │
│  - Statics      │
│  - Proxy /api/* │
└────────┬────────┘
         │ http://api:8000 (Docker internal network)
         ▼
┌─────────────────┐
│   API (Backend) │ :8000
│  - REST JSON    │
│  - CRUD Logic   │
└────────┬────────┘
         │ postgresql://...@db:5432
         ▼
┌─────────────────┐
│   DB (Postgres) │ :5432
│  - Data persist │
└─────────────────┘
```

## Communication Flow

1. Browser loads the page from `http://localhost:3000/`
2. The `web` service renders HTML with Jinja2 and serves static files
3. JavaScript in the browser makes requests to `/api/*`
4. The `web` service acts as a proxy and forwards requests to `http://api:8000/*`
5. The `api` service processes the request and queries the database if needed
6. The `api` returns JSON to `web`, which forwards it to the browser

## Advantages of This Architecture

1. **Separation of concerns**: Backend and frontend can be developed, deployed, and scaled independently
2. **Horizontal scaling**: You can have multiple API instances without replicating the frontend
3. **Flexible deployment**:
   - In development: both services locally
   - In production: API in ECS/EC2, Frontend in CloudFront + S3 or lightweight web server
4. **Independent testing**: Each service can be tested separately
5. **Resource optimization**: Smaller and more specific Docker images for each service

## AWS Deployment

### Option 1: Elastic Beanstalk Multi-Container
Use `docker-compose.yml` as a base to create a `Dockerrun.aws.json` v2

### Option 2: ECS/Fargate
- Create separate task definitions for `api` and `web`
- Use ALB to route:
  - `/api/*` → API service
  - `/*` → Web service
- Connect API to RDS PostgreSQL

### Option 3: EC2 with Docker Compose
- Launch EC2 with Docker installed
- Clone repository and run `docker compose up -d`
- Configure ALB/Security Groups appropriately

To stop and remove containers:

```bash
docker compose down
```


### 5. **Testing the API with `pytest`**

Unit tests for the API are included in the `api/tests/test_sample.py` file. You can run the tests using `pytest`.

To run the tests, simply execute:

```bash
python -m pytest
```

## Api testing
#### GET `/productos`
- **Description**: Retrieve the complete list of available products.
- **Query Parameters**:
  - None
- **Example Request**:
  ```
  GET /productos
  ```
- **Response**:
  ```json
  [
    {
      "id": 1,
      "nombre": "Laptop",
      "precio": 999.99,
      "stock": 10
    },
    {
      "id": 2,
      "nombre": "Wireless Mouse",
      "precio": 25.50,
      "stock": 50
    }
  ]
  ```

#### GET `/productos/{product_id}`
- **Description**: Retrieve information about a specific product by its ID.
- **Query Parameters**:
  - No parameters
- **Example Request**:
  ```
  GET /productos/2
  ```
- **Response**:
  ```json
  {
    "id": 2,
    "nombre": "Wireless Mouse",
    "precio": 25.5,
    "stock": 50
  }
  ```

#### POST `/productos`
- **Description**: Upload a product.
- **Query Parameters**:
  - No parameters
- **Example Request**:
  ```
  POST /productos
  ```
- **Body example**:
  ```json
  {
    "id": 99,
    "nombre": "Headphones",
    "precio": 59.99,
    "stock": 100
  }
  ```
- **Response**:
  ```json
  {
    "mensaje": "Producto creado",
    "producto": {
      "id": 99,
      "nombre": "Headphones",
      "precio": 59.99,
      "stock": 100
    }
  }
  ```

#### PUT `/productos/{id}`
- **Description**: Replace all fields of an existing product.
- **Query Parameters**:
  - No parameters
- **Example Request**:
  ```
  PUT /productos/99
  ```
  - **Body example**:
  ```json
  {
    "mensaje": "Producto actualizado",
    "producto": {
      "id": 99,
      "nombre": "Headphones Pro",
      "precio": 79.99,
      "stock": 60
    }
  }
  ```

- **Response**:
  ```json
  {
    "mensaje": "Producto modificado",
    "producto": {
      "id": 99,
      "nombre": "Headphones",
      "precio": 49.99,
      "stock": 80
    }
  }
  ```

#### PATCH `/productos/{id}/modificar`
- **Description**: Partially update one or more product fields.
- **Query Parameters**:
  - No parameters
- **Example Request**:
  ```
  PATCH /productos/99/modificar
  ```
  - **Body example**:
  ```json
  {
    "precio": 49.99,
    "stock": 80
  }
  ```

- **Response**:
  ```json
  {
    "mensaje": "Producto modificado",
    "producto": {
      "id": 99,
      "nombre": "Headphones",
      "precio": 49.99,
      "stock": 80
    }
  }
  ```

#### DELETE `/productos/{id}`
- **Description**: Delete an existing product by its ID.
- **Query Parameters**:
  - No parameters
- **Example Request**:
  ```
  DELETE /products/2
  ```
- **Response**:
  ```json
  {
    "msg": "Deleted succesfully"
  }
  ```

#### GET `/health`
- **Description**: Check if the API service is healthy and operational.
- **Query Parameters**:
  - No parameters
- **Example Request**:
  ```
  GET /health
  ```
- **Response**:
  ```json
  {
    "status": "ok"
  }
  ```

#### GET `/ready`
- **Description**: Check if the application is ready to receive traffic (useful for AWS load balancer health checks).
- **Query Parameters**:
  - No parameters
- **Example Request**:
  ```
  GET /ready
  ```
- **Response**:
  ```json
  {
    "ready": true
  }
  ```


#### GET `/burn_cpu`
- **Description**: Simulate CPU load for autoscaling testing.
- **Query Parameters**:
  - iterations: (int) Number of load iterations.
  - work_secs: (float) Approximate duration of work per iteration.
- **Example Request**:
  ```
  GET /burn_cpu?iterations=5&work_secs=0.1
  ```
- **Response**:
  ```json
  {
    "estado": "carga simulada completada",
    "iteraciones": 5
  }
  ```

#### GET `/async_sleep`
- **Description**: Asynchronous endpoint that simulates non-blocking wait, useful to test concurrent requests.
- **Query Parameters**:
  - segundos: (float) Time to wait in seconds.
- **Example Request**:
  ```
  GET /async_sleep?segundos=0.5
  ```
- **Response**:
  ```json
  {
    "espera": 0.5
  }
  ```
  
  
## What's next?
- Implement a verification process to prevent adding invalid product types.
- Create a list.txt of basic products an id for clearly managment
- Create an enviroment for the products managment
- Simple web interface (GET on /) ?? MAYBE
