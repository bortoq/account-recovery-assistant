import json
from pathlib import Path


def test_incident_records_define_review_policy_and_status():
    data = json.loads(Path("data/recovery_playbooks.json").read_text(encoding="utf-8"))

    incident_records = data["incident_records"]

    assert set(incident_records) == {
        "gmail_mfa_loss",
        "apple_trusted_device_loss",
        "meta_account_hacked",
        "microsoft_admin_lockout",
    }

    for incident_id, incident in incident_records.items():
        assert incident["review_cadence_days"] == 30
        assert incident["review_due_at"]
        assert incident["status"] in {"verified", "needs_review", "stale"}
        assert isinstance(incident["stale"], bool)
        assert incident["source_notes"], incident_id

    assert incident_records["meta_account_hacked"]["status"] == "needs_review"
    assert incident_records["meta_account_hacked"]["stale"] is True


def test_incident_records_define_decision_paths_for_canonical_mvp_cases():
    data = json.loads(Path("data/recovery_playbooks.json").read_text(encoding="utf-8"))

    for incident in data["incident_records"].values():
        assert incident["decision_paths"]
        assert incident["default_guidance"]
        assert incident["default_guidance"]["next_best_action"]
        assert incident["default_guidance"]["prepare_now"]

    gmail_paths = data["incident_records"]["gmail_mfa_loss"]["decision_paths"]
    assert any(path["id"] == "backup_codes_available" for path in gmail_paths)

    microsoft_paths = data["incident_records"]["microsoft_admin_lockout"]["decision_paths"]
    assert any(path["id"] == "backup_admin_available" for path in microsoft_paths)
