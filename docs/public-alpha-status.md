# Public Alpha Status

Current status: **controlled local alpha MVP**.

## Ready

- CLI and local web wizard.
- Packaged wheel with JSON knowledge base.
- Public alpha checklist.
- Security, privacy, disclaimer, and license docs.
- Data validation and link checking scripts.
- Microsoft consumer vs Microsoft 365 tenant branching.
- Consent-based memory-only feedback.
- Health endpoint.

## Known Limitations

- X/Twitter links require manual browser review because automated checks return bot-protection 403 responses.
- Hosted deployment controls are a skeleton, not production enforcement.
- Outcome and willingness-to-pay data are not validated yet.
- Browser E2E is currently lightweight/optional, not a full cross-browser matrix.

## Public Alpha Gate

Before announcing widely:

1. Run `PUBLIC_ALPHA_CHECKLIST.md`.
2. Run `python3 scripts/sync_packaged_data.py`.
3. Run `python3 scripts/validate_data.py`.
4. Run `python3 scripts/check_links.py`.
5. Build and test the wheel from a clean checkout.
6. Manually review X/Twitter links or keep them explicitly marked as manual review.
