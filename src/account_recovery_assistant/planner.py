from typing import Any

from .playbooks import load_playbooks


UNAUTHORIZED_ROLES = {"not_authorized", "attacker", "unknown_third_party"}
UNSAFE_INTENT_WORDS = ("someone else", "without permission", "bypass", "hack", "phish")


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
    playbook = playbooks["playbooks"][case_type]
    service = str(situation.get("service", "the service"))

    return {
        "allowed": True,
        "case_type": case_type,
        "service": service,
        "checklist": playbook["checklist"],
        "evidence": playbook["evidence"],
        "official_links": _official_links_for(service, playbook),
        "support_message": _support_message(service, playbook),
        "hardening_steps": playbooks["hardening_steps"],
        "safety_warnings": playbooks["safety_warnings"],
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


def _official_links_for(service: str, playbook: dict[str, Any]) -> list[dict[str, str]]:
    service_key = service.strip().lower()
    links_by_service = playbook.get("official_links_by_service", {})
    if service_key in links_by_service:
        return links_by_service[service_key]
    return playbook["default_official_links"]


def _support_message(service: str, playbook: dict[str, Any]) -> str:
    return (
        f"I am the rightful owner or authorized representative for this {service} account. "
        f"{playbook['support_summary']} "
        "I can provide ownership evidence through the official recovery process."
    )
