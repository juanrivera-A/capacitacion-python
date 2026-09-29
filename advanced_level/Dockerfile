
# STAGE 1: Builder

FROM python:3.13-slim AS builder

# Evitar escritura de archivos .pyc y forzar stdout/stderr sin buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

# Instalar dependencias del sistema mínimas para compilar
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

# Copiar archivos de definición de dependencias
COPY pyproject.toml poetry.lock* ./

# Instalar dependencias del proyecto (solo de producción)
RUN poetry install --no-root --only main


# STAGE 2: Runtime

FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    PORT=8000

# Instalar dependencias en tiempo de ejecución (ej. curl para el healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Principio de menor privilegio: Crear usuario no-root
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -s /bin/sh -m appuser

WORKDIR /app

# Copiar el entorno virtual con todas las dependencias desde el builder
COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv

# Copiar el código fuente de la aplicación desde src/
COPY --chown=appuser:appgroup ./src /app/src

# Cambiar al usuario no administrativo
USER appuser

EXPOSE 8000

# Healthcheck para monitorear el estado del contenedor
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/orders/health || exit 1

# Comando por defecto para iniciar la aplicación FastAPI
CMD ["uvicorn", "src.modulo01.main:app", "--host", "0.0.0.0", "--port", "8000"]