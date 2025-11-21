from app.app import app
from app.routes import sample
from fastapi.staticfiles import StaticFiles
import os


# Include the sample routes
app.include_router(sample.router)

# Serve static files from `app/static` at `/static`
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

