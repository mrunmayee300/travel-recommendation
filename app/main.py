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
    configure_cors(app)
    register_routes(app)

    return app


def configure_logging(settings: Settings) -> None:
    log_level = logging.DEBUG if settings.env == "development" else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)


def configure_cors(app: FastAPI) -> None:
    # Get CORS origins from environment or use defaults
    cors_origins_env = os.getenv("CORS_ALLOW_ORIGINS", "")
    
    if cors_origins_env:
        # Split by comma and strip whitespace
        origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]
    else:
        # Default origins - allow all for development
        origins = ["*"]
    
    # For production, allow specific origins
    # If "*" is in the list, allow all origins
    allow_all = "*" in origins or len(origins) == 0

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins if not allow_all else ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_routes(app: FastAPI) -> None:
    from app.routes.health import router as health_router
    from app.routes.recommendations import router as recommendations_router
    from app.routes.itinerary import router as itinerary_router
    from app.routes.nearby import router as nearby_router

    app.include_router(health_router, prefix="/api")
    app.include_router(recommendations_router, prefix="/api")
    app.include_router(itinerary_router, prefix="/api")
    app.include_router(nearby_router, prefix="/api")


app = create_app()


# -----------------------------------------------------------------------------
# Metadata + Debug Endpoints
# -----------------------------------------------------------------------------

@app.get("/api/meta", tags=["meta"])
def get_meta() -> Dict[str, Any]:
    settings = get_settings()
    return {
        "app": settings.app_name,
        "env": settings.env,
    }


@app.get("/")
def root():
    return {"status": "ok", "message": "Travel Recommendation API active"}
