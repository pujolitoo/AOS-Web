from fastapi import HTTPException, Query, APIRouter
from fastapi.responses import JSONResponse
import time
import asyncio
import signal
from typing import List
import os
from api.app import get_app
from api import db as _db
from api.models.product import *

router = APIRouter()

# ==============================
# DATOS EN MEMORIA
# ==============================
# Crear DB en un docker 
# Beanstalk, RDS o similar en producción
productos: List[Producto] = [
    Producto(id=1, nombre="Monitor 24\"", precio=129.99, stock=50),
    Producto(id=2, nombre="Teclado Mecánico", precio=89.50, stock=150),
    Producto(id=3, nombre="Ratón Inalámbrico", precio=35.99, stock=200),
]

# Flag de readiness
is_ready = True

# DB enabled when DATABASE_URL env var is set
DB_ENABLED = bool(os.getenv("DATABASE_URL"))


# ==============================
# ENDPOINTS CRUD
# ==============================

@router.get("/productos")
async def listar_productos():
    """Devuelve todos los productos"""
    if DB_ENABLED:
        return _db.list_products_db()
    return productos

@router.get("/productos/buscar")
async def buscar_producto(nombre: str = Query(..., description="Nombre o parte del nombre del producto")):
    """
    Busca productos cuyo nombre contenga el texto proporcionado (no sensible a mayúsculas).
    Ejemplo: /productos/buscar?nombre=teclado
    """
    source = _db.list_products_db() if DB_ENABLED else productos
    resultados = [p for p in source if nombre.lower() in p.nombre.lower()]
    if not resultados:
        return {"mensaje": "No se encontraron productos", "resultados": []}
    return {"resultados": resultados, "total": len(resultados)}

@router.get("/productos/{id}")
async def obtener_producto(id: int):
    """Obtiene un producto por su ID"""
    if DB_ENABLED:
        p = _db.get_product_db(id)
        if p:
            return p
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for p in productos:
        if p.id == id:
            return p
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@router.post("/productos")
async def crear_producto(producto: Producto):
    """Crea un nuevo producto"""
    if DB_ENABLED:
        if _db.get_product_db(producto.id) is not None:
            raise HTTPException(status_code=400, detail="Ya existe un producto con ese ID")
        _db.create_product_db(producto)
        return {"mensaje": "Producto creado", "producto": producto}
    if any(p.id == producto.id for p in productos):
        raise HTTPException(status_code=400, detail="Ya existe un producto con ese ID")
    productos.append(producto)
    return {"mensaje": "Producto creado", "producto": producto}

@router.put("/productos/{id}")
async def actualizar_producto(id: int, producto: Producto):
    """Actualiza un producto existente"""
    if DB_ENABLED:
        updated = _db.update_product_db(id, producto)
        if updated is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return {"mensaje": "Producto actualizado", "producto": producto}
    for i, p in enumerate(productos):
        if p.id == id:
            productos[i] = producto
            return {"mensaje": "Producto actualizado", "producto": producto}
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@router.delete("/productos/{id}")
async def eliminar_producto(id: int):
    """Elimina un producto por su ID"""
    if DB_ENABLED:
        deleted = _db.delete_product_db(id)
        if deleted:
            return {"mensaje": f"Producto con ID {id} eliminado"}
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for i, p in enumerate(productos):
        if p.id == id:
            productos.pop(i)
            return {"mensaje": f"Producto con ID {id} eliminado"}
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@router.patch("/productos/{id}/modificar")
async def modificar_producto(id: int, cambios: ProductoUpdate):
    """
    Modifica parcialmente un producto (solo los campos enviados).
    Ejemplo body: {"precio": 99.99, "stock": 120}
    """
    if DB_ENABLED:
        patched = _db.patch_product_db(id, cambios)
        if patched is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return {"mensaje": "Producto modificado parcialmente", "producto": patched}
    for p in productos:
        if p.id == id:
            if cambios.nombre is not None:
                p.nombre = cambios.nombre
            if cambios.precio is not None:
                p.precio = cambios.precio
            if cambios.stock is not None:
                p.stock = cambios.stock
            return {"mensaje": "Producto modificado parcialmente", "producto": p}
    raise HTTPException(status_code=404, detail="Producto no encontrado")



# ==============================
# ENDPOINTS DE MONITORIZACIÓN
# ==============================

@router.get("/health")
async def health():
    """Liveness probe — responde siempre mientras la app esté viva."""
    return {"status": "ok"}

@router.get("/ready")
async def ready():
    """Readiness probe — usado por AWS ALB o Kubernetes."""
    if is_ready:
        return {"ready": True}
    else:
        return JSONResponse(status_code=503, content={"ready": False})


# ==============================
# ENDPOINTS PARA PRUEBAS DE CARGA
# ==============================

@router.get("/burn_cpu")
def burn_cpu(iterations: int = Query(5, ge=1, le=500),
             work_secs: float = Query(0.5, ge=0.01, le=30.0)):
    """
    Simula trabajo intensivo de CPU (por ejemplo, cálculo de stock o precios masivos).
    Ideal para probar autoescalado basado en CPU.
    """
    for _ in range(iterations):
        end = time.time() + work_secs
        while time.time() < end:
            _ = sum(i * i for i in range(500))
    return {"estado": "completado", "iteraciones": iterations, "segundos_trabajo": work_secs}

@router.get("/async_sleep")
async def async_sleep(segundos: float = Query(2.0, ge=0.1, le=60.0)):
    """
    Simula una tarea I/O-bound (como esperar respuesta de un servicio externo o base de datos).
    """
    await asyncio.sleep(segundos)
    return {"espera": segundos}


# ==============================
# EVENTOS DE VIDA Y SEÑALES
# ==============================

@router.on_event("startup")
async def on_startup():
    get_app().state.start_time = time.time()
    # Inicializar DB si está configurada
    if DB_ENABLED:
        _db.init_db()
        print("📦 Conectado a la base de datos (DATABASE_URL)")
    print("🚀 Aplicación iniciada correctamente")

@router.on_event("shutdown")
async def on_shutdown():
    print("🧹 Apagando aplicación... limpieza completada.")

# Manejo de SIGTERM / SIGINT (para shutdown limpio en AWS)
def handle_sigterm(*_):
    global is_ready
    is_ready = False
    print("⚠️ SIGTERM recibido: marcando instancia como no lista...")
    time.sleep(2)
    print("🚪 Cerrando servidor FastAPI...")
    exit(0)

signal.signal(signal.SIGTERM, handle_sigterm)
signal.signal(signal.SIGINT, handle_sigterm)
