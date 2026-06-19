import json
import subprocess
import sys


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
