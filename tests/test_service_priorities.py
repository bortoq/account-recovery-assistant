import json
from pathlib import Path


def test_service_priorities_include_top_ten_with_official_links():
    data = json.loads(Path("data/service_priorities.json").read_text(encoding="utf-8"))

    services = data["top_services"]

    assert len(services) == 10
    assert [service["priority"] for service in services] == list(range(1, 11))
    assert services[0]["service"] == "Google / Gmail"
    assert services[-1]["service"] == "Telegram"

    for service in services:
        assert service["aliases"]
        assert service["official_links"]
        assert all(link["url"].startswith("https://") for link in service["official_links"])


def test_x_links_are_marked_for_manual_review_due_to_bot_protection():
    data = json.loads(Path("data/service_priorities.json").read_text(encoding="utf-8"))
    x_service = next(service for service in data["top_services"] if service["service"] == "X / Twitter")

    assert x_service["manual_review_required"] is True
    assert "bot protection" in x_service["manual_review_reason"].lower()
    assert all(link["review_status"] == "manual_review_required" for link in x_service["official_links"])
