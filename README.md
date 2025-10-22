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
#### GET `/products`
- **Description**: Search a product.
- **Query Parameters**:
  - `search`: Search string.
- **Example Request**:
  ```
  GET /products?search=bike
  ```
- **Response**:
  ```json
  {
    "result": "HelloWorld"
  }
  ```
  
## What's next?
- Implement a verification process to prevent adding invalid product types.
- 
