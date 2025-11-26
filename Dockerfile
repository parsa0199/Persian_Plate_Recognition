# Use Python 3.9 slim as the base image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Install necessary system packages
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY utils.py .
COPY config.py .
COPY utils/ ./utils/
COPY weights/ ./weights/

# Healthcheck to verify the application is running
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Expose the port
EXPOSE 8501

# Entry point command to start the Streamlit application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]