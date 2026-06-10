from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.routers import (category_r, comment_r, location_r, post_r, user_r, auth_r)
from src.logging_config import setup_logging
from src.widdleware.log_middleware import LoggingMiddleware


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI()

    app.add_middleware(LoggingMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_r.router)
    app.include_router(location_r.router)
    app.include_router(category_r.router)
    app.include_router(user_r.router)
    app.include_router(comment_r.router)
    app.include_router(post_r.router)

    return app


app = create_app()
