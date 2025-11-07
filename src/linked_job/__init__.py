from __future__ import annotations

import os

import uvicorn

from .app import app, create_app

__all__ = ("app", "create_app", "main")


def _should_reload() -> bool:
    value = os.environ.get("FASTAPI_RELOAD", "").lower()
    return value in {"1", "true", "yes"}


def main() -> None:
    """Run the FastAPI development server."""
    host = os.environ.get("FASTAPI_HOST", "127.0.0.1")
    port = int(os.environ.get("FASTAPI_PORT", "8005"))
    uvicorn.run(
        "linked_job.app:app",
        host=host,
        port=port,
        reload=_should_reload(),
    )
