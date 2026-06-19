# Monitoring Skeleton

This is a minimal monitoring plan for a hosted alpha. It is not a full production observability stack.

## Health Check

Monitor:

```text
GET /healthz
```

Expected response:

```json
{
  "status": "ok",
  "incidents": 4,
  "feedback_events": 0,
  "rate_limit_max_requests": 120
}
```

## Alerts

Create alerts for:

- `/healthz` non-200 for more than 2 minutes;
- elevated 429 rate-limit responses;
- elevated 4xx validation errors that may indicate abuse or UI regressions;
- elevated 5xx responses;
- link-check workflow hard failures.

## Logging Boundary

Do not log request bodies. Operational logs may include:

- route;
- status code;
- coarse timestamp;
- anonymous request id;
- latency.

Do not log:

- passwords;
- backup codes;
- SMS/authenticator codes;
- identity document numbers;
- payment card details;
- full recovery narratives.

## Manual Review

Review provider links on a schedule and update knowledge-base metadata when manual checks are complete.
