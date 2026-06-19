# Account Recovery Assistant CLI MVP Design

## Goal

Build a small safety-first CLI and core library that turns a structured account recovery situation into a safe recovery plan.

## Scope

The MVP supports three scenarios:

- lost MFA device;
- changed phone number;
- suspicious activity lock.

The output includes case type, checklist, evidence list, official links, support message, safety warnings, and post-recovery hardening steps.

## Non-Goals

- No hacking, bypass, cracking, phishing, social engineering, or unauthorized access guidance.
- No web UI.
- No automated account access.
- No provider-specific guarantee of recovery.

## Architecture

The implementation is a Python package with pure functions and a CLI wrapper. Recovery playbooks live in JSON so the knowledge base can be updated without changing code. Tests verify behavior and safety boundaries.

## Data Flow

1. CLI reads a JSON situation file.
2. Core classifier maps inputs to a supported scenario.
3. Planner loads the matching playbook.
4. Planner generates a safe recovery plan.
5. CLI prints JSON output.

## Safety Rules

The product helps only rightful owners or authorized representatives. Dangerous intent or unsupported unauthorized scenarios must return a refusal-style safety response instead of procedural guidance.
