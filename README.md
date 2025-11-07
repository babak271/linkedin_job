# FastAPI App

Basic FastAPI project managed with [uv](https://docs.astral.sh/uv/).

## Getting started

```bash
# install dependencies
uv sync

# run the development server
FASTAPI_RELOAD=1 uv run linkedin_job
```

The server listens on `http://127.0.0.1:8000` by default. Set `FASTAPI_HOST` / `FASTAPI_PORT` / `FASTAPI_RELOAD` to override host, port, and autoreload behavior.

Alternatively, you can run Uvicorn directly:

```bash
uv run uvicorn linkedin_job.app:app --reload --host 0.0.0.0 --port 8080
```
