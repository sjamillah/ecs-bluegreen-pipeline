# ---- Stage 1: builder ----
FROM python:3.12-slim@sha256:2c941e860699f878900b0edc2403613c234d4b32eda3cc9fa7036991a2a63c4a AS builder
WORKDIR /app
COPY app/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ---- Stage 2: target ----
FROM python:3.12-slim@sha256:2c941e860699f878900b0edc2403613c234d4b32eda3cc9fa7036991a2a63c4a AS target

# Accept APP_VERSION from GitHub Actions build-args
ARG APP_VERSION=dev
ENV APP_VERSION=$APP_VERSION
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /app

COPY --from=builder /root/.local /home/appuser/.local
COPY app/ .

RUN chown -R appuser:appuser /app /home/appuser/.local
USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

# Updated entrypoint to point to app:app instead of main:app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]
