# Use Python 3.10 slim as the base image
# BUILD_DATE: 2025-11-27-v2 - Force rebuild to fix NameError
FROM python:3.10-slim

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

# Upgrade pip to latest version to avoid version warnings
RUN pip install --upgrade pip --no-cache-dir --quiet

# Install Python dependencies
# Note: The "running as root" warning is expected and harmless in Docker containers
RUN pip install --no-cache-dir --quiet -r requirements.txt

# Copy application files (app.py copied last to break cache)
COPY utils.py .
COPY config.py .
COPY utils/ ./utils/
# Create weights directory (will be mounted from Liara disk at runtime)
# Note: If weights exist locally, they'll be copied. In production on Liara,
# the disk mount at /app/weights will override any copied files.
RUN mkdir -p ./weights
COPY weights/ ./weights/
COPY valid_plates.csv .

# Copy app.py LAST and verify it's the correct version
# This ensures Docker doesn't use cached version
COPY app.py .
# Verify the correct version is copied (this will fail build if wrong version)
RUN python3 -c "import sys; content = open('/app/app.py').read(); assert 'VERSION: 2025-11-27-v2' in content or 'st.stop()' in content, 'Wrong app.py version!'; print('✓ Correct app.py version detected')"

# Healthcheck to verify the application is running
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Expose the port
EXPOSE 8501

# Entry point command to start the Streamlit application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]