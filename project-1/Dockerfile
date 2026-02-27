# ============================================
# IT Ticket Automation Bot — Dockerfile
# ============================================
# Base image: Python slim (small and lightweight)
FROM python:3.11-slim

# Metadata
LABEL maintainer="Jordan Cohen"
LABEL description="IT Ticket Automation Bot"

# Set working directory inside the container
WORKDIR /app

# Copy dependencies first (to leverage Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py .

# Expose port 5000 (documentation only, not functional)
EXPOSE 5000

# Default command when the container starts
CMD ["python", "app.py"]
