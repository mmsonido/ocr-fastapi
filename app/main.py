"""
Main entry point for the FastAPI application.
Mounts static files and includes API endpoints.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import endpoints
from typing import Any

def create_app() -> FastAPI:
    """
    Application factory for FastAPI app.
    """
    app = FastAPI()
    app.include_router(endpoints.router)
    app.mount("/static", StaticFiles(directory="static"), name="static")
    return app

app = create_app()