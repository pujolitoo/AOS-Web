from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Concatenate two query parameters
@app.get("/concat")
def concatenate(param1: str, param2: str):
    return {"result": param1 + param2}

# Return the length of a string
@app.get("/length")
def length_of_string(string: str):
    return {"length": len(string)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
