FROM python:3.11-slim

WORKDIR /app
COPY app /app

ENV PYTHONPATH=/app

COPY app/fastapi/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port $PORT"]
CMD ["sh", "-c", "uvicorn app.fastapi.app:app --host 0.0.0.0 --port 8080"]
