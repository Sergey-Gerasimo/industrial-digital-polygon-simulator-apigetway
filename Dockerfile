FROM python:3.13-slim AS builder

WORKDIR /app

RUN pip install --no-cache-dir poetry==2.1.1

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main


FROM python:3.13-slim AS runtime

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY application ./application

ENV PYTHONPATH="/app/application"
ENV HOST=0.0.0.0
ENV PORT=8000
ENV LOG_LEVEL=INFO

EXPOSE 8000

CMD ["uvicorn", "application.main:app", "--host", "0.0.0.0", "--port", "8000"]

