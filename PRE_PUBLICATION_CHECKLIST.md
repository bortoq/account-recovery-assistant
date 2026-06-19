# Pre-Publication Checklist

Run this immediately before posting the project publicly, for example in Telegram, Hacker News, Reddit, or a GitHub release.

## 1. Fresh Checkout Smoke Test

```bash
git clone https://github.com/bortoq/account-recovery-assistant.git /tmp/ara-public-test
cd /tmp/ara-public-test
python -m pip install .
account-recovery-assistant --version
account-recovery-assistant examples/lost_mfa.json
```

## 2. Local Validation

```bash
PYTHONPATH=src python3 -m pytest -q
python3 scripts/check_data_source.py
python3 scripts/validate_data.py
python3 scripts/check_links.py
python3 -m build --no-isolation
```

Expected:

- tests pass;
- data validation passes;
- link check has zero hard failures;
- Instagram/X links may remain manual-review because of provider bot protection;
- build succeeds.

## 3. README Review

Check the first screen of README:

- says controlled alpha;
- explains official channels only;
- does not promise recovery;
- tells users not to enter passwords/codes;
- has a clear quickstart;
- links to feedback instructions.

## 4. Demo Asset

Before posting, prepare one visual:

- GIF from `docs/assets/demo.gif`; or
- screenshot of the web wizard plan screen; or
- terminal screenshot of Markdown output.

## 5. Telegram Post Checklist

The post should include:

- one-sentence problem;
- what the tool does;
- what it does not do;
- supported scenarios;
- GitHub link;
- request for specific feedback;
- warning not to send passwords/codes.

## 6. Feedback Capture

Make sure these exist:

- `FEEDBACK.md`;
- GitHub issue templates;
- `docs/alpha-tester-issue.md` pinned issue draft.

## 7. After Publishing

Track:

- replies/comments;
- GitHub stars;
- issues opened;
- scenario requests;
- people willing to do a 15-minute interview;
- whether anyone asks for hosted or human-assisted version.

Do not judge success by stars alone.
