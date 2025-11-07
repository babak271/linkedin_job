"""FastAPI application instance and route definitions."""

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="LinkedIn Job Service",
        description="Starter FastAPI project managed by uv.",
        version="0.1.0",
    )

    @app.get("/", tags=["root"])
    async def read_root() -> dict[str, str]:
        return {"message": "LinkedIn Job service is ready"}

    @app.get("/health", tags=["health"])
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()

