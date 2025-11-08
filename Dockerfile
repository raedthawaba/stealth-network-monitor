# Stealth Network Monitor - Docker Image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    net-tools \
    netstat-nat \
    iproute2 \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY stealth_network_spy_fixed.py .
COPY main.py .
COPY config.yaml .

# Create necessary directories
RUN mkdir -p data logs exports backups

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO
ENV MONITORING_INTERVAL=30

# Create a non-root user for security
RUN useradd -m -u 1000 monitor && \
    chown -R monitor:monitor /app
USER monitor

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python3 -c "import sqlite3; sqlite3.connect('/app/data/monitor.db').close()" || exit 1

# Expose port for potential web interface
EXPOSE 8080

# Run the application
CMD ["python3", "stealth_network_spy_fixed.py"]