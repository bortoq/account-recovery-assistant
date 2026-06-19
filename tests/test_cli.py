import json
import subprocess
import sys


def test_cli_can_start_web_server_help():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "account_recovery_assistant",
            "--help",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "--serve-web" in result.stdout


def test_cli_prints_recovery_plan_for_lost_mfa_example():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "account_recovery_assistant",
            "examples/lost_mfa.json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    plan = json.loads(result.stdout)

    assert plan["allowed"] is True
    assert plan["case_type"] == "lost_mfa_device"
    assert plan["service"] == "Google"
    assert any("backup codes" in item.lower() for item in plan["checklist"])


def test_cli_prints_markdown_report_when_requested():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "account_recovery_assistant",
            "--format",
            "markdown",
            "examples/lost_mfa.json",
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout.startswith("# Account Recovery Plan")
    assert "## Next Best Action" in result.stdout
    assert "## Prepare Now" in result.stdout
    assert "## What Can Make This Worse" in result.stdout
    assert "## Escalate When" in result.stdout
    assert "Expected timeline:" in result.stdout
    assert "## Checklist" in result.stdout
    assert "- Try backup codes" in result.stdout
    assert "Google Account Recovery" in result.stdout
    assert "## Knowledge Freshness" in result.stdout
    assert "- Review due: 2026-07-19" in result.stdout
    assert "- Status: verified" in result.stdout
    assert "## Common Mistakes To Avoid" in result.stdout
    assert "## Source Notes" in result.stdout
