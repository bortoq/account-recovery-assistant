def _boolean_question(question_id: str, prompt: str) -> dict[str, object]:
    return {
        "id": question_id,
        "field": question_id,
        "prompt": prompt,
        "answer_type": "boolean",
        "required": True,
    }


def _role_question(prompt: str) -> dict[str, object]:
    return {
        "id": "role",
        "field": "role",
        "prompt": prompt,
        "answer_type": "single_choice",
        "required": True,
        "choices": [
            {"value": "owner", "label": "Rightful owner"},
            {"value": "authorized_representative", "label": "Authorized representative"},
            {"value": "not_authorized", "label": "Not authorized"},
        ],
    }


INCIDENTS = [
    {
        "id": "gmail_mfa_loss",
        "service": "Google / Gmail",
        "title": "Lost MFA device for a Google account",
        "questions": [
            _role_question("Are you the rightful owner or an authorized representative?"),
            _boolean_question("still_knows_password", "Do you still know the account password?"),
            _boolean_question("has_backup_codes", "Do you have backup codes for the account?"),
            _boolean_question("has_recovery_email", "Do you still control the recovery email?"),
            _boolean_question("has_trusted_device", "Do you still have a trusted signed-in device?"),
        ],
    },
    {
        "id": "apple_trusted_device_loss",
        "service": "Apple / iCloud",
        "title": "Lost trusted device or trusted phone for Apple ID recovery",
        "questions": [
            _role_question("Are you the rightful owner or an authorized representative?"),
            _boolean_question("still_knows_password", "Do you still know the Apple ID password?"),
            _boolean_question("has_trusted_device", "Do you still have a trusted Apple device?"),
            _boolean_question("has_trusted_phone", "Do you still control a trusted phone number?"),
            _boolean_question("has_purchase_proof", "Can you prove ownership of the device or account?"),
        ],
    },
    {
        "id": "meta_account_hacked",
        "service": "Meta",
        "title": "Facebook or Instagram account hacked",
        "questions": [
            _role_question("Are you the rightful owner or an authorized representative?"),
            _boolean_question("still_controls_email", "Do you still control the email linked to the account?"),
            _boolean_question("still_controls_phone", "Do you still control the phone linked to the account?"),
            _boolean_question("has_photo_id", "Can you provide photo ID if the service asks for it?"),
            _boolean_question("business_account", "Is this linked to a business page, creator account, or ad account?"),
        ],
    },
    {
        "id": "microsoft_admin_lockout",
        "service": "Microsoft",
        "title": "Microsoft admin or workspace lockout",
        "questions": [
            _role_question("Are you the admin, owner, or an authorized business representative?"),
            _boolean_question("still_knows_password", "Do you still know the account password?"),
            _boolean_question("has_backup_admin", "Is there another admin with working access?"),
            _boolean_question("has_billing_access", "Can you access billing or tenant records?"),
            _boolean_question("domain_control", "Do you control the verified business domain?"),
        ],
    },
]


def list_supported_incidents() -> list[dict[str, object]]:
    return [
        {
            "id": incident["id"],
            "service": incident["service"],
            "title": incident["title"],
            "questionnaire_id": incident["id"],
            "question_count": len(incident["questions"]),
        }
        for incident in INCIDENTS
    ]


def get_incident_questionnaire(incident_id: str) -> list[dict[str, object]]:
    for incident in INCIDENTS:
        if incident["id"] == incident_id:
            return incident["questions"]
    raise KeyError(f"Unknown incident: {incident_id}")


def get_incident_definition(incident_id: str) -> dict[str, object]:
    for incident in INCIDENTS:
        if incident["id"] == incident_id:
            return incident
    raise KeyError(f"Unknown incident: {incident_id}")
