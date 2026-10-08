from __future__ import annotations

import json

import httpx

from forge.config import Settings


def main() -> None:
    s = Settings()
    headers = {"Authorization": f"Bearer {s.api_key}"} if s.api_key else {}
    with httpx.Client(timeout=15.0) as client:
        r = client.get(s.api_base.rstrip("/") + "/models", headers=headers)
        print("status:", r.status_code)
        try:
            print(json.dumps(r.json(), indent=2)[:8000])
        except Exception:
            print(r.text[:8000])


if __name__ == "__main__":
    main()
