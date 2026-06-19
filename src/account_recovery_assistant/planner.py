from datetime import date, timedelta
from typing import Any

from .playbooks import load_playbooks, load_service_priorities
from .questionnaire import get_incident_definition
from .validation import UNAUTHORIZED_ROLES, ALLOWED_ROLES


UNSAFE_INTENT_WORDS = (
    "someone else",
    "without permission",
    "bypass",
    "hack",
    "phish",
    "phishing",
    "social engineer",
    "steal",
    "ex girlfriend",
    "ex-boyfriend",
    "employee account",
    "get into",
    "взлом",
    "взломать",
    "фишинг",
    "без разрешения",
    "לפרוץ",
    "פישינג",
    "בלי רשות",
    "ללא רשות",
    "לעקוף",
)


def _refusal_plan(reason: str = "") -> dict[str, Any]:
    return {
        "allowed": False,
        "case_type": "unsafe_or_unauthorized",
        "reason": reason or "This assistant only helps the rightful owner or an authorized representative use official recovery channels.",
        "checklist": [],
        "evidence": [],
        "official_links": [],
        "support_message": "",
        "hardening_steps": [],
        "next_best_action": "",
        "prepare_now": [],
        "what_can_make_this_worse": [],
        "escalate_when": [],
        "expected_timeline": "",
        "safety_warnings": [
            "Do not attempt to access accounts without authorization.",
            "Use only official recovery procedures.",
        ],
        "questionnaire": None,
    }


def generate_recovery_plan(situation: dict[str, Any]) -> dict[str, Any]:
    if _is_unsafe_or_unauthorized(situation):
        return _refusal_plan("This assistant only helps the rightful owner or an authorized representative use official recovery channels.")

    if "role" not in situation or not situation.get("role"):
        return _refusal_plan("Role is required. Specify 'owner' or 'authorized_representative'.")
    if str(situation["role"]).lower() not in ALLOWED_ROLES:
        return _refusal_plan(f"Unsupported role '{situation['role']}'. Allowed roles: owner, authorized_representative.")

    playbooks = load_playbooks()
    service_priorities = load_service_priorities()
    provisional_case_type = _classify_case(situation)
    incident_record = _incident_record_for(situation, provisional_case_type, playbooks, service_priorities)
    case_type = str(incident_record["case_type"]) if incident_record else provisional_case_type
    playbook = playbooks["playbooks"][case_type]
    service = str(situation.get("service", "the service"))
    official_links = _official_links_for(service, playbook, service_priorities, incident_record)
    evidence = incident_record.get("ownership_evidence", playbook["evidence"]) if incident_record else playbook["evidence"]
    checklist = incident_record.get("checklist", playbook["checklist"]) if incident_record else playbook["checklist"]
    support_summary = incident_record.get("support_summary", playbook["support_summary"]) if incident_record else playbook["support_summary"]
    knowledge_base = _knowledge_base_status(incident_record)
    safety_warnings = _safety_warnings(playbooks["safety_warnings"], knowledge_base)
    questionnaire = _questionnaire_for(incident_record)
    guidance = _actionable_guidance(situation, service, case_type, incident_record)
    checklist = _merge_unique(checklist, guidance.get("checklist_additions", []))
    evidence = _merge_unique(evidence, guidance.get("evidence_additions", []))
    support_summary = _merge_support_summary(support_summary, guidance)

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
        "decision_path_id": guidance["decision_path_id"],
        "next_best_action": guidance["next_best_action"],
        "prepare_now": guidance["prepare_now"],
        "what_can_make_this_worse": guidance["what_can_make_this_worse"],
        "escalate_when": guidance["escalate_when"],
        "expected_timeline": guidance["expected_timeline"],
        "safety_warnings": safety_warnings,
        "common_mistakes": incident_record.get("common_mistakes", []) if incident_record else [],
        "knowledge_base": knowledge_base,
        "source_notes": incident_record.get("source_notes", []) if incident_record else [],
        "questionnaire": questionnaire,
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
        return {
            "last_verified_at": None,
            "review_due_at": None,
            "review_cadence_days": None,
            "confidence": "unknown",
            "status": "unverified",
            "stale": True,
        }
    review_cadence_days = int(incident_record.get("review_cadence_days", 30))
    review_due_at = incident_record.get("review_due_at") or _review_due_at(
        incident_record.get("last_verified_at"),
        review_cadence_days,
    )
    stale = bool(incident_record.get("stale", False)) or _is_past_due(review_due_at)
    status = str(incident_record.get("status") or ("needs_review" if stale else "verified"))
    if stale:
        status = "needs_review"
    return {
        "last_verified_at": incident_record.get("last_verified_at"),
        "review_due_at": review_due_at,
        "review_cadence_days": review_cadence_days,
        "confidence": incident_record.get("confidence", "unknown"),
        "status": status,
        "stale": stale,
    }


def _support_message(service: str, support_summary: str) -> str:
    return (
        f"I am the rightful owner or authorized representative for this {service} account. "
        f"{support_summary} "
        "I can provide ownership evidence through the official recovery process."
    )


def _review_due_at(last_verified_at: Any, review_cadence_days: int) -> str | None:
    if not last_verified_at:
        return None
    verified_date = date.fromisoformat(str(last_verified_at))
    return (verified_date + timedelta(days=review_cadence_days)).isoformat()


def _is_past_due(review_due_at: Any) -> bool:
    if not review_due_at:
        return False
    return date.fromisoformat(str(review_due_at)) < date.today()


def _questionnaire_for(incident_record: dict[str, Any] | None) -> dict[str, Any] | None:
    if not incident_record:
        return None
    incident = get_incident_definition(str(incident_record["id"]))
    return {
        "incident_id": incident["id"],
        "service": incident["service"],
        "title": incident["title"],
        "questions": incident["questions"],
    }


def _safety_warnings(base_warnings: list[str], knowledge_base: dict[str, Any]) -> list[str]:
    warnings = list(base_warnings)
    if knowledge_base["status"] != "verified":
        warnings.append(
            "Service-specific recovery details for this incident need review and should be treated as needs review before relying on them."
        )
    return warnings


def _actionable_guidance(
    situation: dict[str, Any],
    service: str,
    case_type: str,
    incident_record: dict[str, Any] | None,
) -> dict[str, Any]:
    if not incident_record:
        return {"decision_path_id": "generic", **_generic_guidance(service, case_type)}

    default_guidance = incident_record.get("default_guidance")
    if not default_guidance:
        return {"decision_path_id": "generic", **_generic_guidance(service, case_type)}

    guidance = dict(default_guidance)
    guidance["decision_path_id"] = str(default_guidance.get("id", "default"))

    for path in incident_record.get("decision_paths", []):
        if _decision_path_matches(situation, path.get("when", {})):
            guidance = _merge_guidance(guidance, path)
            guidance["decision_path_id"] = str(path.get("id", guidance["decision_path_id"]))
            break
    return guidance


def _generic_guidance(service: str, case_type: str) -> dict[str, Any]:
    return {
        "next_best_action": f"Use the official {service} recovery flow for this {case_type.replace('_', ' ')} and prepare ownership evidence before retrying.",
        "prepare_now": [
            "A short timeline of when access was lost.",
            "Any recovery email, recovery phone, or trusted device details still under your control.",
            "Recent billing, subscription, or account ownership records.",
        ],
        "what_can_make_this_worse": [
            "Too many repeated recovery attempts in a short period.",
            "Changing account details in the middle of a recovery review.",
            "Using unofficial help, phishing, or bypass tactics.",
        ],
        "escalate_when": [
            "The official recovery flow loops without offering a working path.",
            "You can prove ownership but the service keeps rejecting stable evidence.",
        ],
        "expected_timeline": "varies by provider and whether you still control trusted recovery factors",
    }


def _decision_path_matches(situation: dict[str, Any], conditions: dict[str, Any]) -> bool:
    for key, expected in conditions.items():
        actual = situation.get(key)
        if actual != expected:
            return False
    return True


def _merge_guidance(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if key in {"id", "when"}:
            continue
        if isinstance(value, list):
            merged[key] = list(value)
        else:
            merged[key] = value
    return merged


def _merge_support_summary(support_summary: str, guidance: dict[str, Any]) -> str:
    override = guidance.get("support_summary_override")
    if override:
        return str(override)
    addition = guidance.get("support_summary_addition")
    if addition:
        return f"{support_summary} {addition}"
    return support_summary


def _merge_unique(base: list[str], additions: list[str]) -> list[str]:
    merged = list(base)
    for item in additions:
        if item not in merged:
            merged.append(item)
    return merged
