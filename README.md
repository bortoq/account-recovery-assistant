# Account Recovery Assistant

![Python](https://img.shields.io/badge/python-3.11%2B-3776AB)
![Status](https://img.shields.io/badge/status-alpha-bb6c2f)
![Surface](https://img.shields.io/badge/interface-CLI%20%2B%20Web-165d52)
[![PyPI version](https://img.shields.io/pypi/v/account-recovery-assistant.svg)](https://pypi.org/project/account-recovery-assistant/)

Account Recovery Assistant is a safe guide for people who lost access to an account, got stuck in multi-factor authentication, forgot recovery details, or need help using official recovery channels.

## Simple Description

This is an account recovery helper. It does not hack accounts or bypass security. It helps the rightful owner understand what happened, collect proof, choose the right official process, and avoid mistakes that make recovery harder.

## Full Description

People lose access to email, social media, banking, work, gaming, domain, and cloud accounts. Common causes include forgotten passwords, lost phones, broken authenticator apps, changed phone numbers, missing backup codes, suspicious activity locks, old recovery emails, and business admin turnover.

Official recovery flows are often confusing. Users do not know what information is required, why forms are rejected, or which actions look suspicious. Account Recovery Assistant turns recovery into a guided process: identify the account and failure type, collect ownership evidence, find the official recovery channel, prepare support messages, track attempts, and harden the account after access is restored.

## Safety Principle

The product must only help the rightful owner or an authorized representative. It must not provide instructions for bypassing MFA, phishing, social engineering, password cracking, device hacking, or session theft. All guidance must use official service procedures.

## Main Use Cases

- A user lost a phone with an authenticator app.
- A user changed phone numbers and cannot receive SMS codes.
- A user forgot a password and lost access to the recovery email.
- An account is locked after suspicious activity.
- A family member needs to recover an account through official estate procedures.
- A small business lost access to an ad, domain, or cloud account.

## MVP

- Diagnostic questionnaire
- Step-by-step recovery checklist
- Database of official recovery links for popular services
- Support message generator
- List of documents and proof to prepare
- Post-recovery security checklist: backup codes, passkeys, recovery contacts, and password manager setup

## Current Prototype

The first prototype is a small Python CLI and core library. It reads a JSON situation file and prints a safe recovery plan as JSON.

The project now also includes a local web wizard on top of the same engine for the first four canonical incidents.

Run an example:

```bash
PYTHONPATH=src python3 -m account_recovery_assistant examples/lost_mfa.json
```

Print a readable Markdown report:

```bash
PYTHONPATH=src python3 -m account_recovery_assistant --format markdown examples/lost_mfa.json
```

Run tests:

```bash
PYTHONPATH=src python3 -m pytest -v
```

Build a package locally:

```bash
python3 -m build
```

Start the local web wizard:

```bash
PYTHONPATH=src python3 -m account_recovery_assistant --serve-web
```

Or directly:

```bash
PYTHONPATH=src python3 -m account_recovery_assistant.web
```

Supported MVP scenarios:

- lost MFA device;
- changed phone number;
- suspicious activity lock.

Example inputs included in the repository:

- `examples/lost_mfa.json`
- `examples/changed_phone.json`
- `examples/suspicious_lock.json`
- `examples/google_identity_review.json`
- `examples/apple_wait_period.json`
- `examples/meta_business_takeover.json`
- `examples/meta_identity_review.json`
- `examples/microsoft_backup_admin.json`
- `examples/microsoft_domain_support.json`

The planner also uses `data/service_priorities.json` for aliases and official links for the first top-priority services, including Google/Gmail, Apple/iCloud, Facebook, Instagram, Microsoft/Outlook, X/Twitter, TikTok, Yahoo Mail, LinkedIn, and Telegram.

The project now also exposes a normalized incident questionnaire layer for the first high-value web-wizard cases: Gmail MFA loss, Apple trusted-device loss, Meta account hacked, and Microsoft admin lockout.

Each of those first incidents now uses a shared questionnaire contract with stable `id`, `field`, `answer_type`, and `required` keys so the same flow can drive the CLI today and a future web wizard later.

The recovery knowledge base now carries incident-specific metadata for those first web-wizard cases: ownership evidence, common mistakes to avoid, source notes, verification date, review due date, review cadence, confidence level, and explicit review status.

The Phase 2 and Phase 3 foundation is now product-oriented rather than purely exploratory:

- the first four incidents are canonical and exposed through a normalized questionnaire contract;
- incident-specific plans include questionnaire metadata, so a wizard can render the same entry flow and plan output consistently;
- knowledge-base entries now declare `verified`, `needs_review`, or fallback `unverified` status, with explicit 30-day review cadence metadata.

Phase 4 is now started as a local web product surface:

- a mobile-friendly incident picker;
- a browser questionnaire flow for the first four canonical incidents;
- a plan screen that surfaces checklist, evidence, official links, support message, hardening steps, and knowledge freshness warnings.

The current MVP now also produces first-approximation recovery guidance instead of only generic checklists:

- a `next_best_action` for the chosen incident and answer path;
- a `decision_path_id` that shows which incident branch was selected;
- a `prepare_now` list focused on evidence and context to gather before retrying;
- a `what_can_make_this_worse` list to reduce lockout and support-review mistakes;
- an `escalate_when` list for cases where official recovery is stalling;
- an `expected_timeline` estimate based on whether trusted factors still exist.

That guidance is now driven by incident-specific `decision_paths` in `data/recovery_playbooks.json`, so the first four incidents can be deepened by updating the knowledge base instead of hardcoding every branch in Python.

The current recovery engine already distinguishes several materially different first-pass branches inside the same incident, such as backup-code recovery vs. identity-review recovery for Google, or backup-admin recovery vs. tenant-support recovery for Microsoft.

## Similar Projects And Difference

- Passware, Lazesoft, Ophcrack, and John the Ripper recover or crack passwords for files, devices, and local systems. Account Recovery Assistant is different: it does not crack passwords. It guides users through official account recovery.
- Password managers help prevent future loss, but they do not solve the full recovery situation once MFA, phone access, or support workflows fail.
- Official help centers from Google, Apple, Meta, Microsoft, banks, and SaaS products contain the correct procedures, but they are scattered and hard to navigate.
- IT support and managed service providers can help businesses manually. This project turns that help into a guided workflow with evidence collection and message templates.
- Shady “account recovery” services and hacking offers are the opposite of this project. Account Recovery Assistant must stay legal, safe, and owner-only.

The main difference is safe navigation: understand the situation, collect proof, use official channels, and protect the account after recovery.

## Value

- Less panic and confusion
- Fewer mistakes that make recovery harder
- Faster evidence collection
- Clear navigation through official procedures
- Better prevention after recovery

## Risks

- The product must clearly separate owner recovery from attacker guidance.
- Recovery procedures change often and the knowledge base must stay current.
- It cannot promise guaranteed recovery.
- Financial, corporate, and estate cases may need legal or administrative procedures.

## Monetization

- Free basic diagnosis
- Paid detailed recovery plans
- Small business subscription for account inventory and recovery planning
- Partnerships with IT support, legal services, and managed service providers

## Documents

See [docs/current-usage.md](docs/current-usage.md) for the current MVP workflow and user value.

See [docs/service-priorities.md](docs/service-priorities.md) for the first knowledge-base expansion plan.

See [docs/knowledge-base-operations.md](docs/knowledge-base-operations.md) for the incident review policy and freshness contract.

See [docs/releasing.md](docs/releasing.md) for package and release steps.

See [roadmap.md](roadmap.md).
