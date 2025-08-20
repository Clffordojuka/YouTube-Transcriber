# Use a lightweight Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if needed for FAISS, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the project
COPY . .

# Expose Streamlit default port
EXPOSE 8501

# Set environment variable so Streamlit doesn’t ask for email etc.
ENV STREAMLIT_DISABLE_WATCHDOG_WARNING=1 \
    PYTHONUNBUFFERED=1

# Run Streamlit app
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]