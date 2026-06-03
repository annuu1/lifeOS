FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /data

COPY backend/app ./app
COPY .env .

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

CMD ["python", "app/main.py"]
