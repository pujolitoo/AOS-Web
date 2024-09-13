from fastapi import FastAPI
from app.routes import sample

app = FastAPI()

# Include the sample routes
app.include_router(sample.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
