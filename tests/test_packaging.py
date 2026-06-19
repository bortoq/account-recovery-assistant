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


def test_data_files_have_single_source_of_truth():
    """Ensure data/ is the only tracked JSON source; build_py packages it."""
    top_level = Path("data")
    packaged = Path("src/account_recovery_assistant/data")

    for name in ["recovery_playbooks.json", "service_priorities.json"]:
        assert (top_level / name).exists()
        assert not (packaged / name).exists(), f"Do not track duplicate packaged data file: {name}"


def test_installed_console_script_runs_real_example():
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
        script = Path(target_dir) / "bin" / "account-recovery-assistant"
        result = subprocess.run(
            [str(script), "examples/lost_mfa.json"],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )

    plan = json.loads(result.stdout)
    assert plan["allowed"] is True
    assert plan["incident_id"] == "gmail_mfa_loss"


def test_deployment_skeleton_uses_non_root_docker_and_reverse_proxy_docs():
    dockerfile = Path("Dockerfile").read_text(encoding="utf-8")
    deployment_doc = Path("docs/deployment.md").read_text(encoding="utf-8")
    nginx_conf = Path("deploy/nginx.conf").read_text(encoding="utf-8")

    assert "USER app" in dockerfile
    assert "HEALTHCHECK" in dockerfile
    assert "deploy/nginx.conf" in deployment_doc
    assert "limit_req_zone" in nginx_conf
    assert "client_max_body_size" in nginx_conf


def test_release_candidate_document_exists():
    rc = Path("docs/release-candidate-v0.1.0-rc.1.md")

    assert rc.exists()
    assert "v0.1.0-rc.1" in rc.read_text(encoding="utf-8")


def test_production_deployment_docs_include_monitoring_privacy_and_compose():
    assert Path("deploy/docker-compose.yml").exists()
    assert Path("docs/monitoring.md").exists()
    assert Path("docs/production-privacy-template.md").exists()

    compose = Path("deploy/docker-compose.yml").read_text(encoding="utf-8")
    monitoring = Path("docs/monitoring.md").read_text(encoding="utf-8")
    privacy = Path("docs/production-privacy-template.md").read_text(encoding="utf-8")

    assert "read_only: true" in compose
    assert "no-new-privileges" in compose
    assert "/healthz" in monitoring
    assert "Request bodies" in privacy
