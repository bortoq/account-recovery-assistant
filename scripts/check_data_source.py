#!/usr/bin/env python3
"""Verify the repository's single source of truth for knowledge-base data.

The canonical source of truth is `data/`. Package-local JSON files are no
longer tracked in `src/`; `setup.py` copies `data/*.json` into build artifacts.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data"
PACKAGE_DATA = ROOT / "src" / "account_recovery_assistant" / "data"
FILES = ["recovery_playbooks.json", "service_priorities.json"]


def main() -> int:
    missing = [name for name in FILES if not (SOURCE / name).is_file()]
    if missing:
        for name in missing:
            print(f"Missing source data file: data/{name}")
        return 1

    tracked_duplicates = [name for name in FILES if (PACKAGE_DATA / name).exists()]
    if tracked_duplicates:
        for name in tracked_duplicates:
            print(f"Remove duplicate package data file: src/account_recovery_assistant/data/{name}")
        return 1

    print("Data source of truth is data/. Build artifacts receive packaged JSON via setup.py build_py.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
