from __future__ import annotations

import json
from pathlib import Path


def main() -> int:
    paused = Path(".forge/PAUSED")
    packet = {
        "paused": paused.exists(),
        "pause_reason": paused.read_text().strip() if paused.exists() else None,
        "autonomous_guard_armed": Path(".forge/AIDE_AUTONOMOUS").exists(),
        "best_known_exists": Path("artifacts/checkpoints/BEST_KNOWN.json").exists(),
        "recent_experiments": sorted(str(p) for p in Path("experiments").glob("*.json"))[-10:],
        "instructions": "Review pause reason, last approved incumbent, evaluator integrity, protected-path diffs, and unresolved incidents before resuming.",
    }
    print(json.dumps(packet, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
