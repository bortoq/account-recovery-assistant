#!/usr/bin/env python3
"""Validate knowledge-base data without external dependencies."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RECOVERY_PATH = ROOT / "data" / "recovery_playbooks.json"
PRIORITIES_PATH = ROOT / "data" / "service_priorities.json"
PACKAGED_RECOVERY_PATH = ROOT / "src" / "account_recovery_assistant" / "data" / "recovery_playbooks.json"
PACKAGED_PRIORITIES_PATH = ROOT / "src" / "account_recovery_assistant" / "data" / "service_priorities.json"
QUESTIONNAIRE_PATH = ROOT / "src" / "account_recovery_assistant" / "questionnaire.py"


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_links(links: Any, path: str, errors: list[str]) -> None:
    require(isinstance(links, list) and bool(links), f"{path}: official_links must be a non-empty list", errors)
    if not isinstance(links, list):
        return
    for index, link in enumerate(links):
        location = f"{path}.official_links[{index}]"
        require(isinstance(link, dict), f"{location}: link must be an object", errors)
        if not isinstance(link, dict):
            continue
        require(bool(link.get("label")), f"{location}: missing label", errors)
        url = link.get("url")
        require(isinstance(url, str) and url.startswith("https://"), f"{location}: url must start with https://", errors)


def validate_recovery_playbooks(data: dict[str, Any], errors: list[str]) -> None:
    for key in ["safety_warnings", "hardening_steps", "incident_records", "playbooks"]:
        require(key in data, f"recovery_playbooks: missing {key}", errors)
    require(isinstance(data.get("safety_warnings"), list) and data.get("safety_warnings"), "safety_warnings must be non-empty", errors)
    require(isinstance(data.get("hardening_steps"), list) and data.get("hardening_steps"), "hardening_steps must be non-empty", errors)

    incident_records = data.get("incident_records", {})
    require(isinstance(incident_records, dict) and incident_records, "incident_records must be a non-empty object", errors)
    for incident_id, record in incident_records.items():
        path = f"incident_records.{incident_id}"
        for key in [
            "case_type",
            "service_aliases",
            "title",
            "support_summary",
            "last_verified_at",
            "review_due_at",
            "confidence",
            "status",
            "checklist",
            "ownership_evidence",
            "official_links",
            "default_guidance",
        ]:
            require(key in record, f"{path}: missing {key}", errors)
        require(record.get("case_type") in data.get("playbooks", {}), f"{path}: unknown case_type {record.get('case_type')}", errors)
        require(isinstance(record.get("service_aliases"), list) and record.get("service_aliases"), f"{path}: service_aliases must be non-empty", errors)
        require(record.get("status") in {"verified", "needs_review", "unverified"}, f"{path}: invalid status", errors)
        validate_links(record.get("official_links"), path, errors)
        guidance = record.get("default_guidance", {})
        for key in ["id", "next_best_action", "prepare_now", "what_can_make_this_worse", "escalate_when", "expected_timeline"]:
            require(key in guidance, f"{path}.default_guidance: missing {key}", errors)


def validate_service_priorities(data: dict[str, Any], errors: list[str]) -> None:
    services = data.get("top_services")
    require(isinstance(services, list) and services, "top_services must be a non-empty list", errors)
    if not isinstance(services, list):
        return
    priorities = [service.get("priority") for service in services if isinstance(service, dict)]
    require(priorities == list(range(1, len(priorities) + 1)), "service priorities must be sequential", errors)
    for service in services:
        name = service.get("service") if isinstance(service, dict) else "unknown"
        path = f"top_services.{name}"
        for key in ["priority", "service", "aliases", "criticality", "recovery_complexity", "recommended_focus", "official_links"]:
            require(isinstance(service, dict) and key in service, f"{path}: missing {key}", errors)
        if isinstance(service, dict):
            validate_links(service.get("official_links"), path, errors)
            if service.get("manual_review_required"):
                require(bool(service.get("manual_review_reason")), f"{path}: manual review reason required", errors)
                for link in service.get("official_links", []):
                    require(link.get("review_status") == "manual_review_required", f"{path}: manual-review link missing review_status", errors)


def validate_questionnaire_alignment(recovery: dict[str, Any], errors: list[str]) -> None:
    questionnaire_source = QUESTIONNAIRE_PATH.read_text(encoding="utf-8")
    for incident_id in recovery.get("incident_records", {}):
        require(f'"{incident_id}"' in questionnaire_source, f"questionnaire missing incident id {incident_id}", errors)


def main() -> int:
    errors: list[str] = []
    recovery = load_json(RECOVERY_PATH)
    priorities = load_json(PRIORITIES_PATH)
    packaged_recovery = load_json(PACKAGED_RECOVERY_PATH)
    packaged_priorities = load_json(PACKAGED_PRIORITIES_PATH)

    require(recovery == packaged_recovery, "data/recovery_playbooks.json differs from packaged copy", errors)
    require(priorities == packaged_priorities, "data/service_priorities.json differs from packaged copy", errors)
    validate_recovery_playbooks(recovery, errors)
    validate_service_priorities(priorities, errors)
    validate_questionnaire_alignment(recovery, errors)

    if errors:
        print("Data validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Data validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
