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
