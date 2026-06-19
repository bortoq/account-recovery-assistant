import json
from importlib.resources import files
from pathlib import Path
from typing import Any


def _data_path(name: str) -> Path:
    packaged = files("account_recovery_assistant.data").joinpath(name)
    if packaged.is_file():
        return Path(str(packaged))

    source_tree = Path(__file__).resolve().parents[2] / "data" / name
    if source_tree.is_file():
        return source_tree

    return Path(str(packaged))


def default_playbooks_path() -> Path:
    return _data_path("recovery_playbooks.json")


def default_service_priorities_path() -> Path:
    return _data_path("service_priorities.json")


def load_playbooks(path: str | Path | None = None) -> dict[str, Any]:
    playbook_path = Path(path) if path is not None else default_playbooks_path()
    with playbook_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_service_priorities(path: str | Path | None = None) -> dict[str, Any]:
    priorities_path = Path(path) if path is not None else default_service_priorities_path()
    with priorities_path.open(encoding="utf-8") as handle:
        return json.load(handle)
