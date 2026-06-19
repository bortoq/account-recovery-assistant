# Account Recovery Assistant

[![CI](https://github.com/bortoq/account-recovery-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/bortoq/account-recovery-assistant/actions/workflows/ci.yml)
[![Link Check](https://github.com/bortoq/account-recovery-assistant/actions/workflows/link-check.yml/badge.svg)](https://github.com/bortoq/account-recovery-assistant/actions/workflows/link-check.yml)
![Status](https://img.shields.io/badge/status-controlled%20alpha-bb6c2f)

**Safe account recovery guidance through official channels — for rightful owners and authorized representatives.**

Lost access to an important account? This local CLI/web wizard helps you choose the safest official recovery path, prepare ownership evidence, avoid common lockout mistakes, and generate a clear support message.

> **⚠️ Controlled alpha.** This tool helps you navigate official recovery flows. It does **not** automate account recovery, guarantee success, or bypass security.
>
> See [DISCLAIMER.md](DISCLAIMER.md), [PRIVACY.md](PRIVACY.md), [FEEDBACK.md](FEEDBACK.md), and [LICENSE](LICENSE).

**Try it in 60 seconds:**

```bash
python -m pip install .
account-recovery-assistant examples/lost_mfa.json
```

**Looking for alpha feedback:** if you test a real or simulated recovery scenario, please share what was clear, confusing, missing, or stale. See [FEEDBACK.md](FEEDBACK.md).

---

## What It Is

A local CLI and web wizard that turns a confusing account recovery situation into a structured, safe recovery plan. It asks what happened, what you still control, and your relationship to the account — then produces a checklist, evidence list, official links, and step-by-step guidance using **only official service procedures**.

## What It Is Not

🚫 Not a hacking tool, password cracker, or bypass.
🚫 Not affiliated with Google, Apple, Meta, Microsoft, LinkedIn, or any other service.
🚫 Not legal advice or identity verification authority.

---

## Quickstart

```bash
git clone https://github.com/bortoq/account-recovery-assistant.git
cd account-recovery-assistant
python -m pip install .
```

### CLI

```bash
# Generate a plan from an example situation
account-recovery-assistant examples/lost_mfa.json

# Or with PYTHONPATH from source
PYTHONPATH=src python3 -m account_recovery_assistant examples/lost_mfa.json

# Markdown report
account-recovery-assistant --format markdown examples/lost_mfa.json

# Version
account-recovery-assistant --version
```

### Web Wizard

```bash
PYTHONPATH=src python3 -m account_recovery_assistant --serve-web
# Open http://127.0.0.1:8000
```


### Library Usage

If you call the Python library directly, validate user input before generating a plan:

```python
from account_recovery_assistant import generate_recovery_plan
from account_recovery_assistant.validation import validate_situation

situation = validate_situation({
    "service": "Google",
    "lost_factor": "authenticator_app",
    "role": "owner",
})
plan = generate_recovery_plan(situation)
```

---

## Supported Incidents (MVP)

| Service | Incident | Example file |
|---------|----------|-------------|
| Google | Lost MFA device (authenticator app) | `examples/lost_mfa.json` |
| Apple | Lost trusted device or trusted phone | `examples/apple_wait_period.json` |
| Meta (FB/IG) | Account hacked | `examples/meta_business_takeover.json` |
| Microsoft | Admin or workspace lockout | `examples/microsoft_backup_admin.json` |

Each generates a plan with: checklist, evidence, official links, support message template, hardening steps, decision path, timeline, and knowledge freshness status.

---

## Safety & Privacy

- **All processing is local.** No data is sent to any server.
- **Never enter** passwords, backup codes, SMS codes, authenticator codes, passport scans, or payment card numbers into the tool.
- The tool is for **guidance and evidence preparation** only.
- Plans include safety warnings against unauthorized access, bypass attempts, and unofficial recovery services.
- Claims of unauthorized intent ("hack", "phish", "someone else's account") are **refused by design** with no plan generated.

---

## Development

```bash
# Install in editable mode
pip install -e .

# Run tests
PYTHONPATH=src python3 -m pytest -v

# Build package
python3 -m build --no-isolation

# Verify data/ is the single source of truth before build
python3 scripts/check_data_source.py

# Validate knowledge-base structure and packaged-data sync
python3 scripts/validate_data.py

# Check official links in the knowledge base
python3 scripts/check_links.py
```

Project structure:

```
├── src/account_recovery_assistant/
│   ├── data/            # Package data namespace; JSON copied during build
│   ├── planner.py       # Core recovery plan engine
│   ├── validation.py    # Input validation (role, required fields, types)
│   ├── web.py           # Local web wizard server
│   ├── static/          # Frontend JS/CSS
│   └── __main__.py      # CLI entry point
├── data/                # Playbook source of truth
├── examples/            # Sample situation JSON files
└── tests/               # pytest suite
```

---

## Roadmap & Docs

- [roadmap.md](roadmap.md) — full plan and status
- [docs/current-usage.md](docs/current-usage.md) — detailed usage
- [FEEDBACK.md](FEEDBACK.md) — how to share useful alpha feedback safely
- [docs/demo-script.md](docs/demo-script.md) — short demo flow
- [docs/interview-script.md](docs/interview-script.md) — user discovery and validation questions
- [docs/landing-pages.md](docs/landing-pages.md) — landing-page validation drafts
- [docs/releasing.md](docs/releasing.md) — build & publish guide
- [docs/public-alpha-status.md](docs/public-alpha-status.md) — current public alpha readiness status
- [docs/deployment.md](docs/deployment.md) — local container and hosted deployment skeleton
- [docs/monitoring.md](docs/monitoring.md) — hosted monitoring skeleton
- [docs/production-privacy-template.md](docs/production-privacy-template.md) — hosted privacy template
- [docs/hosted-operations.md](docs/hosted-operations.md) — hosted privacy, logging, retention, and abuse controls
- [SECURITY.md](SECURITY.md) — vulnerability and safety reporting
- [THREAT_MODEL.md](THREAT_MODEL.md) — abuse and privacy threat model
- [PUBLIC_ALPHA_CHECKLIST.md](PUBLIC_ALPHA_CHECKLIST.md) — public alpha release gate
- [PRE_PUBLICATION_CHECKLIST.md](PRE_PUBLICATION_CHECKLIST.md) — final checklist before posting publicly
- [docs/alpha-tester-issue.md](docs/alpha-tester-issue.md) — pinned alpha tester issue draft
- [CHANGELOG.md](CHANGELOG.md) — release history

---

<p align="center"><sub>Made for rightful owners, not for bypass.</sub></p>
