# Account Recovery Assistant

Account Recovery Assistant is a safe guide for people who lost access to an account, got stuck in multi-factor authentication, forgot recovery details, or need help using official recovery channels.

## Simple Description

This is an account recovery helper. It does not hack accounts or bypass security. It helps the rightful owner understand what happened, collect proof, choose the right official process, and avoid mistakes that make recovery harder.

## Full Description

People lose access to email, social media, banking, work, gaming, domain, and cloud accounts. Common causes include forgotten passwords, lost phones, broken authenticator apps, changed phone numbers, missing backup codes, suspicious activity locks, old recovery emails, and business admin turnover.

Official recovery flows are often confusing. Users do not know what information is required, why forms are rejected, or which actions look suspicious. Account Recovery Assistant turns recovery into a guided process: identify the account and failure type, collect ownership evidence, find the official recovery channel, prepare support messages, track attempts, and harden the account after access is restored.

## Safety Principle

The product must only help the rightful owner or an authorized representative. It must not provide instructions for bypassing MFA, phishing, social engineering, password cracking, device hacking, or session theft. All guidance must use official service procedures.

## Main Use Cases

- A user lost a phone with an authenticator app.
- A user changed phone numbers and cannot receive SMS codes.
- A user forgot a password and lost access to the recovery email.
- An account is locked after suspicious activity.
- A family member needs to recover an account through official estate procedures.
- A small business lost access to an ad, domain, or cloud account.

## MVP

- Diagnostic questionnaire
- Step-by-step recovery checklist
- Database of official recovery links for popular services
- Support message generator
- List of documents and proof to prepare
- Post-recovery security checklist: backup codes, passkeys, recovery contacts, and password manager setup

## Current Prototype

The first prototype is a small Python CLI and core library. It reads a JSON situation file and prints a safe recovery plan as JSON.

Run an example:

```bash
PYTHONPATH=src python3 -m account_recovery_assistant examples/lost_mfa.json
```

Print a readable Markdown report:

```bash
PYTHONPATH=src python3 -m account_recovery_assistant --format markdown examples/lost_mfa.json
```

Run tests:

```bash
PYTHONPATH=src python3 -m pytest -v
```

Supported MVP scenarios:

- lost MFA device;
- changed phone number;
- suspicious activity lock.

The planner also uses `data/service_priorities.json` for aliases and official links for the first top-priority services, including Google/Gmail, Apple/iCloud, Facebook, Instagram, Microsoft/Outlook, X/Twitter, TikTok, Yahoo Mail, LinkedIn, and Telegram.

## Similar Projects And Difference

- Passware, Lazesoft, Ophcrack, and John the Ripper recover or crack passwords for files, devices, and local systems. Account Recovery Assistant is different: it does not crack passwords. It guides users through official account recovery.
- Password managers help prevent future loss, but they do not solve the full recovery situation once MFA, phone access, or support workflows fail.
- Official help centers from Google, Apple, Meta, Microsoft, banks, and SaaS products contain the correct procedures, but they are scattered and hard to navigate.
- IT support and managed service providers can help businesses manually. This project turns that help into a guided workflow with evidence collection and message templates.
- Shady “account recovery” services and hacking offers are the opposite of this project. Account Recovery Assistant must stay legal, safe, and owner-only.

The main difference is safe navigation: understand the situation, collect proof, use official channels, and protect the account after recovery.

## Value

- Less panic and confusion
- Fewer mistakes that make recovery harder
- Faster evidence collection
- Clear navigation through official procedures
- Better prevention after recovery

## Risks

- The product must clearly separate owner recovery from attacker guidance.
- Recovery procedures change often and the knowledge base must stay current.
- It cannot promise guaranteed recovery.
- Financial, corporate, and estate cases may need legal or administrative procedures.

## Monetization

- Free basic diagnosis
- Paid detailed recovery plans
- Small business subscription for account inventory and recovery planning
- Partnerships with IT support, legal services, and managed service providers

## Documents

See [docs/current-usage.md](docs/current-usage.md) for the current MVP workflow and user value.

See [docs/service-priorities.md](docs/service-priorities.md) for the first knowledge-base expansion plan.

See [roadmap.md](roadmap.md).
