from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

from app.core.exceptions import (
    register_exception_handlers,
)


app = FastAPI(

    title="IMMO AI API",

    version="1.0.0",

)

# ==========================================================
# Exception Handlers
# ==========================================================

register_exception_handlers(
    app
)

# ==========================================================
# CORS
# ==========================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "http://localhost:3000",

        "http://127.0.0.1:3000",

        "http://localhost:5173",

        "http://127.0.0.1:5173",

    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)

# ==========================================================
# API Routers
# ==========================================================

app.include_router(

    health_router

)

app.include_router(

    conversation_router

)

app.include_router(

    chat_router

)

app.include_router(

    logs_router

)