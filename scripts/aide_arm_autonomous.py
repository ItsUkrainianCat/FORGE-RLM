from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Arm protected-path checks for an explicitly approved autonomous AIDE run."
    )
    parser.add_argument(
        "--ack", required=True, help="Human acknowledgement string; must be at least 12 characters"
    )
    args = parser.parse_args()
    if len(args.ack.strip()) < 12:
        raise SystemExit("--ack must be at least 12 characters")
    if Path(".forge/PAUSED").exists():
        raise SystemExit("project is paused; do not arm autonomous AIDE")
    Path(".forge").mkdir(exist_ok=True)
    Path(".forge/AIDE_AUTONOMOUS").write_text("armed by explicit human acknowledgement\n")
    print("AIDE autonomous mutation guard armed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
