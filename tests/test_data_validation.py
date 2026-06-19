import subprocess
import sys
from pathlib import Path


def test_validate_data_script_passes():
    result = subprocess.run(
        [sys.executable, "scripts/validate_data.py"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Data validation passed." in result.stdout


def test_schema_files_exist_for_knowledge_base_contracts():
    assert Path("schemas/recovery_playbooks.schema.json").exists()
    assert Path("schemas/service_priorities.schema.json").exists()


def test_check_data_source_script_confirms_single_source_of_truth():
    result = subprocess.run(
        [sys.executable, "scripts/check_data_source.py"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Data source of truth is data/." in result.stdout


def test_packaged_json_files_are_not_tracked_in_source_tree():
    packaged = Path("src/account_recovery_assistant/data")

    assert not (packaged / "recovery_playbooks.json").exists()
    assert not (packaged / "service_priorities.json").exists()
