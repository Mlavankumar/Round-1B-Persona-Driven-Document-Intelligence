# Use an official Python slim image compatible with AMD64
FROM --platform=linux/amd64 python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LANG=C.UTF-8

# Create app directory
WORKDIR /app

# Copy requirements first for Docker caching
COPY requirements.txt .

# Install system dependencies and Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        poppler-utils \
        tesseract-ocr \
        tesseract-ocr-eng \
        libgl1 \
        libglib2.0-0 && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy your source code
COPY . .

# Make logs and output directories if needed
RUN mkdir -p /app/output /app/logs

# Expose a port if using a web interface (optional)
# EXPOSE 8000

# Set default command
CMD ["python", "main.py"]
