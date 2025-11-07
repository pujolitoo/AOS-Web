from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ============================
# PRUEBAS DE ESTADO Y HEALTH
# ============================

def test_health_check():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_ready_check():
    r = client.get("/ready")
    assert r.status_code in [200, 503]  # puede variar si cambia is_ready
    assert "ready" in r.json()


# ============================
# PRUEBAS CRUD DE PRODUCTOS
# ============================

def test_listar_productos():
    r = client.get("/productos")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "nombre" in data[0]

def test_crear_producto():
    nuevo = {"id": 99, "nombre": "Auriculares", "precio": 59.99, "stock": 100}
    r = client.post("/productos", json=nuevo)
    assert r.status_code == 200
    body = r.json()
    assert body["mensaje"] == "Producto creado"
    assert body["producto"]["nombre"] == "Auriculares"

def test_obtener_producto():
    r = client.get("/productos/99")
    assert r.status_code == 200
    data = r.json()
    assert data["nombre"] == "Auriculares"

def test_modificar_producto():
    mod = {"precio": 49.99, "stock": 80}
    r = client.patch("/productos/99/modificar", json=mod)
    assert r.status_code == 200
    p = r.json()["producto"]
    assert p["precio"] == 49.99
    assert p["stock"] == 80

def test_actualizar_producto_completo():
    actualizado = {"id": 99, "nombre": "Auriculares Pro", "precio": 79.99, "stock": 60}
    r = client.put("/productos/99", json=actualizado)
    assert r.status_code == 200
    data = r.json()["producto"]
    assert data["nombre"] == "Auriculares Pro"

def test_buscar_producto():
    r = client.get("/productos/buscar?nombre=Auriculares")
    assert r.status_code == 200
    data = r.json()
    assert "resultados" in data
    assert len(data["resultados"]) >= 1

def test_eliminar_producto():
    r = client.delete("/productos/99")
    assert r.status_code == 200
    msg = r.json()["mensaje"]
    assert "eliminado" in msg

def test_eliminar_inexistente():
    r = client.delete("/productos/9999")
    assert r.status_code == 404


# ============================
# PRUEBAS DE CARGA SIMULADA
# ============================

def test_burn_cpu_endpoint():
    r = client.get("/burn_cpu?iterations=2&work_secs=0.1")
    assert r.status_code == 200
    assert "estado" in r.json()

def test_async_sleep_endpoint():
    r = client.get("/async_sleep?segundos=0.2")
    assert r.status_code == 200
    assert r.json()["espera"] == 0.2