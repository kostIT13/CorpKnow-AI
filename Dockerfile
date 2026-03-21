FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

# Системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Установка uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Копируем зависимости
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости
RUN uv sync --frozen --no-dev

# 🔹 КРИТИЧНО: Добавляем .venv/bin в PATH
ENV PATH="/app/.venv/bin:$PATH"

# Копируем код
COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini ./

EXPOSE 8000

# 🔹 Теперь uvicorn найдётся без "uv run"
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]