from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py as _build_py


class build_py(_build_py):
    """Copy the top-level knowledge-base data into the built package.

    `data/` is the single source of truth in the repository. The package-local
    JSON files are generated only inside build artifacts.
    """

    def run(self):
        super().run()
        root = Path(__file__).parent
        source = root / "data"
        target = Path(self.build_lib) / "account_recovery_assistant" / "data"
        target.mkdir(parents=True, exist_ok=True)
        for name in ("recovery_playbooks.json", "service_priorities.json"):
            self.copy_file(str(source / name), str(target / name))


setup(cmdclass={"build_py": build_py})
