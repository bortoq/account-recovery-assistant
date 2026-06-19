import json
from pathlib import Path

from account_recovery_assistant.web import dispatch_request


def test_incidents_endpoint_returns_canonical_incidents():
    response = dispatch_request("GET", "/api/incidents")
    payload = json.loads(response["body"].decode("utf-8"))

    assert [item["id"] for item in payload["incidents"]] == [
        "gmail_mfa_loss",
        "apple_trusted_device_loss",
        "meta_account_hacked",
        "microsoft_admin_lockout",
    ]


def test_questionnaire_endpoint_returns_normalized_questions():
    response = dispatch_request("GET", "/api/incidents/gmail_mfa_loss/questionnaire")
    payload = json.loads(response["body"].decode("utf-8"))

    assert payload["incident_id"] == "gmail_mfa_loss"
    assert payload["questions"][0]["id"] == "role"
    assert payload["questions"][0]["answer_type"] == "single_choice"


def test_unknown_questionnaire_returns_json_404():
    response = dispatch_request("GET", "/api/incidents/nope/questionnaire")
    payload = json.loads(response["body"].decode("utf-8"))

    assert response["status"] == 404
    assert payload["error"] == "Unknown incident"


def test_root_page_serves_wizard_shell():
    response = dispatch_request("GET", "/")
    html = response["body"].decode("utf-8")

    assert "Account Recovery Wizard" in html
    assert "/static/app.js" in html
    assert "/static/app.css" in html


def test_plan_endpoint_returns_incident_plan_and_review_status():
    payload = {
        "incident_id": "meta_account_hacked",
        "service": "Instagram",
        "account_state": "locked_suspicious_activity",
        "role": "owner",
        "still_controls_email": False,
        "still_controls_phone": True,
        "has_photo_id": True,
        "business_account": False,
    }

    response = dispatch_request("POST", "/api/plan", body=json.dumps(payload).encode("utf-8"))
    plan = json.loads(response["body"].decode("utf-8"))

    assert plan["incident_id"] == "meta_account_hacked"
    assert plan["knowledge_base"]["status"] == "needs_review"
    assert "hacked-account flow" in plan["next_best_action"].lower()
    assert "expected_timeline" in plan
    assert any("needs review" in warning.lower() for warning in plan["safety_warnings"])


def test_plan_endpoint_uses_incident_case_type_when_incident_id_is_explicit():
    payload = {
        "incident_id": "microsoft_admin_lockout",
        "service": "Microsoft",
        "role": "owner",
        "account_scope": "tenant",
        "has_backup_admin": False,
        "has_billing_access": False,
        "domain_control": True,
        "still_knows_password": False,
    }

    response = dispatch_request("POST", "/api/plan", body=json.dumps(payload).encode("utf-8"))
    plan = json.loads(response["body"].decode("utf-8"))

    assert plan["case_type"] == "suspicious_activity_lock"


def test_plan_endpoint_returns_json_400_for_invalid_json():
    response = dispatch_request("POST", "/api/plan", body=b"{not json")
    payload = json.loads(response["body"].decode("utf-8"))

    assert response["status"] == 400
    assert payload["error"] == "Invalid JSON"


def test_plan_endpoint_returns_json_400_for_missing_required_fields():
    response = dispatch_request(
        "POST",
        "/api/plan",
        body=json.dumps({"incident_id": "gmail_mfa_loss", "service": "Google"}).encode("utf-8"),
    )
    payload = json.loads(response["body"].decode("utf-8"))

    assert response["status"] == 400
    assert payload["error"] == "Validation error"
    assert payload["field"] == "role"


def test_static_app_exposes_markdown_export_and_local_feedback_controls():
    app_js = Path("src/account_recovery_assistant/static/app.js").read_text(encoding="utf-8")

    assert "Download Markdown" in app_js
    assert "Copy Support Message" in app_js
    assert "Copy Full Plan" in app_js
    assert "Print Plan" in app_js
    assert "## Knowledge Freshness" in app_js
    assert "## Common Mistakes To Avoid" in app_js
    assert "## Source Notes" in app_js
    assert "Decision path:" in app_js
    assert "feedback-recovered" in app_js
    assert "feedback-stuck" in app_js
    assert "feedback-link-worked" in app_js
    assert "feedback-link-failed" in app_js


def test_markdown_endpoint_returns_backend_report():
    payload = {
        "incident_id": "gmail_mfa_loss",
        "service": "Google",
        "role": "owner",
        "still_knows_password": True,
        "has_backup_codes": True,
        "has_recovery_email": True,
        "has_trusted_device": False,
    }

    response = dispatch_request("POST", "/api/plan/markdown", body=json.dumps(payload).encode("utf-8"))
    markdown = response["body"].decode("utf-8")

    assert response["status"] == 200
    assert response["headers"]["Content-Type"] == "text/markdown; charset=utf-8"
    assert markdown.startswith("# Account Recovery Plan")
    assert "## Knowledge Freshness" in markdown
    assert "## Source Notes" in markdown


def test_feedback_endpoint_requires_consent_and_accepts_minimal_feedback():
    without_consent = dispatch_request(
        "POST",
        "/api/feedback",
        body=json.dumps({"outcome": "recovered", "link_status": "worked"}).encode("utf-8"),
    )
    assert without_consent["status"] == 400

    accepted = dispatch_request(
        "POST",
        "/api/feedback",
        body=json.dumps(
            {
                "consent": True,
                "incident_id": "gmail_mfa_loss",
                "decision_path_id": "backup_codes_available",
                "outcome": "recovered",
                "link_status": "worked",
            }
        ).encode("utf-8"),
    )
    payload = json.loads(accepted["body"].decode("utf-8"))

    assert accepted["status"] == 200
    assert payload["accepted"] is True
    assert payload["stored"] == "memory_only"


def test_healthz_endpoint_returns_safe_operational_status():
    response = dispatch_request("GET", "/healthz")
    payload = json.loads(response["body"].decode("utf-8"))

    assert response["status"] == 200
    assert payload["status"] == "ok"
    assert payload["incidents"] >= 4
    assert "feedback_events" in payload


def test_unknown_post_path_returns_404_before_json_parse():
    response = dispatch_request("POST", "/nope")
    payload = json.loads(response["body"].decode("utf-8"))

    assert response["status"] == 404
    assert payload["error"] == "Not found"


def test_feedback_endpoint_records_timestamp_consent_and_caps_memory_store():
    from account_recovery_assistant import web

    web.FEEDBACK_EVENTS.clear()
    web.RATE_LIMIT_EVENTS.clear()
    for index in range(web.FEEDBACK_MAX_EVENTS + 2):
        response = dispatch_request(
            "POST",
            "/api/feedback",
            body=json.dumps(
                {
                    "consent": True,
                    "incident_id": "gmail_mfa_loss",
                    "decision_path_id": f"path-{index}",
                    "outcome": "recovered",
                    "link_status": "worked",
                }
            ).encode("utf-8"),
        )
        assert response["status"] == 200

    payload = json.loads(response["body"].decode("utf-8"))
    assert payload["count"] == web.FEEDBACK_MAX_EVENTS
    assert payload["max_events"] == web.FEEDBACK_MAX_EVENTS
    assert len(web.FEEDBACK_EVENTS) == web.FEEDBACK_MAX_EVENTS
    assert web.FEEDBACK_EVENTS[-1]["consent"] is True
    assert web.FEEDBACK_EVENTS[-1]["timestamp"]
    assert web.FEEDBACK_EVENTS[0]["decision_path_id"] == "path-2"
    web.FEEDBACK_EVENTS.clear()
    web.RATE_LIMIT_EVENTS.clear()


def test_plan_endpoint_rejects_non_object_json_payload():
    response = dispatch_request("POST", "/api/plan", body=b"[]")
    payload = json.loads(response["body"].decode("utf-8"))

    assert response["status"] == 400
    assert payload["error"] == "Validation error"
    assert "object" in payload["detail"]


def test_plan_endpoint_rejects_wrong_boolean_type():
    response = dispatch_request(
        "POST",
        "/api/plan",
        body=json.dumps(
            {
                "incident_id": "gmail_mfa_loss",
                "service": "Google",
                "role": "owner",
                "still_knows_password": "yes",
                "has_backup_codes": False,
                "has_recovery_email": True,
                "has_trusted_device": False,
            }
        ).encode("utf-8"),
    )
    payload = json.loads(response["body"].decode("utf-8"))

    assert response["status"] == 400
    assert payload["field"] == "still_knows_password"


def test_feedback_endpoint_rejects_unsupported_link_status():
    response = dispatch_request(
        "POST",
        "/api/feedback",
        body=json.dumps({"consent": True, "outcome": "recovered", "link_status": "maybe"}).encode("utf-8"),
    )
    payload = json.loads(response["body"].decode("utf-8"))

    assert response["status"] == 400
    assert payload["field"] == "link_status"


def test_rate_limit_returns_429_when_limit_is_exceeded(monkeypatch):
    from account_recovery_assistant import web

    web.RATE_LIMIT_EVENTS.clear()
    monkeypatch.setattr(web, "RATE_LIMIT_MAX_REQUESTS", 1)
    payload = json.dumps({"consent": True, "outcome": "recovered", "link_status": "worked"}).encode("utf-8")

    first = dispatch_request("POST", "/api/feedback", body=payload)
    second = dispatch_request("POST", "/api/feedback", body=payload)
    second_payload = json.loads(second["body"].decode("utf-8"))

    assert first["status"] == 200
    assert second["status"] == 429
    assert second_payload["error"] == "Rate limit exceeded"
    web.RATE_LIMIT_EVENTS.clear()
