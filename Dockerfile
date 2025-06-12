FROM python:3.11-slim

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc libffi-dev libxml2-dev libxslt1-dev libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app
COPY scraper ./scraper
COPY startup.sh ./startup.sh

# Make script executable
RUN chmod +x startup.sh

# Create output directory
RUN mkdir -p /app/scraper/output

# Expose port
EXPOSE 80

# Default command
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80", "--workers", "2", "--timeout", "60"]
