from fastapi import FastAPI

app = FastAPI(title="AOS Web Frontend")

def get_app() -> FastAPI:
    global app
    return app
