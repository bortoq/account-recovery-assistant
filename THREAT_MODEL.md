# Threat Model

## Scope

Account Recovery Assistant is a local controlled-alpha tool that generates safe account recovery plans through official provider channels. It must not become an account takeover, bypass, or social-engineering tool.

## Assets To Protect

- User recovery context.
- Ownership evidence descriptions.
- Generated plans and support messages.
- Feedback outcome metadata.
- Knowledge-base integrity.
- Provider official-link accuracy.

## Non-Goals

The product must not collect or process:

- passwords;
- backup codes;
- SMS or authenticator codes;
- identity document scans or numbers;
- payment card numbers;
- provider session tokens or cookies.

## Trust Boundaries

1. User input to CLI/web API.
2. Local web UI to local HTTP server.
3. Knowledge-base JSON loaded from package data or source tree.
4. Optional memory-only feedback endpoint.
5. External official links opened in the user's browser.

## Abuse Cases

- A user asks to recover someone else's account.
- A user asks to bypass MFA or provider review.
- A user tries to phish or socially engineer support.
- A user submits dangerous intent in English, Russian, Hebrew, or mixed phrasing.
- A user attempts high-volume automated plan generation.
- A hosted deployment accidentally logs sensitive request bodies.

## Existing Controls

- Role validation and fail-closed refusal for missing/unsupported roles.
- Unsafe intent phrase detection across English, Russian, and Hebrew examples.
- No procedural plan for unauthorized or bypass requests.
- UI warnings not to enter passwords, codes, identity documents, or payment card data.
- Consent-required feedback with no free-text field.
- Memory-only feedback capped by `FEEDBACK_MAX_EVENTS`.
- App-level rate limiting for POST endpoints.
- No request body logging in application code.
- Official links stored in data and checked by `scripts/check_links.py`.
- Manual-review status for X/Twitter links that trigger bot protection.

## Residual Risks

- Rule-based intent detection can miss novel abuse phrasing.
- In-memory rate limiting is not shared across multiple processes or hosts.
- Hosted reverse proxies could log request bodies if misconfigured.
- Official provider flows can change without notice.
- Users can ignore warnings and enter sensitive information anyway.

## Required Hosted Controls

Before public hosted launch:

- edge rate limiting through reverse proxy/platform controls;
- request body logging disabled at every layer;
- monitoring of `/healthz`;
- abuse reporting contact;
- production privacy policy and terms;
- manual knowledge-base review process;
- no persistent feedback storage unless retention/deletion are implemented.
