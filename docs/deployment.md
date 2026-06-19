# Deployment Skeleton

The project is currently designed for local controlled alpha use. This document describes a minimal hosted skeleton and the controls still required before public hosting.

## Local Container Build

```bash
docker build -t account-recovery-assistant:alpha .
docker run --rm -p 8000:8000 account-recovery-assistant:alpha
```

The Docker image runs as a non-root `app` user.

Open:

```text
http://127.0.0.1:8000
```

Health check:

```bash
curl http://127.0.0.1:8000/healthz
```

## Environment Variables

- `ARA_RATE_LIMIT_MAX_REQUESTS` — app-level POST request limit per window per client. Default: `120`.
- `ARA_RATE_LIMIT_WINDOW_SECONDS` — app-level rate-limit window. Default: `60`.
- `ARA_ACCESS_LOG=1` — enable basic server access logs. Request bodies are never logged by application code.

## Reverse Proxy Profile

Use a reverse proxy for TLS, request size limits, and production-grade edge rate limiting. See:

```text
deploy/nginx.conf
```

The example config sets:

- small request body limit;
- edge rate limiting;
- `/healthz` proxying;
- no application request body logging.

## Persisted-Free Feedback Policy

The current app stores feedback in memory only and caps it with `FEEDBACK_MAX_EVENTS`. It is lost on restart and is intended only for local alpha validation.

Before persisting feedback in a hosted deployment, implement:

- explicit hosted privacy policy;
- retention period;
- deletion path;
- storage encryption;
- no free-text personal details;
- monitoring that request bodies are not logged.

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
