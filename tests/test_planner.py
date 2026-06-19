from account_recovery_assistant import (
    generate_recovery_plan,
    get_incident_questionnaire,
    list_supported_incidents,
)


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
    assert plan["incident_id"] == "gmail_mfa_loss"
    assert plan["incident_title"] == "Lost MFA device for a Google account"
    assert any("backup codes" in item.lower() for item in plan["checklist"])
    assert any(link["label"] == "Google Account Recovery" for link in plan["official_links"])
    assert plan["knowledge_base"]["last_verified_at"] == "2026-06-19"
    assert plan["knowledge_base"]["confidence"] == "high"
    assert plan["knowledge_base"]["stale"] is False
    assert "backup code" in plan["next_best_action"].lower()
    assert plan["expected_timeline"] == "immediate if backup codes or a trusted session still work"
    assert any("backup code" in item.lower() for item in plan["prepare_now"])
    assert any("too many" in item.lower() for item in plan["common_mistakes"])
    assert any("official recovery flow" in note.lower() for note in plan["source_notes"])
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
    assert plan["incident_id"] == "apple_trusted_device_loss"
    assert any("recovery email" in item.lower() for item in plan["checklist"])
    assert any("trusted device" in item.lower() for item in plan["evidence"])
    assert any(link["label"] == "Apple Account Recovery" for link in plan["official_links"])
    assert any("trusted phone" in item.lower() for item in plan["evidence"])
    assert "trusted device" in plan["next_best_action"].lower()
    assert any("account recovery wait period" in item.lower() for item in plan["escalate_when"])


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
    assert "business support" in plan["next_best_action"].lower()
    assert any("tenant" in item.lower() for item in plan["prepare_now"])


def test_explicit_meta_incident_uses_incident_specific_playbook_and_links():
    situation = {
        "service": "Instagram",
        "incident_id": "meta_account_hacked",
        "account_state": "locked_suspicious_activity",
        "role": "owner",
    }

    plan = generate_recovery_plan(situation)

    assert plan["case_type"] == "suspicious_activity_lock"
    assert plan["incident_id"] == "meta_account_hacked"
    assert any("photo id" in item.lower() for item in plan["evidence"])
    assert any(link["label"] == "Instagram Hacked Account" for link in plan["official_links"])
    assert plan["knowledge_base"]["confidence"] == "medium"
    assert any("recovery email or phone" in item.lower() for item in plan["common_mistakes"])
    assert "hacked-account flow" in plan["next_best_action"].lower()
    assert any("duplicate reports" in item.lower() for item in plan["what_can_make_this_worse"])


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
    assert questions[0]["field"] == "role"
    assert questions[0]["answer_type"] == "single_choice"
    assert questions[0]["required"] is True
    assert questions[1]["id"] == "still_knows_password"
    assert any(question["id"] == "has_backup_codes" for question in questions)
    assert any(question["id"] == "has_recovery_email" for question in questions)
    assert all("prompt" in question for question in questions)
    assert all("field" in question for question in questions)
    assert all("answer_type" in question for question in questions)
    assert all("required" in question for question in questions)


def test_meta_hacked_questionnaire_asks_about_account_control_and_identity():
    questions = get_incident_questionnaire("meta_account_hacked")

    assert any(question["id"] == "still_controls_email" for question in questions)
    assert any(question["id"] == "still_controls_phone" for question in questions)
    assert any(question["id"] == "has_photo_id" for question in questions)
    assert all(question["answer_type"] in {"boolean", "single_choice"} for question in questions)


def test_supported_incident_list_exposes_questionnaire_availability():
    incidents = list_supported_incidents()

    assert all(incident["questionnaire_id"] == incident["id"] for incident in incidents)
    assert all(incident["question_count"] >= 5 for incident in incidents)


def test_incident_specific_plan_exposes_questionnaire_contract():
    plan = generate_recovery_plan(
        {
            "service": "Google",
            "incident_id": "gmail_mfa_loss",
            "lost_factor": "authenticator_app",
            "role": "owner",
        }
    )

    assert plan["incident_id"] == "gmail_mfa_loss"
    assert plan["questionnaire"]["incident_id"] == "gmail_mfa_loss"
    assert plan["questionnaire"]["service"] == "Google / Gmail"
    assert plan["questionnaire"]["questions"][0]["id"] == "role"


def test_verified_incident_reports_review_due_date_and_status():
    plan = generate_recovery_plan(
        {
            "service": "Google",
            "incident_id": "gmail_mfa_loss",
            "lost_factor": "authenticator_app",
            "role": "owner",
        }
    )

    assert plan["knowledge_base"]["status"] == "verified"
    assert plan["knowledge_base"]["review_due_at"] == "2026-07-19"
    assert plan["knowledge_base"]["review_cadence_days"] == 30


def test_stale_incident_sets_review_status_and_warning():
    plan = generate_recovery_plan(
        {
            "service": "Instagram",
            "incident_id": "meta_account_hacked",
            "account_state": "locked_suspicious_activity",
            "role": "owner",
        }
    )

    assert plan["knowledge_base"]["status"] == "needs_review"
    assert plan["knowledge_base"]["review_due_at"] == "2026-06-14"
    assert plan["knowledge_base"]["stale"] is True
    assert any("needs review" in warning.lower() for warning in plan["safety_warnings"])


def test_gmail_without_backup_codes_steers_user_to_consistent_recovery_context():
    plan = generate_recovery_plan(
        {
            "service": "Google",
            "incident_id": "gmail_mfa_loss",
            "lost_factor": "authenticator_app",
            "still_knows_password": True,
            "has_backup_codes": False,
            "has_recovery_email": True,
            "has_trusted_device": False,
            "role": "owner",
        }
    )

    assert "recovery page" in plan["next_best_action"].lower()
    assert plan["decision_path_id"] == "google_recovery_context"
    assert any("same device" in item.lower() or "same browser" in item.lower() for item in plan["prepare_now"])
    assert any("same browser" in item.lower() for item in plan["checklist"])
    assert any("too many recovery attempts" in item.lower() for item in plan["what_can_make_this_worse"])
    assert any("recovery form keeps failing" in item.lower() for item in plan["escalate_when"])


def test_meta_business_takeover_flags_linked_assets_and_fast_escalation():
    plan = generate_recovery_plan(
        {
            "service": "Instagram",
            "incident_id": "meta_account_hacked",
            "account_state": "locked_suspicious_activity",
            "still_controls_email": False,
            "still_controls_phone": True,
            "has_photo_id": True,
            "business_account": True,
            "role": "owner",
        }
    )

    assert plan["decision_path_id"] == "business_asset_takeover"
    assert "phone-linked recovery" in plan["next_best_action"].lower()
    assert any("ad account" in item.lower() or "business page" in item.lower() for item in plan["prepare_now"])
    assert any("suspicious sessions" in item.lower() for item in plan["checklist"])
    assert any("linked business assets" in item.lower() for item in plan["escalate_when"])


def test_microsoft_backup_admin_path_is_prioritized_when_available():
    plan = generate_recovery_plan(
        {
            "service": "Microsoft",
            "incident_id": "microsoft_admin_lockout",
            "account_state": "locked_suspicious_activity",
            "has_backup_admin": True,
            "has_billing_access": True,
            "domain_control": True,
            "role": "owner",
        }
    )

    assert plan["decision_path_id"] == "backup_admin_available"
    assert "backup admin" in plan["next_best_action"].lower()
    assert plan["expected_timeline"] == "same day if another admin can still access the tenant"
    assert any("break-glass" in item.lower() for item in plan["escalate_when"])


def test_apple_without_trusted_factors_uses_wait_period_path_and_purchase_evidence():
    plan = generate_recovery_plan(
        {
            "service": "Apple",
            "incident_id": "apple_trusted_device_loss",
            "lost_factor": "phone_number",
            "has_trusted_device": False,
            "has_trusted_phone": False,
            "has_purchase_proof": True,
            "role": "owner",
        }
    )

    assert plan["decision_path_id"] == "account_recovery_wait_period"
    assert "account recovery" in plan["next_best_action"].lower()
    assert any("proof of purchase" in item.lower() for item in plan["prepare_now"])
    assert any("one stable recovery attempt" in item.lower() for item in plan["checklist"])


def test_google_backup_code_path_adds_post_recovery_cleanup_step():
    plan = generate_recovery_plan(
        {
            "service": "Google",
            "incident_id": "gmail_mfa_loss",
            "lost_factor": "authenticator_app",
            "has_backup_codes": True,
            "has_trusted_device": False,
            "role": "owner",
        }
    )

    assert plan["decision_path_id"] == "backup_codes_available"
    assert any("fresh backup codes" in item.lower() for item in plan["checklist"])
    assert "replace the lost authenticator" in plan["support_message"].lower()


def test_unknown_incident_questionnaire_returns_key_error():
    try:
        get_incident_questionnaire("unknown_incident")
    except KeyError as exc:
        assert "unknown_incident" in str(exc)
    else:
        raise AssertionError("Expected KeyError for unknown incident")
