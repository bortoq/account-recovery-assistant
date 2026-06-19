#!/usr/bin/env python3
"""Copy top-level knowledge-base data into the package data directory.

The canonical source of truth is `data/`. The packaged copies under
`src/account_recovery_assistant/data/` are generated from it before builds.
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data"
TARGET = ROOT / "src" / "account_recovery_assistant" / "data"
FILES = ["recovery_playbooks.json", "service_priorities.json"]


def main() -> int:
    TARGET.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        source = SOURCE / name
        target = TARGET / name
        shutil.copyfile(source, target)
        print(f"Synced {source.relative_to(ROOT)} -> {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
