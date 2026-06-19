# Public Alpha Checklist

Use this checklist before tagging or announcing a controlled public alpha.

## Product Boundary

- [ ] README says controlled alpha and no guaranteed recovery.
- [ ] DISCLAIMER, PRIVACY, LICENSE, and SECURITY docs are present.
- [ ] Supported incidents are listed clearly.
- [ ] Known limitations are documented.

## Safety

- [ ] Unauthorized roles are refused.
- [ ] Bypass, phishing, hacking, and social-engineering intents are refused.
- [ ] UI warns users not to enter passwords, backup codes, SMS codes, authenticator codes, identity document numbers, or payment cards.
- [ ] Feedback collection is opt-in and does not accept free-text personal details.

## Technical Release

- [ ] `PYTHONPATH=src python3 -m pytest -q` passes.
- [ ] `python3 scripts/check_data_source.py` confirms no duplicate packaged JSON is tracked.
- [ ] `python3 scripts/validate_data.py` passes.
- [ ] `python3 scripts/check_links.py` has zero hard failures.
- [ ] `python3 -m build --no-isolation` succeeds.
- [ ] Installed wheel can generate a plan from a real example.
- [ ] All `examples/*.json` work through the CLI.

## Knowledge Base

- [ ] `data/` is the only tracked JSON source of truth; build artifacts receive package data via `setup.py`.
- [ ] All canonical incident ids exist in both questionnaire and playbook data.
- [ ] Manual-review links have review notes.
- [ ] Instagram and X/Twitter links are manually checked in a browser or left explicitly marked as manual review.

## Hosted Gate

Do not launch a hosted version until `docs/hosted-operations.md` requirements are implemented, especially rate limiting, body logging prevention, retention enforcement, and abuse reporting.
