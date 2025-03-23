FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install ping
RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy code except .env, logs, certs
COPY app/ app/
COPY templates/ templates/
COPY static/ static/
COPY README.md README.md

EXPOSE ${PORT:-443}

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-443} \
--ssl-certfile /app/certs/cert.pem --ssl-keyfile /app/certs/key.pem --reload"]
