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


def test_optional_playwright_browser_smoke_if_installed():
    playwright_api = pytest.importorskip("playwright.sync_api")

    with run_server_in_thread() as base_url:
        with playwright_api.sync_playwright() as playwright:
            try:
                browser = playwright.chromium.launch()
            except Exception as exc:  # Browser binaries may not be installed in lightweight CI.
                pytest.skip(f"Playwright is installed but browser binaries are unavailable: {exc}")
            page = browser.new_page()
            page.goto(base_url)
            assert "Account Recovery Wizard" in page.text_content("body")
            browser.close()
