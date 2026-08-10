from __future__ import annotations

from pathlib import Path

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Register ORM entities.
import app.database.entities

from app.api.routers.chat_router import (
    router as chat_router,
)
from app.api.routers.conversation_router import (
    router as conversation_router,
)
from app.api.routers.health_router import (
    router as health_router,
)
from app.api.routers.logs_router import (
    router as logs_router,
)
from app.api.routers.map import (
    router as map_router,
)
from app.core.exceptions import (
    register_exception_handlers,
)

__all__ = (
    "app",
    "create_app",
)

# ==========================================================
# MIDDLEWARES
# ==========================================================

_ALLOWED_ORIGINS = (
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
)


def _configure_middlewares(
    *,
    app: FastAPI,
) -> None:
    """
    Configure all application middlewares.
    """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(_ALLOWED_ORIGINS),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# ==========================================================
# ROUTERS
# ==========================================================

def _register_routers(
    *,
    app: FastAPI,
) -> None:
    """
    Register all API routers.
    """

    app.include_router(health_router)
    app.include_router(conversation_router)
    app.include_router(chat_router)
    app.include_router(logs_router)
    app.include_router(map_router)


# ==========================================================
# APPLICATION
# ==========================================================

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """

    application = FastAPI(
        title="IMMO AI API",
        version="1.0.0",
    )

    # ======================================================
    # STORAGE
    # ======================================================

    storage_path = (
        Path.cwd()
        / "storage"
    ).resolve()

    storage_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        f"[STORAGE] Serving files from: {storage_path}"
    )

    application.mount(
        "/storage",
        StaticFiles(
            directory=str(storage_path),
        ),
        name="storage",
    )

    # ======================================================
    # EXCEPTION HANDLERS
    # ======================================================

    register_exception_handlers(
        app=application,
    )

    # ======================================================
    # MIDDLEWARES
    # ======================================================

    _configure_middlewares(
        app=application,
    )

    # ======================================================
    # ROUTERS
    # ======================================================

    _register_routers(
        app=application,
    )

    return application


app = create_app()


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )