from __future__ import annotations

import json
from pathlib import Path

import yaml

from forge.genome.schema import CognitiveGenome


class GenomeStore:
    def load(self, path: str | Path) -> CognitiveGenome:
        path = Path(path)
        if path.suffix in {".yaml", ".yml"}:
            data = yaml.safe_load(path.read_text())
        else:
            data = json.loads(path.read_text())
        return CognitiveGenome.model_validate(data)

    def save(self, genome: CognitiveGenome, path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        data = genome.model_dump(mode="json")
        if path.suffix in {".yaml", ".yml"}:
            path.write_text(yaml.safe_dump(data, sort_keys=False))
        else:
            path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        return path
