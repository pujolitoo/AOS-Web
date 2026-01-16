"""
Punto de entrada para el servicio Web (frontend).
Sirve la interfaz HTML y archivos estáticos.
Se comunica con el servicio API para obtener datos.
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os
import httpx

app = FastAPI(title="AOS Web Frontend")

# Configurar plantillas y estáticos
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# URL del servicio API (configurable via env var)
API_URL = os.getenv("API_URL", "http://api:8000")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Página principal que muestra la lista de productos"""
    try:
        # Llamar al API para obtener productos
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/productos", timeout=5.0)
            productos = response.json() if response.status_code == 200 else []
            
            # Obtener health para calcular uptime aproximado
            try:
                health_response = await client.get(f"{API_URL}/health", timeout=2.0)
                uptime = 0  # El API no devuelve uptime en /health, ponemos 0
            except:
                uptime = 0
    except Exception as e:
        print(f"Error conectando con API: {e}")
        productos = []
        uptime = 0
    
    return templates.TemplateResponse(
        "products.html", 
        {"request": request, "productos": productos, "uptime": uptime}
    )


# Proxy endpoints para que el frontend JavaScript pueda llamar al API
# Todas las peticiones a /api/* se reenvían al servicio backend
@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_api(request: Request, path: str):
    """Proxy todas las peticiones /api/* al servicio backend API"""
    async with httpx.AsyncClient() as client:
        # Construir la URL del backend
        url = f"{API_URL}/{path}"
        
        # Copiar query params
        if request.url.query:
            url = f"{url}?{request.url.query}"
        
        # Leer el body si existe
        body = await request.body() if request.method in ["POST", "PUT", "PATCH"] else None
        
        # Hacer la petición al backend
        try:
            response = await client.request(
                method=request.method,
                url=url,
                headers={k: v for k, v in request.headers.items() if k.lower() not in ["host", "connection"]},
                content=body,
                timeout=30.0
            )
            
            # Devolver la respuesta del backend
            return JSONResponse(
                content=response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text,
                status_code=response.status_code,
                headers={k: v for k, v in response.headers.items() if k.lower() not in ["content-encoding", "transfer-encoding"]}
            )
        except httpx.RequestError as e:
            return JSONResponse(
                content={"error": f"Error conectando con el API: {str(e)}"},
                status_code=503
            )


@app.get("/health")
async def health():
    """Health check del frontend"""
    return {"status": "ok", "service": "frontend"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
