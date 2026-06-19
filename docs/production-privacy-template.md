# Production Privacy Policy Template

This template must be reviewed and adapted before any hosted public launch.

## Product Scope

Account Recovery Assistant provides guidance for official account recovery flows. It does not recover accounts automatically, bypass provider security, or guarantee account restoration.

## Data We Do Not Want

Users must not submit:

- passwords;
- backup codes;
- SMS codes;
- authenticator codes;
- identity document scans or numbers;
- payment card numbers;
- provider session tokens or cookies.

## Data Processed In Hosted Mode

A hosted deployment may process the answers needed to generate a recovery plan. The default production posture should be no persistent storage of recovery-plan request bodies.

## Feedback

Feedback must be opt-in. During alpha, feedback should be limited to:

- incident id;
- decision path id;
- outcome: recovered or stuck;
- link status: worked, failed, or not used;
- timestamp;
- consent flag.

No free-text personal details should be collected during alpha.

## Retention

If feedback is persisted, define a short retention period before launch. Example: delete alpha feedback after 30 days unless a user separately opts into research follow-up.

## Logging

Request bodies for plan generation, Markdown generation, and feedback endpoints must not be logged by the app, reverse proxy, or hosting platform.

## Deletion And Contact

Before public hosted launch, provide a contact path for privacy questions, abuse reports, and deletion requests.

## Provider Affiliation

The product is not affiliated with Google, Apple, Meta, Microsoft, X, LinkedIn, TikTok, Yahoo, Telegram, or other providers referenced in playbooks.
