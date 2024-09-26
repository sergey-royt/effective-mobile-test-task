FROM python:3.12-alpine AS builder

WORKDIR /app

COPY . .

RUN python -m pip install --no-cache-dir poetry==1.4.2 \
  && poetry config virtualenvs.in-project true \
  && poetry install --without dev,test --no-interaction --no-ansi
  
CMD [".venv/bin/uvicorn", "warehouse_manager.app:app", "--host", "0.0.0.0", "--port", "8000"]
