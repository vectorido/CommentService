import uvicorn

from src.infrastructure.config import settings


if __name__ == "__main__":
    uvicorn.run(
        "src.presentation.api.app:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug,
    )

