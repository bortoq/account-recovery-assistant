# Current Usage

This document explains how to use the current MVP of `account-recovery-assistant` and what value it already provides.

## What The Project Is Right Now

The current implementation is a Python CLI tool plus a small core library.

It does not recover accounts automatically. It does not bypass security. It turns a confusing recovery situation into a structured recovery plan that uses official channels only.

It now also exposes the minimum product contract needed before a web wizard:

- a canonical first incident set;
- a normalized questionnaire schema for those incidents;
- explicit knowledge-base review status and review cadence metadata.

## How To Use It

1. Prepare a JSON file that describes the recovery situation.
2. Run the CLI with that file.
3. Read the generated plan in JSON or Markdown form.

Or use the local web wizard:

1. Start `PYTHONPATH=src python3 -m account_recovery_assistant --serve-web`
2. Open the local URL in a browser.
3. Pick one of the four canonical incidents.
4. Answer the questionnaire.
5. Review the generated recovery plan and warnings.

Examples are already included:

- `examples/lost_mfa.json`
- `examples/changed_phone.json`
- `examples/suspicious_lock.json`
- `examples/google_identity_review.json`
- `examples/apple_wait_period.json`
- `examples/meta_business_takeover.json`
- `examples/meta_identity_review.json`
- `examples/microsoft_backup_admin.json`
- `examples/microsoft_domain_support.json`

Run JSON output:

```bash
PYTHONPATH=src python3 -m account_recovery_assistant examples/lost_mfa.json
```

Run Markdown output:

```bash
PYTHONPATH=src python3 -m account_recovery_assistant --format markdown examples/lost_mfa.json
```

## What The User Gets

- A structured recovery plan
- A next best action for the exact incident path
- A step-by-step checklist
- A focused prepare-now list
- A list of actions that can make recovery worse
- Escalation triggers for stuck recovery cases
- A rough expected timeline
- Evidence and documents to prepare
- Official recovery links
- Knowledge freshness metadata
- Common mistakes to avoid
- Source notes for the recovery path
- A support message template
- Post-recovery hardening steps
- Safety warnings

## Where It Already Helps

The current value is not automation. The current value is structure and safety.

It helps users:

- diagnose what was actually lost;
- decide what to do first instead of trying random recovery actions;
- avoid random or repeated actions that make recovery harder;
- collect stronger ownership evidence;
- use official channels instead of unsafe shortcuts;
- write support messages that do not look suspicious;
- see whether the current playbook was recently verified or may need review;
- reduce the chance of losing the account again after recovery.

## Real MVP Scenarios

- Lost phone with authenticator app
- Changed phone number
- Suspicious activity lock
- Business account recovery planning
- Estate or family recovery planning through official procedures

## Incident Contract Ready For A Wizard

The first four high-value incidents are now treated as canonical product entries:

- `gmail_mfa_loss`
- `apple_trusted_device_loss`
- `meta_account_hacked`
- `microsoft_admin_lockout`

Each incident now has:

- a stable incident id;
- a normalized questionnaire with `id`, `field`, `answer_type`, and `required`;
- incident-specific `decision_paths` for the first recovery branches;
- multiple answer-driven branches for the same incident where the recovery path materially changes;
- incident-specific checklist, evidence, links, mistakes, and source notes;
- knowledge freshness metadata with `last_verified_at`, `review_due_at`, `review_cadence_days`, `confidence`, `status`, and `stale`.

## What Is Not Built Yet

- Interactive CLI wizard
- Automatic form filling
- Email or Telegram integrations
- Service-specific deep recovery flows for all top-priority accounts

## Near-Term Product Improvements

The most valuable next improvements are:

- mobile-friendly web wizard on top of the current engine;
- richer incident-specific playbooks for Google, Apple, Meta, and Microsoft beyond the first canonical four;
- stronger knowledge-base review tooling and workflows on top of the new freshness contract;
- incident landing pages for real recovery search queries;
- stronger business disaster cases such as lost admin access and account takeover response.
