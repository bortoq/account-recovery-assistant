# v0.1.0

## Summary

First public MVP release of Account Recovery Assistant.

This version ships a safety-first local CLI and local web wizard for the first four canonical recovery incident families:

- Gmail MFA loss
- Apple trusted-device or trusted-phone loss
- Meta account takeover
- Microsoft admin or workspace lockout

## Highlights

- Local web wizard on top of the same recovery engine as the CLI
- Normalized questionnaire contract for the first high-value incidents
- Incident-specific knowledge freshness metadata
- Data-driven `decision_paths` for first-pass recovery branching
- Actionable outputs such as:
  - next best action
  - prepare-now evidence list
  - what can make recovery worse
  - escalation triggers
  - expected timeline
- Expanded example scenarios for Google, Apple, Meta, and Microsoft

## Safety Boundary

This project only helps the rightful owner or an authorized representative use official recovery channels.

It does not provide bypass, phishing, cracking, social engineering, or unauthorized access guidance.

## Artifacts

- `account_recovery_assistant-0.1.0.tar.gz`
- `account_recovery_assistant-0.1.0-py3-none-any.whl`
