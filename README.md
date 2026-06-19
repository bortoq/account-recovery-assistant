# Account Recovery Assistant

**Safe account recovery guidance through official channels — for rightful owners and authorized representatives.**

> **⚠️ Controlled alpha.** This tool helps you navigate official recovery flows. It does **not** automate account recovery, guarantee success, or bypass security.
>
> See [DISCLAIMER.md](DISCLAIMER.md), [PRIVACY.md](PRIVACY.md), and [LICENSE](LICENSE).

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

# Check official links in the knowledge base
python3 scripts/check_links.py
```

Project structure:

```
├── src/account_recovery_assistant/
│   ├── data/            # Packaged playbooks (also mirrored in data/)
│   ├── planner.py       # Core recovery plan engine
│   ├── validation.py    # Input validation (role, required fields, types)
│   ├── web.py           # Local web wizard server
│   ├── static/          # Frontend JS/CSS
│   └── __main__.py      # CLI entry point
├── data/                # Top-level playbook source of truth
├── examples/            # Sample situation JSON files
└── tests/               # pytest suite
```

---

## Roadmap & Docs

- [roadmap.md](roadmap.md) — full plan and status
- [docs/current-usage.md](docs/current-usage.md) — detailed usage
- [docs/releasing.md](docs/releasing.md) — build & publish guide
- [docs/hosted-operations.md](docs/hosted-operations.md) — hosted privacy, logging, retention, and abuse controls
- [CHANGELOG.md](CHANGELOG.md) — release history

---

<p align="center"><sub>Made for rightful owners, not for bypass.</sub></p>
