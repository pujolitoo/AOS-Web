# ARQUITECTURA ORIENTADA A SERVICIOS 
## Curso 2025-26 
## FastAPI Project


# FastAPI Project

This is a simple FastAPI-based project that includes GET and POST services. It includes:
- A POST endpoint for processing JSON data.
- A GET endpoint for concatenating two strings.
- A GET endpoint for calculating the length of a string.

## Project Structure

```bash
aossample/
│
├── app/
│   ├── __init__.py           # Initializes the app as a package
│   ├── main.py               # Main entry point for the FastAPI application
│   ├── routes/
│   │   ├── __init__.py       # Initializes the routes as a package
│   │   └── sample.py         # Contains the API routes (POST/GET)
│   ├── models/
│   │   ├── __init__.py       
│   │   └── item.py           # Defines the data models using Pydantic
│   ├── tests/
│   │   ├── __init__.py       
│   │   └── test_sample.py    # Contains the unit tests for the API
│   └── requirements.txt      # Dependencies for the project
│
├── venv/                     # Python virtual environment
└── README.md                 # Project documentation
```

## Project Setup

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

### API Endpoints

#### POST `/process`
- **Description**: Accepts a JSON object with two integers and returns their sum.
- **Request Body**:
  ```json
  {
    "value1": 10,
    "value2": 5
  }
  ```
- **Response**:
  ```json
  {
    "result": 15
  }
  ```

#### GET `/concat`
- **Description**: Concatenates two query parameters.
- **Query Parameters**:
  - `param1`: First string to concatenate.
  - `param2`: Second string to concatenate.
- **Example Request**:
  ```
  GET /concat?param1=Hello&param2=World
  ```
- **Response**:
  ```json
  {
    "result": "HelloWorld"
  }
  ```

#### GET `/length`
- **Description**: Returns the length of a given string.
- **Query Parameter**:
  - `string`: The string whose length is to be calculated.
- **Example Request**:
  ```
  GET /length?string=FastAPI
  ```
- **Response**:
  ```json
  {
    "length": 7
  }
  ```

### 6. **Generate `requirements.txt`**

To generate a `requirements.txt` file after adding new dependencies, run the following command:

```bash
pip freeze > app/requirements.txt
```

This will capture the current list of installed packages into the `requirements.txt` file.

---

### Notes

- The `app/routes/sample.py` file contains all the route handlers for GET and POST methods.
- The tests are written using `pytest`, and they can be found in `app/tests/test_sample.py`.

For any issues or contributions, please feel free to open a pull request or an issue.
