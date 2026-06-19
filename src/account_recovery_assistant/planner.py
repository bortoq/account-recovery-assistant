from typing import Any

from .playbooks import load_playbooks, load_service_priorities


UNAUTHORIZED_ROLES = {"not_authorized", "attacker", "unknown_third_party"}
UNSAFE_INTENT_WORDS = (
    "someone else",
    "without permission",
    "bypass",
    "hack",
    "phish",
    "phishing",
    "social engineer",
)


def generate_recovery_plan(situation: dict[str, Any]) -> dict[str, Any]:
    if _is_unsafe_or_unauthorized(situation):
        return {
            "allowed": False,
            "case_type": "unsafe_or_unauthorized",
            "reason": "This assistant only helps the rightful owner or an authorized representative use official recovery channels.",
            "checklist": [],
            "evidence": [],
            "official_links": [],
            "support_message": "",
            "hardening_steps": [],
            "safety_warnings": [
                "Do not attempt to access accounts without authorization.",
                "Use only official recovery procedures.",
            ],
        }

    case_type = _classify_case(situation)
    playbooks = load_playbooks()
    service_priorities = load_service_priorities()
    playbook = playbooks["playbooks"][case_type]
    incident_record = _incident_record_for(situation, case_type, playbooks, service_priorities)
    service = str(situation.get("service", "the service"))
    official_links = _official_links_for(service, playbook, service_priorities, incident_record)
    evidence = incident_record.get("ownership_evidence", playbook["evidence"]) if incident_record else playbook["evidence"]
    checklist = incident_record.get("checklist", playbook["checklist"]) if incident_record else playbook["checklist"]
    support_summary = incident_record.get("support_summary", playbook["support_summary"]) if incident_record else playbook["support_summary"]

    return {
        "allowed": True,
        "case_type": case_type,
        "incident_id": incident_record.get("id") if incident_record else None,
        "incident_title": incident_record.get("title") if incident_record else None,
        "service": service,
        "checklist": checklist,
        "evidence": evidence,
        "official_links": official_links,
        "support_message": _support_message(service, support_summary),
        "hardening_steps": playbooks["hardening_steps"],
        "safety_warnings": playbooks["safety_warnings"],
        "common_mistakes": incident_record.get("common_mistakes", []) if incident_record else [],
        "knowledge_base": _knowledge_base_status(incident_record),
        "source_notes": incident_record.get("source_notes", []) if incident_record else [],
    }


def _is_unsafe_or_unauthorized(situation: dict[str, Any]) -> bool:
    role = str(situation.get("role", "")).lower()
    intent = str(situation.get("intent", "")).lower()
    return role in UNAUTHORIZED_ROLES or any(word in intent for word in UNSAFE_INTENT_WORDS)


def _classify_case(situation: dict[str, Any]) -> str:
    lost_factor = str(situation.get("lost_factor", "")).lower()
    account_state = str(situation.get("account_state", "")).lower()

    if lost_factor == "authenticator_app":
        return "lost_mfa_device"
    if lost_factor == "phone_number":
        return "changed_phone_number"
    if account_state == "locked_suspicious_activity":
        return "suspicious_activity_lock"
    return "lost_mfa_device"


def _incident_record_for(
    situation: dict[str, Any],
    case_type: str,
    playbooks: dict[str, Any],
    service_priorities: dict[str, Any],
) -> dict[str, Any] | None:
    incident_records = playbooks.get("incident_records", {})
    explicit_incident_id = situation.get("incident_id")
    if explicit_incident_id in incident_records:
        return {"id": explicit_incident_id, **incident_records[explicit_incident_id]}

    service_names = _service_names(str(situation.get("service", "")), service_priorities)
    for incident_id, incident_record in incident_records.items():
        if incident_record.get("case_type") != case_type:
            continue
        aliases = {str(alias).lower() for alias in incident_record.get("service_aliases", [])}
        if service_names & aliases:
            return {"id": incident_id, **incident_record}
    return None


def _official_links_for(
    service: str,
    playbook: dict[str, Any],
    service_priorities: dict[str, Any],
    incident_record: dict[str, Any] | None,
) -> list[dict[str, str]]:
    if incident_record and incident_record.get("official_links"):
        return incident_record["official_links"]

    service_key = service.strip().lower()
    priority_links = _priority_links_for(service_key, service_priorities)
    if priority_links:
        return priority_links

    links_by_service = playbook.get("official_links_by_service", {})
    if service_key in links_by_service:
        return links_by_service[service_key]
    return playbook["default_official_links"]


def _priority_links_for(service_key: str, service_priorities: dict[str, Any]) -> list[dict[str, str]]:
    for service in service_priorities.get("top_services", []):
        aliases = {str(alias).lower() for alias in service.get("aliases", [])}
        names = {str(service.get("service", "")).lower(), *aliases}
        if service_key in names:
            return service.get("official_links", [])
    return []


def _service_names(service: str, service_priorities: dict[str, Any]) -> set[str]:
    service_key = service.strip().lower()
    names = {service_key}
    for item in service_priorities.get("top_services", []):
        aliases = {str(alias).lower() for alias in item.get("aliases", [])}
        item_names = {str(item.get("service", "")).lower(), *aliases}
        if service_key in item_names:
            names |= item_names
    return names


def _knowledge_base_status(incident_record: dict[str, Any] | None) -> dict[str, Any]:
    if not incident_record:
        return {"last_verified_at": None, "confidence": "unknown", "stale": True}
    return {
        "last_verified_at": incident_record.get("last_verified_at"),
        "confidence": incident_record.get("confidence", "unknown"),
        "stale": bool(incident_record.get("stale", False)),
    }


def _support_message(service: str, support_summary: str) -> str:
    return (
        f"I am the rightful owner or authorized representative for this {service} account. "
        f"{support_summary} "
        "I can provide ownership evidence through the official recovery process."
    )
