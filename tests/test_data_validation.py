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


def test_sync_packaged_data_script_runs_and_preserves_validation():
    result = subprocess.run(
        [sys.executable, "scripts/sync_packaged_data.py"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Synced data/recovery_playbooks.json" in result.stdout
