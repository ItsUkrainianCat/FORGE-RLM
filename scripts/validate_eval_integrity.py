from __future__ import annotations

import hashlib
import json
from pathlib import Path

TRACKED = [
    Path("evals/train/cases.jsonl"),
    Path("evals/dev/cases.jsonl"),
    Path("evals/regression/cases.jsonl"),
    Path("evals/adversarial/cases.jsonl"),
]


def main() -> None:
    seen: set[str] = set()
    manifest: dict[str, dict] = {}
    for path in TRACKED:
        if not path.exists():
            raise SystemExit(f"missing eval file: {path}")
        rows = [json.loads(x) for x in path.read_text().splitlines() if x.strip()]
        for row in rows:
            cid = row["id"]
            if cid in seen:
                raise SystemExit(f"duplicate eval id: {cid}")
            seen.add(cid)
            if "grader" not in row:
                raise SystemExit(f"missing grader: {cid}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        manifest[str(path)] = {"sha256": digest, "cases": len(rows)}
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
