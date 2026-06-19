# Hosted Operations Policy Draft

This project is currently a local controlled alpha. A hosted version should not be launched until the items below are implemented and reviewed.

## Data Retention

- Default posture: do not store recovery situations, passwords, backup codes, SMS codes, authenticator codes, identity scans, or payment card data.
- If outcome feedback is collected, store only minimal fields: incident id, decision path id, outcome, link status, timestamp, and explicit consent flag.
- Set a short retention period for feedback, for example 30 days for alpha validation, unless a user explicitly opts into longer research follow-up.
- Provide a deletion contact or self-service deletion mechanism before public rollout.

## Logging

- Do not log request bodies for `/api/plan`, `/api/plan/markdown`, or feedback endpoints.
- Log only operational metadata needed for reliability: status code, route, coarse timestamp, and anonymous request id.
- Redact query strings and headers that may contain sensitive values.
- Disable verbose debug logs in production.

## Privacy & Consent

- Show a clear hosted privacy notice before collecting any feedback.
- Feedback must be opt-in and should not include free-text personal details during the alpha phase.
- Never ask users to enter passwords, backup codes, SMS codes, authenticator codes, identity document numbers, or payment card numbers.
- Clearly state that the product is not affiliated with Google, Apple, Meta, Microsoft, X, LinkedIn, TikTok, Yahoo, Telegram, or other providers.

## Abuse Controls

- Rate-limit plan generation and feedback endpoints.
- Block or refuse unauthorized intent and bypass language before generating a plan.
- Monitor aggregate abuse signals without storing sensitive account details.
- Provide a contact path for abuse reports.

## Deployment Gate

Before a hosted public MVP, add:

- production privacy policy and terms;
- data processing inventory;
- rate limiting;
- structured redaction tests;
- backup/restore plan for non-sensitive operational data;
- security review for headers, TLS, dependency updates, and logging configuration.
