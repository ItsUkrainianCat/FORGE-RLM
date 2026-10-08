from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="FORGE_", extra="ignore")

    model_id: str = "qwen-local"
    api_base: str = "http://127.0.0.1:8080/v1"
    api_key: str = "local"
    sub_model_id: str | None = None
    critic_model_id: str | None = None
    reflection_model_id: str | None = None

    temperature: float = 0.2
    max_tokens: int = 4096
    rlm_max_iters: int = 10
    rlm_max_llm_calls: int = 24
    rlm_max_output_chars: int = 10_000

    genome_path: str = "config/genome.yaml"
    best_known_path: str = "artifacts/checkpoints/BEST_KNOWN.json"
    experiment_dir: str = "experiments"
    trace_dir: str = "artifacts/traces"

    rvf_path: str = "memory/project.rvf"
    ruvector_endpoint: str | None = None
    memory_enabled: bool = False

    holdout_dir: str = ".forge/holdout"
    allow_holdout: bool = False
    mlflow_uri: str | None = None

    aide_config_path: str = "config/aide.yaml"
    aide_pause_sentinel: str = ".forge/PAUSED"
    aide_enabled: bool = True
    aide_allow_ignition: bool = False
    aide_outer_steps: int = 25

    @property
    def root_model(self) -> str:
        return self.model_id

    @property
    def sub_model(self) -> str:
        return self.sub_model_id or self.model_id
