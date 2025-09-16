FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Create data directories
RUN mkdir -p /app/data/{repos,chunks,cache}

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "src.impact_analysis.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
