# Deployment Skeleton

The project is currently designed for local controlled alpha use. This document describes a minimal hosted skeleton and the controls still required before public hosting.

## Local Container Build

```bash
docker build -t account-recovery-assistant:alpha .
docker run --rm -p 8000:8000 account-recovery-assistant:alpha
```

Open:

```text
http://127.0.0.1:8000
```

Health check:

```bash
curl http://127.0.0.1:8000/healthz
```

## Environment Variables

- `ARA_RATE_LIMIT_MAX_REQUESTS` — max POST requests per window per client. Default: `120`.
- `ARA_RATE_LIMIT_WINDOW_SECONDS` — rate-limit window. Default: `60`.
- `ARA_ACCESS_LOG=1` — enable basic server access logs. Request bodies are never logged by application code.

## Production Requirements Before Hosted Public MVP

- TLS termination.
- Reverse proxy or platform rate limiting in front of the app.
- No request body logging at proxy/platform layer.
- Monitoring for `/healthz`.
- Abuse contact route.
- Production privacy policy and terms.
- Data retention enforcement for any persisted feedback.
- Manual review process for stale provider links.

## Logging Boundary

The app does not log request bodies. If access logs are enabled, they are basic route/status logs only. Hosted infrastructure must also disable or redact request body logging.
