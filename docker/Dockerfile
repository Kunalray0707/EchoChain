# Production Dockerfile for EchoChain Lakehouse Engine
FROM python:3.12-slim

# Install Java 17 for Spark runtime & system utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-17-jre-headless \
    curl \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set Java & Spark environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

# Create data & log directories
RUN mkdir -p data/raw data/bronze data/silver data/gold logs

# Expose Spark UI port
EXPOSE 4040 8080

CMD ["python", "scripts/run_daily_pipeline.py"]
