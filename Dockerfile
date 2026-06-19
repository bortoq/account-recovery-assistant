FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ARA_RATE_LIMIT_MAX_REQUESTS=120 \
    ARA_RATE_LIMIT_WINDOW_SECONDS=60

WORKDIR /app

COPY . /app
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python scripts/sync_packaged_data.py && \
    python scripts/validate_data.py && \
    python -m pip install --no-cache-dir .

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz', timeout=3).read()"

CMD ["account-recovery-assistant", "--serve-web", "--host", "0.0.0.0", "--port", "8000"]
