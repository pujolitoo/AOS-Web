# Este archivo es para evitar importaciones cíclicas

from fastapi import FastAPI

app = FastAPI(title="Gestión de Productos - AutoScaling Demo")

def get_app() -> FastAPI:
    global app
    return app
