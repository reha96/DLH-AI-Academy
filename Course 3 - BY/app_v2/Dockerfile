# Dockerfile for BeatRec - Optimized for Hugging Face Spaces
# Also works on Fly.io, Railway, and other container platforms

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
# Only copy necessary files to reduce image size
COPY *.py ./
COPY templates/ ./templates/
COPY static/ ./static/
COPY data/ ./data/ 2>/dev/null || true
COPY embeddings/ ./embeddings/ 2>/dev/null || true

# Create non-root user for security
RUN useradd -m -u 1000 beatrec && chown -R beatrec:beatrec /app
USER beatrec

# Expose port (7860 for Hugging Face Spaces, or use PORT env var)
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:7860/api/genres')" || exit 1

# Run with gunicorn (1 worker for memory efficiency)
# For Hugging Face Spaces, use 7860
# For other platforms, use $PORT environment variable
CMD ["sh", "-c", "gunicorn main:app --bind 0.0.0.0:${PORT:-7860} --workers 1 --threads 2 --timeout 120"]
