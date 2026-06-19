# Account Recovery Assistant Web Wizard Design

## Goal

Build a mobile-friendly local web wizard on top of the existing planner so a user can choose a supported incident, answer a normalized questionnaire, and receive the same safe recovery plan that the CLI already generates.

## Scope

The first web release supports only the four canonical incidents:

- `gmail_mfa_loss`
- `apple_trusted_device_loss`
- `meta_account_hacked`
- `microsoft_admin_lockout`

The wizard must:

- show an incident picker;
- fetch the questionnaire for the chosen incident;
- collect answers in the browser;
- submit answers to the existing planner;
- render checklist, evidence, links, support message, hardening steps, and knowledge freshness warnings.

## Non-Goals

- No production hosting or deployment pipeline.
- No database, accounts, or persistent sessions.
- No knowledge-base editing UI.
- No analytics or landing pages.
- No additional incidents beyond the first canonical four.

## Architecture

The web wizard is a thin layer over the current Python package. A standard-library HTTP server serves one HTML page plus static CSS and JS, and exposes a small JSON API. The planner and knowledge-base files remain the source of truth for incidents, questionnaires, and recovery plans.

## API

The first version exposes:

- `GET /` for the web UI
- `GET /static/app.css`
- `GET /static/app.js`
- `GET /api/incidents`
- `GET /api/incidents/<incident_id>/questionnaire`
- `POST /api/plan`

`POST /api/plan` accepts a JSON object with:

- `incident_id`
- `service`
- questionnaire-derived fields such as `role`, `has_backup_codes`, `still_controls_email`

The server maps that payload directly into `generate_recovery_plan`.

## UI Flow

1. Load the single-page app.
2. Fetch incidents and show a short incident picker.
3. After selection, fetch the questionnaire and render one question block per entry.
4. Require answers before submit.
5. Submit the payload to `/api/plan`.
6. Render the plan with a prominent warning banner when `knowledge_base.status != "verified"`.

## UX Constraints

- Mobile-first layout.
- Plain, readable typography and clear grouping.
- No fake chat UI.
- No hidden steps: the user should always know whether they are choosing an incident, answering questions, or reviewing a plan.

## Safety Rules

The web layer must preserve the existing safety boundary:

- unauthorized or unsafe intent still returns refusal output;
- the UI must display safety refusals clearly instead of trying to keep the user in the wizard flow;
- stale or needs-review knowledge-base entries must surface warnings above the recovery checklist.

## Testing

Add tests for:

- API incident listing;
- questionnaire endpoint;
- plan generation endpoint;
- static page serving;
- planner warning propagation into the HTTP response contract.
