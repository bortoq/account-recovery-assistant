import json

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
    }

    response = dispatch_request("POST", "/api/plan", body=json.dumps(payload).encode("utf-8"))
    plan = json.loads(response["body"].decode("utf-8"))

    assert plan["incident_id"] == "meta_account_hacked"
    assert plan["knowledge_base"]["status"] == "needs_review"
    assert "hacked-account flow" in plan["next_best_action"].lower()
    assert "expected_timeline" in plan
    assert any("needs review" in warning.lower() for warning in plan["safety_warnings"])
