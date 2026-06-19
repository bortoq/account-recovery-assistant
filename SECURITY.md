# Security Policy

## Supported Versions

This repository is currently a controlled alpha. Security fixes are applied to the latest `master` branch unless a release process states otherwise.

## Safety Boundary

Account Recovery Assistant must only help rightful owners and authorized representatives use official account recovery channels.

It must not provide instructions for:

- bypassing MFA or security checks;
- phishing or social engineering;
- password cracking or credential theft;
- session theft or device compromise;
- unauthorized access to someone else's account.

## Sensitive Data

Do not submit passwords, backup codes, SMS codes, authenticator codes, identity document scans, payment card numbers, or private recovery secrets in issues, discussions, feedback, examples, or pull requests.

## Reporting a Vulnerability

If you find a vulnerability or unsafe recovery path, please open a private report if GitHub private vulnerability reporting is enabled. If not, contact the repository owner with a minimal description and no sensitive account data.

Include:

- affected component;
- safe reproduction steps;
- expected vs actual behavior;
- why the behavior could enable abuse or leak data.

Do not include real user credentials, recovery codes, or identity documents.

## Maintainer Response Goals

For controlled alpha:

- acknowledge reports as soon as practical;
- prioritize issues that enable unauthorized access guidance or sensitive-data exposure;
- add regression tests for safety fixes where possible.
