from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .questionnaire import get_incident_definition

UNAUTHORIZED_ROLES = {"not_authorized", "attacker", "unknown_third_party"}
ALLOWED_ROLES = {"owner", "authorized_representative", *UNAUTHORIZED_ROLES}


@dataclass
class ValidationError(Exception):
    field: str
    message: str

    def __str__(self) -> str:
        return f"{self.field}: {self.message}"


def validate_situation(situation: dict[str, Any]) -> dict[str, Any]:
    role = situation.get("role")
    if not role:
        raise ValidationError("role", "Missing required field.")
    normalized_role = str(role).lower()
    if normalized_role not in ALLOWED_ROLES:
        raise ValidationError("role", "Unsupported role value.")
    situation["role"] = normalized_role

    incident_id = situation.get("incident_id")
    if incident_id:
        incident = get_incident_definition(str(incident_id))
        questions = incident["questions"]
        for question in questions:
            if not question.get("required", False):
                continue
            field = str(question["field"])
            if field not in situation:
                raise ValidationError(field, "Missing required field.")
            if question["answer_type"] == "boolean" and not isinstance(situation[field], bool):
                raise ValidationError(field, "Expected a boolean value.")
            if question["answer_type"] == "single_choice":
                choices = {str(choice["value"]) for choice in question.get("choices", [])}
                if str(situation[field]) not in choices:
                    raise ValidationError(field, "Unsupported choice value.")

    return situation
