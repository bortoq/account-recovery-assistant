INCIDENTS = [
    {
        "id": "gmail_mfa_loss",
        "service": "Google / Gmail",
        "title": "Lost MFA device for a Google account",
        "questions": [
            {"id": "role", "prompt": "Are you the rightful owner or an authorized representative?"},
            {"id": "still_knows_password", "prompt": "Do you still know the account password?"},
            {"id": "has_backup_codes", "prompt": "Do you have backup codes for the account?"},
            {"id": "has_recovery_email", "prompt": "Do you still control the recovery email?"},
            {"id": "has_trusted_device", "prompt": "Do you still have a trusted signed-in device?"},
        ],
    },
    {
        "id": "apple_trusted_device_loss",
        "service": "Apple / iCloud",
        "title": "Lost trusted device or trusted phone for Apple ID recovery",
        "questions": [
            {"id": "role", "prompt": "Are you the rightful owner or an authorized representative?"},
            {"id": "still_knows_password", "prompt": "Do you still know the Apple ID password?"},
            {"id": "has_trusted_device", "prompt": "Do you still have a trusted Apple device?"},
            {"id": "has_trusted_phone", "prompt": "Do you still control a trusted phone number?"},
            {"id": "has_purchase_proof", "prompt": "Can you prove ownership of the device or account?"},
        ],
    },
    {
        "id": "meta_account_hacked",
        "service": "Meta",
        "title": "Facebook or Instagram account hacked",
        "questions": [
            {"id": "role", "prompt": "Are you the rightful owner or an authorized representative?"},
            {"id": "still_controls_email", "prompt": "Do you still control the email linked to the account?"},
            {"id": "still_controls_phone", "prompt": "Do you still control the phone linked to the account?"},
            {"id": "has_photo_id", "prompt": "Can you provide photo ID if the service asks for it?"},
            {"id": "business_account", "prompt": "Is this linked to a business page, creator account, or ad account?"},
        ],
    },
    {
        "id": "microsoft_admin_lockout",
        "service": "Microsoft",
        "title": "Microsoft admin or workspace lockout",
        "questions": [
            {"id": "role", "prompt": "Are you the admin, owner, or an authorized business representative?"},
            {"id": "still_knows_password", "prompt": "Do you still know the account password?"},
            {"id": "has_backup_admin", "prompt": "Is there another admin with working access?"},
            {"id": "has_billing_access", "prompt": "Can you access billing or tenant records?"},
            {"id": "domain_control", "prompt": "Do you control the verified business domain?"},
        ],
    },
]


def list_supported_incidents() -> list[dict[str, str]]:
    return [
        {"id": incident["id"], "service": incident["service"], "title": incident["title"]}
        for incident in INCIDENTS
    ]


def get_incident_questionnaire(incident_id: str) -> list[dict[str, str]]:
    for incident in INCIDENTS:
        if incident["id"] == incident_id:
            return incident["questions"]
    raise KeyError(f"Unknown incident: {incident_id}")
