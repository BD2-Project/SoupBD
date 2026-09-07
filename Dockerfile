# syntax=docker/dockerfile:1

FROM ghcr.io/astral-sh/uv:0.11.16 AS build
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

FROM python:3.12-slim AS runtime
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=build /app/.venv ./.venv
COPY engine ./engine
CMD ["python", "-c", "import engine; print('soupdb engine ready')"]