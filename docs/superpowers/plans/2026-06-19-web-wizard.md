# Account Recovery Assistant Web Wizard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a tested local web wizard that exposes the existing recovery planner through a mobile-friendly browser flow.

**Architecture:** A standard-library HTTP server serves one static HTML shell plus CSS and JS assets, and exposes JSON endpoints for incidents, questionnaires, and plan generation. The server reuses the existing questionnaire and planner contracts so the web flow stays aligned with the CLI and knowledge base.

**Tech Stack:** Python 3.11 standard library (`http.server`, `json`, `threading` in tests), existing package modules, vanilla HTML/CSS/JavaScript, `pytest`

---

## File Structure

- Create: `src/account_recovery_assistant/web.py` - HTTP server, routing, JSON API, static asset serving
- Create: `src/account_recovery_assistant/static/app.css` - mobile-first styles for the wizard
- Create: `src/account_recovery_assistant/static/app.js` - browser flow for incidents, questionnaire, and plan rendering
- Modify: `src/account_recovery_assistant/__main__.py` - optional CLI entry to launch the web server
- Modify: `src/account_recovery_assistant/__init__.py` - export web server helpers if needed
- Modify: `README.md` - document how to launch the web wizard
- Modify: `docs/current-usage.md` - describe the new web wizard workflow
- Test: `tests/test_web.py` - HTTP endpoint and response contract tests

### Task 1: Web API Contract

**Files:**
- Create: `tests/test_web.py`
- Create: `src/account_recovery_assistant/web.py`

- [ ] **Step 1: Write the failing tests**

```python
import json
import urllib.request

from account_recovery_assistant.web import run_server_in_thread


def test_incidents_endpoint_returns_canonical_incidents():
    with run_server_in_thread() as base_url:
        payload = json.loads(urllib.request.urlopen(f"{base_url}/api/incidents").read().decode("utf-8"))
        assert [item["id"] for item in payload["incidents"]] == [
            "gmail_mfa_loss",
            "apple_trusted_device_loss",
            "meta_account_hacked",
            "microsoft_admin_lockout",
        ]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=src python3 -m pytest tests/test_web.py -v`
Expected: FAIL with `ModuleNotFoundError` or missing `run_server_in_thread`

- [ ] **Step 3: Write minimal implementation**

```python
def run_server_in_thread():
    raise NotImplementedError
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=src python3 -m pytest tests/test_web.py::test_incidents_endpoint_returns_canonical_incidents -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_web.py src/account_recovery_assistant/web.py
git commit -m "feat: add web api contract"
```

### Task 2: Static Wizard UI

**Files:**
- Modify: `tests/test_web.py`
- Modify: `src/account_recovery_assistant/web.py`
- Create: `src/account_recovery_assistant/static/app.css`
- Create: `src/account_recovery_assistant/static/app.js`

- [ ] **Step 1: Write the failing static asset tests**

```python
def test_root_page_serves_wizard_shell():
    with run_server_in_thread() as base_url:
        html = urllib.request.urlopen(f"{base_url}/").read().decode("utf-8")
        assert "Account Recovery Wizard" in html
        assert "/static/app.js" in html
        assert "/static/app.css" in html
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=src python3 -m pytest tests/test_web.py::test_root_page_serves_wizard_shell -v`
Expected: FAIL because the route or asset references do not exist yet

- [ ] **Step 3: Write minimal implementation**

```html
<main id="app">
  <h1>Account Recovery Wizard</h1>
</main>
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=src python3 -m pytest tests/test_web.py::test_root_page_serves_wizard_shell -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_web.py src/account_recovery_assistant/web.py src/account_recovery_assistant/static/app.css src/account_recovery_assistant/static/app.js
git commit -m "feat: add web wizard shell"
```

### Task 3: Planner Submission Flow

**Files:**
- Modify: `tests/test_web.py`
- Modify: `src/account_recovery_assistant/web.py`

- [ ] **Step 1: Write the failing plan submission tests**

```python
def test_plan_endpoint_returns_incident_plan_and_review_status():
    payload = {
        "incident_id": "meta_account_hacked",
        "service": "Instagram",
        "account_state": "locked_suspicious_activity",
        "role": "owner",
    }
    with run_server_in_thread() as base_url:
        request = urllib.request.Request(
            f"{base_url}/api/plan",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        plan = json.loads(urllib.request.urlopen(request).read().decode("utf-8"))
        assert plan["knowledge_base"]["status"] == "needs_review"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=src python3 -m pytest tests/test_web.py::test_plan_endpoint_returns_incident_plan_and_review_status -v`
Expected: FAIL because `POST /api/plan` is not implemented yet

- [ ] **Step 3: Write minimal implementation**

```python
if self.path == "/api/plan":
    plan = generate_recovery_plan(payload)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=src python3 -m pytest tests/test_web.py::test_plan_endpoint_returns_incident_plan_and_review_status -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_web.py src/account_recovery_assistant/web.py
git commit -m "feat: add plan submission endpoint"
```

### Task 4: CLI Entry And Documentation

**Files:**
- Modify: `src/account_recovery_assistant/__main__.py`
- Modify: `README.md`
- Modify: `docs/current-usage.md`
- Modify: `tests/test_cli.py`

- [ ] **Step 1: Write the failing CLI/docs-oriented test**

```python
def test_cli_can_start_web_server_help():
    result = subprocess.run(
        [sys.executable, "-m", "account_recovery_assistant", "--help"],
        check=True,
        capture_output=True,
        text=True,
    )
    assert "--serve-web" in result.stdout
```

- [ ] **Step 2: Run test to verify it fails**

Run: `PYTHONPATH=src python3 -m pytest tests/test_cli.py::test_cli_can_start_web_server_help -v`
Expected: FAIL because the flag does not exist yet

- [ ] **Step 3: Write minimal implementation**

```python
parser.add_argument("--serve-web", action="store_true")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `PYTHONPATH=src python3 -m pytest tests/test_cli.py::test_cli_can_start_web_server_help -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/account_recovery_assistant/__main__.py README.md docs/current-usage.md tests/test_cli.py
git commit -m "feat: document web wizard entrypoint"
```

### Task 5: Full Verification

**Files:**
- Verify: `tests/test_web.py`
- Verify: `tests/test_cli.py`
- Verify: `tests/test_planner.py`
- Verify: `README.md`
- Verify: `docs/current-usage.md`

- [ ] **Step 1: Run focused web and CLI tests**

Run: `PYTHONPATH=src python3 -m pytest tests/test_web.py tests/test_cli.py -v`
Expected: PASS

- [ ] **Step 2: Run the full test suite**

Run: `PYTHONPATH=src python3 -m pytest -v`
Expected: PASS

- [ ] **Step 3: Review docs for launch instructions**

```text
README.md and docs/current-usage.md both show how to start the local web wizard and describe the incident picker -> questionnaire -> plan flow.
```

- [ ] **Step 4: Commit**

```bash
git add tests/test_web.py tests/test_cli.py README.md docs/current-usage.md
git commit -m "feat: ship phase 4 web wizard"
```
