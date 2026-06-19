# Current Usage

This document explains how to use the current MVP of `account-recovery-assistant` and what value it already provides.

## What The Project Is Right Now

The current implementation is a Python CLI tool plus a small core library.

It does not recover accounts automatically. It does not bypass security. It turns a confusing recovery situation into a structured recovery plan that uses official channels only.

## How To Use It

1. Prepare a JSON file that describes the recovery situation.
2. Run the CLI with that file.
3. Read the generated plan in JSON or Markdown form.

Examples are already included:

- `examples/lost_mfa.json`
- `examples/changed_phone.json`
- `examples/suspicious_lock.json`

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
- A step-by-step checklist
- Evidence and documents to prepare
- Official recovery links
- A support message template
- Post-recovery hardening steps
- Safety warnings

## Where It Already Helps

The current value is not automation. The current value is structure and safety.

It helps users:

- diagnose what was actually lost;
- avoid random or repeated actions that make recovery harder;
- collect stronger ownership evidence;
- use official channels instead of unsafe shortcuts;
- write support messages that do not look suspicious;
- reduce the chance of losing the account again after recovery.

## Real MVP Scenarios

- Lost phone with authenticator app
- Changed phone number
- Suspicious activity lock
- Business account recovery planning
- Estate or family recovery planning through official procedures

## What Is Not Built Yet

- Interactive CLI wizard
- Web interface
- Automatic form filling
- Email or Telegram integrations
- Service-specific deep recovery flows for all top-priority accounts

## Near-Term Product Improvements

The most valuable next improvements are:

- interactive questionnaire flow;
- richer service-specific playbooks for Google, Apple, Meta, and Microsoft;
- more readable report outputs;
- broader top-priority account coverage;
- better support for business and estate recovery cases.
