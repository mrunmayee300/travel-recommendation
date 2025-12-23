import logging
import os
from functools import lru_cache
from typing import Any, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------


class Settings:
    """Application settings loaded from environment."""

    app_name: str = os.getenv("APP_NAME", "Travel Recommendation API")
    env: str = os.getenv("APP_ENV", "development")
    allow_origins: str = os.getenv("CORS_ALLOW_ORIGINS", "*")
    allow_methods: str = os.getenv("CORS_ALLOW_METHODS", "GET,POST,PUT,DELETE,OPTIONS")
    allow_headers: str = os.getenv("CORS_ALLOW_HEADERS", "*")


@lru_cache()
def get_settings() -> Settings:
    return Settings()


# -----------------------------------------------------------------------------
# Application factory
# -----------------------------------------------------------------------------


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description="Travel recommendation, itinerary generation, and nearby expansion API.",
    )

    configure_logging(settings)
    configure_cors(app, settings)
    register_routes(app)

    return app


def configure_logging(settings: Settings) -> None:
    log_level = logging.DEBUG if settings.env == "development" else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)


def configure_cors(app: FastAPI, settings: Settings) -> None:
    origins = [origin.strip() for origin in settings.allow_origins.split(",") if origin]
    methods = [method.strip() for method in settings.allow_methods.split(",") if method]
    headers = [header.strip() for header in settings.allow_headers.split(",") if header]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins or ["*"],
        allow_credentials=True,
        allow_methods=methods or ["*"],
        allow_headers=headers or ["*"],
    )


def register_routes(app: FastAPI) -> None:
    from app.routes.health import router as health_router
    from app.routes.itinerary import router as itinerary_router
    from app.routes.nearby import router as nearby_router
    from app.routes.recommendations import router as recommendations_router

    app.include_router(health_router, prefix="/api")
    app.include_router(recommendations_router, prefix="/api")
    app.include_router(itinerary_router, prefix="/api")
    app.include_router(nearby_router, prefix="/api")


app = create_app()

# -----------------------------------------------------------------------------
# Metadata endpoint for debugging
# -----------------------------------------------------------------------------


@app.get("/api/meta", tags=["meta"])
def get_meta() -> Dict[str, Any]:
    settings = get_settings()
    return {
        "app": settings.app_name,
        "env": settings.env,
    }


