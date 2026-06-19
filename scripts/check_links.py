#!/usr/bin/env python3
"""Check official-link URLs stored in the packaged knowledge base.

This is intentionally dependency-free. Some providers block automated checks
with 403/429 even when links work in a browser; those statuses are reported as
manual-review rather than hard failures.
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

DATA_FILES = [
    Path("data/recovery_playbooks.json"),
    Path("data/service_priorities.json"),
]
MANUAL_REVIEW_STATUSES = {403, 429}
USER_AGENT = "account-recovery-assistant-link-check/1.0"


def iter_links(value: Any):
    if isinstance(value, dict):
        if "url" in value:
            yield value.get("label", "Unlabeled"), str(value["url"])
        for child in value.values():
            yield from iter_links(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_links(child)


def check_url(url: str) -> tuple[str, str]:
    for method in ("HEAD", "GET"):
        try:
            request = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=12) as response:
                status = response.status
                if 200 <= status < 400:
                    return "ok", f"{status} -> {response.geturl()}"
                if status in MANUAL_REVIEW_STATUSES:
                    return "manual", f"{status} bot-protection/manual-review"
                return "fail", f"{status}"
        except urllib.error.HTTPError as exc:
            if exc.code in MANUAL_REVIEW_STATUSES:
                return "manual", f"{exc.code} bot-protection/manual-review"
            last_error = f"HTTP {exc.code}"
        except Exception as exc:  # noqa: BLE001 - CLI diagnostics should show any network failure.
            last_error = f"{type(exc).__name__}: {exc}"
    return "fail", last_error


def main() -> int:
    seen: set[str] = set()
    links: list[tuple[str, str]] = []
    for data_file in DATA_FILES:
        payload = json.loads(data_file.read_text(encoding="utf-8"))
        for label, url in iter_links(payload):
            if url not in seen:
                seen.add(url)
                links.append((label, url))

    failures = 0
    manual = 0
    for label, url in links:
        status, detail = check_url(url)
        print(f"{status.upper():6} {label}: {url} ({detail})")
        if status == "fail":
            failures += 1
        elif status == "manual":
            manual += 1

    print(f"\nChecked {len(links)} unique URLs: {failures} failure(s), {manual} manual-review URL(s).")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
