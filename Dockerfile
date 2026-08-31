# ---- Stage 1: builder ----
FROM python:3.12-slim@sha256:2c941e860699f878900b0edc2403613c234d4b32eda3cc9fa7036991a2a63c4a AS builder

WORKDIR /app
COPY app/requirements.txt .
# Install dependencies into standard wheel cache directory
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---- Stage 2: target ----
FROM python:3.12-slim@sha256:2c941e860699f878900b0edc2403613c234d4b32eda3cc9fa7036991a2a63c4a AS target

ARG APP_VERSION=dev
ENV APP_VERSION=$APP_VERSION
ENV PATH=/usr/local/bin:$PATH
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/usr/local/lib/python3.12/site-packages

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /app

# Copy installed dependencies directly to system site-packages
COPY --from=builder /install /usr/local
COPY app/ .

# Ensure appuser owns application assets
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

# Production Gunicorn invocation with explicit worker timeout settings
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "2", "--timeout", "30", "app:app"]
