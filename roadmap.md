# Roadmap

## Phase 1: Safety Policy And Product Boundary

- Define allowed scenarios: owner, estate representative, business admin, or authorized helper.
- Ban bypass, hacking, phishing, social engineering, and unauthorized access guidance.
- Add clear warnings that recovery must use official channels.
- Define escalation paths for financial, business, and estate cases.
- Define the value promise as guidance, evidence preparation, and safer recovery workflow, not guaranteed account restoration.
- Keep the CLI as a core engine, not the final end-user product.

## Phase 2: Narrow Incident Scope

- Start with 3-5 high-value incidents instead of broad top-10 service coverage.
- Prioritize incidents such as Gmail MFA loss, Apple ID trusted-device recovery, Facebook/Instagram hacked account, and Microsoft business admin lockout.
- Define ownership evidence for each incident type.
- Define common user mistakes for each incident type.
- Build a focused diagnostic questionnaire for those incidents first.

## Phase 3: Knowledge Base Operations

- Collect official recovery links and help-center anchors for the first narrow incident set.
- Store `last_verified_at`, confidence level, and source notes for each procedure.
- Structure requirements: documents, backup codes, device history, billing data, domain ownership, and identity checks.
- Add stale-content flags and a manual review cadence.
- Treat the freshness of the knowledge base as a product requirement, not background maintenance.

## Phase 4: Web Wizard First

- Build a mobile-friendly web wizard on top of the existing engine.
- Let users pick a real-world incident from a simple entry screen.
- Generate action checklists.
- Generate support message templates.
- Provide a post-recovery hardening checklist.
- Keep CLI support for internal testing, demos, and automation.

## Phase 5: Incident Pages And Discovery

- Create landing pages around real search queries such as lost authenticator, changed phone number, hacked Instagram, and locked Microsoft account.
- Position the product around incidents and outcomes, not around the word "assistant".
- Test which incident pages convert the best.
- Track whether users want self-serve guidance, paid help, or business readiness.

## Phase 6: B2B Disaster Cases

- Add business-specific incidents: departed admin, lost recovery email, locked workspace account, and account takeover response.
- Package recovery readiness as disaster-response planning, not generic inventory management.
- Validate with small businesses, MSPs, and IT support shops.

## Phase 7: Validation And Moat

- Test on safe simulated recovery scenarios.
- Interview users who actually lost account access.
- Check legal limits by country and account type.
- Evaluate B2B demand from small businesses and IT support teams.
- Define moat explicitly around freshness, incident-specific UX, and specialized recovery workflows rather than code alone.
