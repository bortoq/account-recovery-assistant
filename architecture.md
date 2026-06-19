# Architecture

## Overview

Account Recovery Assistant is a safety-first guided workflow. It diagnoses the access problem and maps it to official recovery procedures.

## Components

- Diagnostic Wizard: identifies account type, lost factor, remaining access, and user role.
- Recovery Taxonomy: classifies the case into known recovery patterns.
- Official Procedure Database: stores verified links, requirements, and last-check dates.
- Evidence Checklist Generator: lists proof the user should prepare.
- Support Message Generator: writes clear, non-suspicious support messages.
- Safety Filter: blocks bypass, hacking, phishing, social engineering, and unauthorized-access guidance.
- Hardening Checklist: recommends backup codes, passkeys, password manager setup, and recovery contacts.

## Data Flow

1. User answers diagnostic questions.
2. The system classifies the recovery case.
3. The system selects official procedures.
4. The assistant generates a safe checklist and support message.
5. After recovery, the assistant generates a hardening plan.

## Safety Boundary

The product helps only rightful owners or authorized representatives. It must never become a tool for attackers.
