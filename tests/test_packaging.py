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
