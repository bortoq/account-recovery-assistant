import json
from importlib.resources import files
from pathlib import Path
from typing import Any


def default_playbooks_path() -> Path:
    return Path(str(files("account_recovery_assistant.data").joinpath("recovery_playbooks.json")))


def default_service_priorities_path() -> Path:
    return Path(str(files("account_recovery_assistant.data").joinpath("service_priorities.json")))


def load_playbooks(path: str | Path | None = None) -> dict[str, Any]:
    playbook_path = Path(path) if path is not None else default_playbooks_path()
    with playbook_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_service_priorities(path: str | Path | None = None) -> dict[str, Any]:
    priorities_path = Path(path) if path is not None else default_service_priorities_path()
    with priorities_path.open(encoding="utf-8") as handle:
        return json.load(handle)
