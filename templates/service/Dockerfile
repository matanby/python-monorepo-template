# syntax=docker/dockerfile:1
FROM python:3.14-slim-trixie AS builder
COPY --from=ghcr.io/astral-sh/uv:0.13.4 /uv /usr/local/bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never
WORKDIR /app
# Build with the repository root as context so workspace dependencies are available.
COPY . .
# Optional CA secret supports builds behind an HTTPS proxy.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=secret,id=proxy_ca \
    if [ -f /run/secrets/proxy_ca ]; then export SSL_CERT_FILE=/run/secrets/proxy_ca; fi; \
    uv sync --locked --no-dev --no-editable --package "<SERVICE-NAME>"

FROM python:3.14-slim-trixie AS runtime
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PATH="/app/.venv/bin:$PATH"
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
USER 10001:10001
CMD ["<SERVICE-NAME>"]
