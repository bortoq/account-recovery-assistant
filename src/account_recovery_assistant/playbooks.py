import json
from pathlib import Path
from typing import Any


def default_playbooks_path() -> Path:
    return Path(__file__).resolve().parents[2] / "data" / "recovery_playbooks.json"


def load_playbooks(path: str | Path | None = None) -> dict[str, Any]:
    playbook_path = Path(path) if path is not None else default_playbooks_path()
    with playbook_path.open(encoding="utf-8") as handle:
        return json.load(handle)
