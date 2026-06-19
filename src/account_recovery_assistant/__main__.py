import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .planner import generate_recovery_plan
from .report import render_markdown


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="account-recovery-assistant",
        description="Generate a safe account recovery plan from a JSON situation file.",
    )
    parser.add_argument("situation", help="Path to a JSON file describing the recovery situation.")
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Output format.",
    )
    args = parser.parse_args(argv)

    situation = _read_json(Path(args.situation))
    plan = generate_recovery_plan(situation)
    if args.format == "markdown":
        sys.stdout.write(render_markdown(plan))
    else:
        json.dump(plan, sys.stdout, indent=2)
        sys.stdout.write("\n")
    return 0


def _read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise SystemExit("Situation JSON must be an object.")
    return data


if __name__ == "__main__":
    raise SystemExit(main())
