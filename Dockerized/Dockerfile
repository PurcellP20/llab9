FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY usaf_data_seed.py .
COPY templates/ templates/
COPY static/ static/

# Expose Flask port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]