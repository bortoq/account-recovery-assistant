# Service Priorities

This document captures the first service expansion plan for the knowledge base.

## Why This Matters

The first playbooks should cover accounts that are both common and high-impact. Email and phone-linked accounts often become recovery anchors for many other services, so losing them can cascade into broader digital life loss.

## Top 10 Services To Add First

1. Google / Gmail
2. Apple ID / iCloud
3. Facebook
4. Instagram
5. Microsoft / Outlook / Hotmail
6. X / Twitter
7. TikTok
8. Yahoo Mail
9. LinkedIn
10. Telegram

## Rationale

- Criticality: email, Apple ID, and Microsoft accounts often control access to many other services.
- Frequency: Google and Meta account recovery problems are common user complaints.
- User reach: the list covers a large share of normal consumer recovery cases.
- Business value: users are more likely to pay for help with Gmail, Apple ID, Facebook, Instagram, and business-linked Microsoft accounts.
- Recovery complexity: high-friction services need clearer checklists and expectation setting.

## Next Candidates

- WhatsApp: strongly tied to phone number and device migration.
- GitHub: high value for developers and open-source maintainers.
- Discord: important for gaming and community accounts.
- PayPal / Stripe: financial accounts with stronger verification and risk controls.
- Banking apps: should start as a generic high-safety playbook before adding country-specific banks.

## Implementation Notes

Each service should eventually have a JSON playbook with:

- official recovery and support links;
- supported scenarios such as lost phone, hacked account, lost MFA, and locked account;
- evidence the user should prepare;
- waiting periods and risk warnings where applicable;
- post-recovery hardening steps.

Do not add unofficial hacks, bypasses, or social-engineering tactics. If a service procedure is unclear, link to the official help center and mark the detailed flow as unverified.
