import argparse
import json
import sys
from pathlib import Path
from typing import Any

from . import __version__
from .planner import generate_recovery_plan
from .validation import ValidationError, validate_situation
from .report import render_markdown
from .web import serve


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="account-recovery-assistant",
        description="Generate a safe account recovery plan from a JSON situation file.",
    )
    parser.add_argument("situation", nargs="?", help="Path to a JSON file describing the recovery situation.")
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Output format.",
    )
    parser.add_argument("--serve-web", action="store_true", help="Start the local web wizard.")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--host", default="127.0.0.1", help="Host for the local web wizard.")
    parser.add_argument("--port", type=int, default=8000, help="Port for the local web wizard.")
    args = parser.parse_args(argv)

    if args.serve_web:
        serve(host=args.host, port=args.port)
        return 0

    if not args.situation:
        raise SystemExit("Situation JSON path is required unless --serve-web is used.")

    situation = _read_json(Path(args.situation))
    try:
        situation = validate_situation(situation)
    except ValidationError as exc:
        raise SystemExit(f"Validation error — {exc.field}: {exc.message}")

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
