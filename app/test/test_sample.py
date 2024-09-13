from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test for POST /process
def test_process_data():
    response = client.post("/process", json={"value1": 10, "value2": 5})
    assert response.status_code == 200
    assert response.json() == {"result": 15}

# Test for POST /process with invalid data
def test_process_data_invalid():
    response = client.post("/process", json={"value1": 10})
    assert response.status_code == 422

# Test for GET /concat
def test_concatenate():
    response = client.get("/concat?param1=Hello&param2=World")
    assert response.status_code == 200
    assert response.json() == {"result": "HelloWorld"}

# Test for GET /length
def test_length_of_string():
    response = client.get("/length?string=FastAPI")
    assert response.status_code == 200
    assert response.json() == {"length": 7}

