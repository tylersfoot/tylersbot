# syntax=docker/dockerfile:1
# Dockerfile for tylersbot — multistage + uv + Python 3.13

FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

ENV UV_COMPILE_BYTECODE=0 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv pip install -r pyproject.toml --system --no-cache

FROM python:3.13-alpine

RUN addgroup -S app && adduser -S -G app app

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.13 /usr/local/lib/python3.13

COPY --chown=app:app src/ ./src/

RUN mkdir -p /app/data && chown app:app /app/data

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

USER app

CMD ["python", "src/bot.py"]

LABEL maintainer="tylersfoot"
LABEL org.opencontainers.image.source="https://github.com/tylersfoot/tylersbot"
