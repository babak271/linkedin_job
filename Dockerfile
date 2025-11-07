# syntax=docker/dockerfile:1.4

FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system packages required for building wheels
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --upgrade pip \
    && pip install --no-cache-dir .

EXPOSE 8080
CMD ["uvicorn", "linked_job.app:app", "--host", "0.0.0.0", "--port", "8080"]
