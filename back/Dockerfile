FROM python:3.11-alpine

RUN adduser -DH user
USER user

WORKDIR /app

ENV PYTHONPATH='/app'

COPY requirements.txt .

RUN python -m venv .venv; \
    .venv/bin/pip install --no-cache-dir -r requirements.txt

COPY src/ .

CMD [".venv/bin/python", "main.py"]
