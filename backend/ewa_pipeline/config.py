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


class PageIndexConfig(BaseModel):
    model: str
    max_pages_per_node: int = 10
    max_tokens_per_node: int = 20000
    add_node_summary: bool = True
    add_doc_description: bool = False


class ModelPrice(BaseModel):
    input_per_1m: float = 0.0   # USD per million input tokens
    output_per_1m: float = 0.0  # USD per million output tokens


class Config(BaseModel):
    azure_openai: AzureConfig
    pageindex: PageIndexConfig
    pricing: dict[str, ModelPrice] = {}

    def pricing_dict(self) -> dict[str, dict[str, float]]:
        """Return pricing in the flat format CostTracker expects."""
        return {k: {"input_per_1m": v.input_per_1m, "output_per_1m": v.output_per_1m}
                for k, v in self.pricing.items()}


def _first_env(*names: str) -> str:
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value
    return ""


def _get_bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _get_int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


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

    pageindex_model = _first_env("PAGEINDEX_MODEL") or f"azure/{router_deployment}"

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
            "pageindex": {
                "model": pageindex_model,
                "max_pages_per_node": _get_int_env("PAGEINDEX_MAX_PAGES_PER_NODE", 10),
                "max_tokens_per_node": _get_int_env("PAGEINDEX_MAX_TOKENS_PER_NODE", 20000),
                "add_node_summary": _get_bool_env("PAGEINDEX_ADD_NODE_SUMMARY", True),
                "add_doc_description": _get_bool_env("PAGEINDEX_ADD_DOC_DESCRIPTION", False),
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
