# Product Management Application

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

## How to run the application
### 1. **Clone the Project**

First, clone the project repository to your local machine:

```bash
git clone https://github.com/mcastrol/aossample.git
cd aossample
```

### 2. **Create and Activate a Python Virtual Environment**

Create a virtual environment to manage dependencies. This ensures that project-specific packages are isolated from your global Python environment.

**On Linux/macOS**:
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows**:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. **Install Dependencies from `requirements.txt`**

Once the virtual environment is activated, install the project dependencies using `requirements.txt`.

```bash
pip install -r app/requirements.txt
```

This will install all the necessary packages such as FastAPI, Uvicorn, and Pytest.

### 4. **Run the FastAPI Application**

To run the FastAPI application, use the following command:

```bash
uvicorn app.main:app --reload
```

The `--reload` option is useful in development mode because it reloads the app when changes are made to the code.

By default, the app will be available at `http://127.0.0.1:8000`. You can access the API documentation via:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### 5. **Testing the API with `pytest`**

Unit tests for the API are included in the `app/tests/test_sample.py` file. You can run the tests using `pytest`.

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
