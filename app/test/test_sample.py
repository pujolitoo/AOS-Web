from fastapi.testclient import TestClient
from app.main import app
from app.database import *

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
    

def test_db_id_unicity():
    id_1 = db_put(Product.model_validate(
        {
            "name": "TEST",
            "desc": "aaaa",
            "price": 10.50
        }
    ))["id"]
    id_2 = db_put(Product.model_validate(
        {
            "name": "TEST2",
            "desc": "aaaa",
            "price": 10.50
        }
    ))["id"]
    
    db_delete_entry(id_1)
    
    id_3 = db_put(Product.model_validate(
        {
            "name": "TEST3",
            "desc": "aaaa",
            "price": 10.50
        }
    ))["id"]
    
    assert id_3 != id_2
    
    db_clear()
    
    
def test_db_remove():
    prod = db_put(Product.model_validate(
        {
            "name": "TEST",
            "desc": "aaaa",
            "price": 10.50
        }
    ))
    
    assert len(db_search(prod["name"])) == 1
    
    response = client.delete(f"/products/{prod["id"]}")
    
    assert response.status_code == 200
    
    assert len(db_search(prod["name"])) == 0
    
    db_clear()
    
    
def test_db_insert():
    testprod = {
        "name": "test_product",
        "desc": "A test product for testing purposes only",
        "price": 33.5
    }
    response = client.post("/products", json=testprod)
    
    assert response.status_code == 200
    
    print(str(response.json()))
    
    prod_id = response.json()['id']
    
    found = False
    try:
        prod = db_get(prod_id)
        prod_query = Product.model_validate(testprod)
        assert prod == prod_query
        found = True
    except:
        pass
    
    assert found == True
    
    db_clear()
    db_remove()

