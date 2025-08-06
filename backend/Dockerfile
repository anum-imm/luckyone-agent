# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt /app/
COPY .env /app/
# Install Python dependencies
RUN pip install -r requirements.txt

# Copy backend code
COPY . /app

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
