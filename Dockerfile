FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]