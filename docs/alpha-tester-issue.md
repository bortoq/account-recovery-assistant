# Pinned Issue Draft: Looking For Alpha Testers

Use this as a pinned GitHub issue or discussion.

---

# Looking for alpha testers: safe account recovery plans

Account Recovery Assistant is a controlled alpha tool that helps rightful owners and authorized representatives prepare safe account recovery plans through official provider channels.

It does **not** recover accounts automatically, bypass security, crack passwords, or guarantee success.

## Current scenarios

- Google / Gmail lost MFA device
- Apple trusted device or trusted phone loss
- Facebook / Instagram hacked account
- Microsoft personal account recovery
- Microsoft 365 tenant/admin lockout

## What I need feedback on

If you have experienced account lockout or can test a safe simulated scenario, please tell me:

1. Which scenario did you test?
2. Was the **Next Best Action** clear?
3. Which checklist item was confusing?
4. Did the official link work?
5. What evidence was missing from the plan?
6. Would you prefer this as local self-serve, hosted web, human-assisted, or business/MSP workflow?

## Do not share sensitive data

Please do **not** post passwords, backup codes, SMS codes, authenticator codes, identity document scans/numbers, payment card data, or private account identifiers.

Use placeholders like:

```text
my Gmail account
old recovery email
business tenant
trusted phone
```

## Quick test command

```bash
git clone https://github.com/bortoq/account-recovery-assistant.git
cd account-recovery-assistant
python -m pip install .
account-recovery-assistant examples/lost_mfa.json
```

Or run the local web wizard:

```bash
PYTHONPATH=src python3 -m account_recovery_assistant --serve-web
```

## Feedback template

```text
Scenario tested:
Service:
Was the next best action clear? yes/no
Most useful section:
Most confusing section:
Did official links work? yes/no/not tested
What was missing?
Would you use this for a real recovery situation? yes/no/maybe
Preferred format: local / hosted / human-assisted / business/MSP
Sensitive data removed: yes
```

Stars are appreciated, but real scenario feedback is much more useful right now.
