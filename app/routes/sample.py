from fastapi import FastAPI, HTTPException, Query, APIRouter
from fastapi.responses import JSONResponse
import time
import asyncio
import signal
from typing import List, Optional
from app.app import get_app

router = APIRouter()

# ==============================
# MODELOS
# ==============================

from app.models.product import *


# ==============================
# DATOS EN MEMORIA
# ==============================

productos: List[Producto] = [
    Producto(id=1, nombre="Monitor 24\"", precio=129.99, stock=50),
    Producto(id=2, nombre="Teclado Mecánico", precio=89.50, stock=150),
    Producto(id=3, nombre="Ratón Inalámbrico", precio=35.99, stock=200),
]

# Flag de readiness
is_ready = True


# ==============================
# ENDPOINTS CRUD
# ==============================

@router.get("/")
async def root():
    uptime = int(time.time() - get_app().state.start_time)
    return {"mensaje": "API de Gestión de Productos", "uptime_segundos": uptime}

@router.get("/productos")
async def listar_productos():
    """Devuelve todos los productos"""
    return productos

@router.get("/productos/buscar")
async def buscar_producto(nombre: str = Query(..., description="Nombre o parte del nombre del producto")):
    """
    Busca productos cuyo nombre contenga el texto proporcionado (no sensible a mayúsculas).
    Ejemplo: /productos/buscar?nombre=teclado
    """
    resultados = [p for p in productos if nombre.lower() in p.nombre.lower()]
    if not resultados:
        return {"mensaje": "No se encontraron productos", "resultados": []}
    return {"resultados": resultados, "total": len(resultados)}

@router.get("/productos/{id}")
async def obtener_producto(id: int):
    """Obtiene un producto por su ID"""
    for p in productos:
        if p.id == id:
            return p
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@router.post("/productos")
async def crear_producto(producto: Producto):
    """Crea un nuevo producto"""
    if any(p.id == producto.id for p in productos):
        raise HTTPException(status_code=400, detail="Ya existe un producto con ese ID")
    productos.append(producto)
    return {"mensaje": "Producto creado", "producto": producto}

@router.put("/productos/{id}")
async def actualizar_producto(id: int, producto: Producto):
    """Actualiza un producto existente"""
    for i, p in enumerate(productos):
        if p.id == id:
            productos[i] = producto
            return {"mensaje": "Producto actualizado", "producto": producto}
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@router.delete("/productos/{id}")
async def eliminar_producto(id: int):
    """Elimina un producto por su ID"""
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