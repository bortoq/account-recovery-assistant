import json
import urllib.request

import pytest

from account_recovery_assistant.web import run_server_in_thread


def _fetch_text(url: str) -> str:
    with urllib.request.urlopen(url, timeout=5) as response:
        return response.read().decode("utf-8")


def test_lightweight_browser_smoke_loads_shell_assets_and_api():
    with run_server_in_thread() as base_url:
        html = _fetch_text(f"{base_url}/")
        js = _fetch_text(f"{base_url}/static/app.js")
        css = _fetch_text(f"{base_url}/static/app.css")
        incidents = json.loads(_fetch_text(f"{base_url}/api/incidents"))

    assert "Account Recovery Wizard" in html
    assert "fetchJson" in js
    assert "renderIncidentPicker" in js
    assert ".plan-section" in css
    assert incidents["incidents"]


def test_playwright_full_wizard_flow_if_installed():
    playwright_api = pytest.importorskip("playwright.sync_api")

    with run_server_in_thread() as base_url:
        with playwright_api.sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch()
            except Exception as exc:  # Browser binaries may not be installed in lightweight local environments.
                pytest.skip(f"Playwright is installed but browser binaries are unavailable: {exc}")

            page = browser.new_page()
            page.goto(base_url)
            page.get_by_role("button", name="Lost MFA device for a Google account").click()
            page.locator('input[name="role"][value="owner"]').check()
            page.locator('input[name="still_knows_password"][value="true"]').check()
            page.locator('input[name="has_backup_codes"][value="true"]').check()
            page.locator('input[name="has_recovery_email"][value="true"]').check()
            page.locator('input[name="has_trusted_device"][value="false"]').check()
            page.get_by_role("button", name="Generate Recovery Plan").click()

            page.get_by_role("heading", name="Next Best Action").wait_for(timeout=5000)
            assert "backup code" in page.text_content("body").lower()
            assert page.get_by_role("button", name="Copy Support Message").is_visible()
            assert page.get_by_role("button", name="Copy Full Plan").is_visible()
            assert page.get_by_role("button", name="Download Markdown").is_visible()
            assert page.get_by_role("button", name="Print Plan").is_visible()
            assert page.locator("#feedback-consent").is_visible()
            assert page.get_by_role("button", name="I recovered access").is_visible()

            browser.close()
