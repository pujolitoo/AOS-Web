"""
Punto de entrada para el servicio API (backend).
Solo expone endpoints JSON, sin servir archivos estáticos ni templates.
"""
from api.app import app
from api.routes import sample
from api.db import init_db

# Include the API routes
app.include_router(sample.router)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
