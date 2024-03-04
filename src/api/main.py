from typing import Optional

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


def start_server():
    """Launched with `poetry run start_server` at root level"""
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)