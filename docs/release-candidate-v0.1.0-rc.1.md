# Release Candidate v0.1.0-rc.1

Date: 2026-06-19

## Checklist Run

The controlled public alpha checklist was run against the current workspace state.

## Results

- Tests: `PYTHONPATH=src python3 -m pytest -q` — pass locally, with optional Playwright skipped when not installed.
- Data source check: `python3 scripts/sync_packaged_data.py` — pass.
- Data validation: `python3 scripts/validate_data.py` — pass.
- Link check: `python3 scripts/check_links.py` — 0 hard failures, 2 manual-review X/Twitter URLs.
- Build: `python3 -m build --no-isolation` — pass.
- Installed console script real example — pass.
- Dockerfile present and included in CI. Local sandbox may not have Docker available.

## Known Limitations

- X/Twitter links still require manual browser review because automated checks return 403 bot-protection responses.
- Hosted deployment remains a skeleton until reverse proxy, monitoring, production privacy/terms, and abuse contact are configured.
- Playwright browser E2E is configured in CI, but local environments without Playwright will skip the optional browser-binary test.

## Suggested Tag

```bash
git tag -a v0.1.0-rc.1 -m "v0.1.0 release candidate 1"
```

Do not publish as production. This is a controlled alpha release candidate.
