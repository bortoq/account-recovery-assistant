import json
import os
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path


def test_pyproject_has_pypi_ready_metadata_and_console_script():
    data = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    project = data["project"]

    assert project["readme"] == "README.md"
    assert project["keywords"]
    assert project["classifiers"]
    assert project["urls"]["Homepage"]
    assert project["urls"]["Repository"]
    assert project["scripts"]["account-recovery-assistant"] == "account_recovery_assistant.__main__:main"


def test_release_docs_exist_for_first_public_package():
    assert Path("CHANGELOG.md").exists()
    assert Path("docs/releasing.md").exists()


def test_package_installs_into_target_and_can_load_packaged_json_data():
    with tempfile.TemporaryDirectory() as target_dir:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--no-build-isolation",
                "--no-deps",
                "--target",
                target_dir,
                ".",
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        env = os.environ.copy()
        env["PYTHONPATH"] = target_dir
        command = (
            "from account_recovery_assistant import generate_recovery_plan; "
            "import json; "
            "plan = generate_recovery_plan({'service': 'Google', 'lost_factor': 'authenticator_app', 'role': 'owner'}); "
            "print(json.dumps({'allowed': plan['allowed'], 'case_type': plan['case_type']}))"
        )
        result = subprocess.run(
            [sys.executable, "-c", command],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )

    payload = json.loads(result.stdout)
    assert payload == {"allowed": True, "case_type": "lost_mfa_device"}
