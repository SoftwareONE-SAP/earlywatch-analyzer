import os
from pathlib import Path
from pydantic import BaseModel
import yaml


class DeploymentsConfig(BaseModel):
    orchestrator: str
    specialist: str
    router: str


class AzureConfig(BaseModel):
    endpoint: str
    api_key: str
    api_version: str
    deployments: DeploymentsConfig


class ModelPrice(BaseModel):
    input_per_1m: float = 0.0   # USD per million input tokens
    cached_input_per_1m: float | None = None  # USD per million cached input tokens
    output_per_1m: float = 0.0  # USD per million output tokens


class Config(BaseModel):
    azure_openai: AzureConfig
    pricing: dict[str, ModelPrice] = {}

    def pricing_dict(self) -> dict[str, dict[str, float]]:
        """Return pricing in the flat format CostTracker expects."""
        pricing: dict[str, dict[str, float]] = {}
        for key, value in self.pricing.items():
            entry = {
                "input_per_1m": value.input_per_1m,
                "output_per_1m": value.output_per_1m,
            }
            if value.cached_input_per_1m is not None:
                entry["cached_input_per_1m"] = value.cached_input_per_1m
            pricing[key] = entry
        return pricing


def _first_env(*names: str) -> str:
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value
    return ""


def _build_env_config() -> Config:
    endpoint = _first_env("AZURE_OPENAI_ENDPOINT")
    api_key = _first_env("AZURE_OPENAI_API_KEY")
    api_version = _first_env("AZURE_OPENAI_API_VERSION") or "2025-03-01-preview"

    orchestrator_deployment = _first_env("V2_ORCHESTRATOR_MODEL")
    specialist_deployment = _first_env("V2_SPECIALIST_MODEL")
    router_deployment = _first_env("V2_ROUTER_MODEL")

    missing = []
    if not endpoint:
        missing.append("AZURE_OPENAI_ENDPOINT")
    if not api_key:
        missing.append("AZURE_OPENAI_API_KEY")
    if not orchestrator_deployment:
        missing.append("V2_ORCHESTRATOR_MODEL")
    if not specialist_deployment:
        missing.append("V2_SPECIALIST_MODEL")
    if not router_deployment:
        missing.append("V2_ROUTER_MODEL")

    if missing:
        missing_list = ", ".join(missing)
        raise FileNotFoundError(
            "No config.yaml was found and the pipeline environment is incomplete. "
            f"Missing: {missing_list}."
        )

    return Config.model_validate(
        {
            "azure_openai": {
                "endpoint": endpoint,
                "api_key": api_key,
                "api_version": api_version,
                "deployments": {
                    "orchestrator": orchestrator_deployment,
                    "specialist": specialist_deployment,
                    "router": router_deployment,
                },
            },
            "pricing": {},
        }
    )


def load_config(path: Path | None = None) -> Config:
    if path and path.exists():
        config_path = path
    else:
        # Search order: CWD → backend/ directory (parent of ewa_pipeline/)
        candidates = [
            Path("config.yaml"),
            Path(__file__).resolve().parent.parent / "config.yaml",
        ]
        config_path = next((p for p in candidates if p.exists()), candidates[0])

    if config_path.exists():
        with open(config_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return Config.model_validate(data)

    return _build_env_config()
