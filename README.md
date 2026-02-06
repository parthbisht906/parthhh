# OSINT Starter Toolkit (Phone + Social)

This repository provides a **starter** OSINT helper that focuses on **phone number parsing** and **social media username checks**. It is designed to be a small, ethical baseline you can extend with your own data sources.

> ⚠️ **Responsible use only**: Use this tool solely on data you own, have explicit permission to analyze, or is publicly available with lawful intent. Avoid harassment, stalking, or violating platform terms of service.

## Features

- **Phone number analysis** via `phonenumbers` (E164 format, validity, region, carrier, timezone)
- **Social media username checks** by testing public profile URLs
- JSON or human-readable output

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Phone number

```bash
python -m osint_tool.cli phone "+1 415 555 0132" --region US
```

### Social media username

```bash
python -m osint_tool.cli social "octocat"
```

### JSON output

```bash
python -m osint_tool.cli phone "+1 415 555 0132" --json
python -m osint_tool.cli social "octocat" --json
```

## Extending the tool

- Add more platforms in `osint_tool.checks.DEFAULT_PLATFORMS`
- Replace URL checks with official APIs where possible
- Add new subcommands (e.g., email, domain, or breach lookups)

## Notes

Some platforms aggressively rate-limit or block automated checks. If a platform returns 403/429, treat it as **unknown** and consider switching to an official API.
