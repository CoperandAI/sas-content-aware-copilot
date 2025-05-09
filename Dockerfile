# Use official Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY Requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r Requirements.txt

# Copy project files
COPY . .

# Expose the default Dash port
EXPOSE 8050

# Run the Dash app (change filename if needed)
CMD ["python", "app.py"]
