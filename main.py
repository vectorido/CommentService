import uvicorn

from src.infrastructure.config import settings

from fastapi import FastAPI

app = FastAPI(redoc_url="/redoc")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "name": f"Item {item_id}"}


if __name__ == "__main__":
    uvicorn.run(
        "src.presentation.api.app:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug,
    )

