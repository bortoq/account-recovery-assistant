# Knowledge Base Operations

This document defines the minimum operating policy for the first incident-specific recovery knowledge base.

## Covered Incidents

The first product-ready incident set is:

- `gmail_mfa_loss`
- `apple_trusted_device_loss`
- `meta_account_hacked`
- `microsoft_admin_lockout`

Each incident must have:

- a normalized questionnaire;
- an incident-specific recovery record;
- one `default_guidance` block;
- one or more `decision_paths` blocks for answer-specific branches;
- official links;
- ownership evidence guidance;
- common mistakes;
- source notes;
- review metadata.

## Questionnaire Contract

Each question uses the same schema:

- `id`: stable question identifier
- `field`: output field name expected by the planner or future wizard
- `prompt`: user-facing question text
- `answer_type`: `boolean` or `single_choice`
- `required`: whether the wizard must collect an answer

The `role` question is the first gate for every incident and must remain explicit.

## Review Metadata Contract

Each incident record must carry:

- `last_verified_at`
- `review_due_at`
- `review_cadence_days`
- `confidence`
- `status`
- `stale`

Each guidance block may also carry:

- `next_best_action`
- `prepare_now`
- `what_can_make_this_worse`
- `escalate_when`
- `expected_timeline`
- optional `checklist_additions`
- optional `support_summary_addition`

## Status Meanings

- `verified`: the incident record was recently reviewed and can be used as the normal service-specific path.
- `needs_review`: the incident record still exists, but service-specific details should be treated cautiously until re-checked.
- `stale`: reserved for incidents that are materially outdated and should trigger stronger product warnings or temporary fallback behavior.
- `unverified`: planner fallback status when no incident-specific record exists.

## Manual Review Cadence

The current minimum cadence is 30 days for the first four incidents.

Reviewers should:

1. Re-open every official link.
2. Re-check that the recovery flow still matches the stored checklist.
3. Confirm evidence requirements and common mistakes still look accurate.
4. Update `last_verified_at`, `review_due_at`, `confidence`, `status`, and `stale`.
5. Update `source_notes` when the service changed behavior or expectations.

## Staleness Policy

The current CLI does not silently trust all incident records equally.

- `verified` records are shown normally.
- `needs_review` records stay usable, but the generated plan adds an explicit warning.
- `unverified` records fall back to generic playbook behavior.

The planner now also treats a past `review_due_at` date as authoritative evidence that the record needs review, even if the JSON file still says `verified`.

This is the minimum contract required before building a web wizard on top of the engine.
