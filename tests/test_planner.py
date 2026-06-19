from account_recovery_assistant import generate_recovery_plan, get_incident_questionnaire, list_supported_incidents


def test_lost_mfa_device_plan_uses_official_recovery_and_backup_codes():
    situation = {
        "service": "Google",
        "lost_factor": "authenticator_app",
        "still_knows_password": True,
        "has_backup_codes": True,
        "role": "owner",
    }

    plan = generate_recovery_plan(situation)

    assert plan["case_type"] == "lost_mfa_device"
    assert plan["allowed"] is True
    assert any("backup codes" in item.lower() for item in plan["checklist"])
    assert any(link["label"] == "Google Account Recovery" for link in plan["official_links"])
    assert "I am the rightful owner" in plan["support_message"]
    assert any("passkey" in item.lower() for item in plan["hardening_steps"])


def test_changed_phone_number_plan_prioritizes_recovery_email_and_trusted_devices():
    situation = {
        "service": "Apple",
        "lost_factor": "phone_number",
        "still_knows_password": True,
        "has_recovery_email": True,
        "has_trusted_device": True,
        "role": "owner",
    }

    plan = generate_recovery_plan(situation)

    assert plan["case_type"] == "changed_phone_number"
    assert plan["allowed"] is True
    assert any("recovery email" in item.lower() for item in plan["checklist"])
    assert any("trusted device" in item.lower() for item in plan["evidence"])
    assert any(link["label"] == "Apple Account Recovery" for link in plan["official_links"])


def test_suspicious_activity_lock_plan_warns_against_repeated_attempts():
    situation = {
        "service": "Microsoft",
        "account_state": "locked_suspicious_activity",
        "still_knows_password": False,
        "role": "owner",
    }

    plan = generate_recovery_plan(situation)

    assert plan["case_type"] == "suspicious_activity_lock"
    assert plan["allowed"] is True
    assert any("repeated" in item.lower() for item in plan["checklist"])
    assert any("recent sign-in" in item.lower() for item in plan["evidence"])
    assert any(link["label"] == "Microsoft Account Recovery" for link in plan["official_links"])


def test_unsafe_intent_returns_refusal_without_procedural_steps():
    situation = {
        "service": "Instagram",
        "intent": "recover someone else's account without permission",
        "role": "not_authorized",
    }

    plan = generate_recovery_plan(situation)

    assert plan["allowed"] is False
    assert plan["case_type"] == "unsafe_or_unauthorized"
    assert "rightful owner" in plan["reason"].lower()
    assert plan["checklist"] == []
    assert plan["official_links"] == []


def test_service_priority_aliases_supply_official_links_for_top_services():
    situation = {
        "service": "IG",
        "lost_factor": "authenticator_app",
        "role": "owner",
    }

    plan = generate_recovery_plan(situation)

    assert plan["service"] == "IG"
    assert any(link["label"] == "Instagram Hacked Account" for link in plan["official_links"])


def test_bypass_and_phishing_intents_are_refused_even_when_role_claims_owner():
    for intent in ["bypass MFA", "phish support agent", "hack my old account"]:
        plan = generate_recovery_plan(
            {
                "service": "Google",
                "lost_factor": "authenticator_app",
                "role": "owner",
                "intent": intent,
            }
        )

        assert plan["allowed"] is False
        assert plan["case_type"] == "unsafe_or_unauthorized"
        assert plan["checklist"] == []


def test_supported_incidents_include_high_value_web_wizard_cases():
    incidents = list_supported_incidents()

    assert [incident["id"] for incident in incidents] == [
        "gmail_mfa_loss",
        "apple_trusted_device_loss",
        "meta_account_hacked",
        "microsoft_admin_lockout",
    ]
    assert incidents[0]["service"] == "Google / Gmail"
    assert incidents[-1]["service"] == "Microsoft"


def test_gmail_mfa_questionnaire_starts_with_clear_entry_questions():
    questions = get_incident_questionnaire("gmail_mfa_loss")

    assert questions[0]["id"] == "role"
    assert questions[1]["id"] == "still_knows_password"
    assert any(question["id"] == "has_backup_codes" for question in questions)
    assert any(question["id"] == "has_recovery_email" for question in questions)
    assert all("prompt" in question for question in questions)


def test_meta_hacked_questionnaire_asks_about_account_control_and_identity():
    questions = get_incident_questionnaire("meta_account_hacked")

    assert any(question["id"] == "still_controls_email" for question in questions)
    assert any(question["id"] == "still_controls_phone" for question in questions)
    assert any(question["id"] == "has_photo_id" for question in questions)


def test_unknown_incident_questionnaire_returns_key_error():
    try:
        get_incident_questionnaire("unknown_incident")
    except KeyError as exc:
        assert "unknown_incident" in str(exc)
    else:
        raise AssertionError("Expected KeyError for unknown incident")
