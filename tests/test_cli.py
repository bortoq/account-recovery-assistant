import json
import os
import subprocess
import sys
from pathlib import Path


SRC_DIR = os.path.join(os.path.dirname(__file__), "..", "src")


def _env_with_pythonpath() -> dict[str, str]:
    env = os.environ.copy()
    env.setdefault("PYTHONPATH", SRC_DIR)
    if SRC_DIR not in env["PYTHONPATH"].split(":"):
        env["PYTHONPATH"] = f"{SRC_DIR}:{env['PYTHONPATH']}"
    return env


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
        env=_env_with_pythonpath(),
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
        env=_env_with_pythonpath(),
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
        env=_env_with_pythonpath(),
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


def test_cli_examples_cover_meta_and_microsoft_branches():
    scenarios = [
        ("examples/meta_business_takeover.json", "business_asset_takeover"),
        ("examples/meta_identity_review.json", "identity_review_path"),
        ("examples/microsoft_backup_admin.json", "backup_admin_available"),
        ("examples/microsoft_domain_support.json", "tenant_support_path"),
    ]

    for path, expected_branch in scenarios:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "account_recovery_assistant",
                path,
            ],
            check=True,
            capture_output=True,
            text=True,
            env=_env_with_pythonpath(),
        )

        plan = json.loads(result.stdout)
        assert plan["decision_path_id"] == expected_branch, path


def test_cli_all_example_files_are_valid_inputs():
    for example_path in sorted(Path("examples").glob("*.json")):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "account_recovery_assistant",
                str(example_path),
            ],
            check=True,
            capture_output=True,
            text=True,
            env=_env_with_pythonpath(),
        )

        plan = json.loads(result.stdout)
        assert plan["allowed"] is True, example_path
        assert plan["next_best_action"], example_path
