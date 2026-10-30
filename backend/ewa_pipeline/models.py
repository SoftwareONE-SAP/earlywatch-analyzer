from typing import Any

from langchain_anthropic import ChatAnthropic
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import AzureChatOpenAI
from ewa_pipeline.config import Config, ReasoningEffort


def _model(config: Config, deployment: str, effort: ReasoningEffort,
           timeout_seconds: int | None = None) -> AzureChatOpenAI:
    return AzureChatOpenAI(
        azure_deployment=deployment,
        azure_endpoint=config.azure_openai.endpoint,
        api_key=config.azure_openai.api_key,
        api_version=config.azure_openai.api_version,
        use_responses_api=True,
        reasoning_effort=effort,
        timeout=timeout_seconds if timeout_seconds is not None else config.request_timeout_seconds,
        max_retries=config.max_model_retries,
    )


def _claude_model(config: Config, deployment: str, effort: ReasoningEffort,
                  timeout_seconds: int | None = None) -> ChatAnthropic:
    thinking_off = effort in ("none", "minimal")
    return ChatAnthropic(
        model=deployment,
        base_url=config.claude.endpoint,
        api_key=config.claude.api_key,
        max_tokens=config.claude.max_output_tokens,
        timeout=timeout_seconds if timeout_seconds is not None else config.request_timeout_seconds,
        max_retries=config.max_model_retries,
        thinking={"type": "disabled"} if thinking_off else {"type": "adaptive"},
        effort="low" if thinking_off else effort,
    )


def _build(config: Config, role: str, deployment: str, effort: ReasoningEffort,
           timeout_seconds: int | None = None) -> BaseChatModel:
    build = _claude_model if config.provider_for(role) == "foundry_claude" else _model
    return build(config, deployment, effort, timeout_seconds)


def structured(model: BaseChatModel, schema: Any):
    """Structured output; Claude uses json_schema because forced tool calls clash with thinking."""
    if isinstance(model, ChatAnthropic):
        return model.with_structured_output(schema, include_raw=True, method="json_schema")
    return model.with_structured_output(schema, include_raw=True)


def get_orchestrator_model(config: Config) -> BaseChatModel:
    return _build(config, "orchestrator", config.azure_openai.deployments.orchestrator,
                  config.reasoning.orchestrator, config.planning_timeout_seconds)


def get_subagent_model(config: Config) -> BaseChatModel:
    return _build(config, "specialist", config.azure_openai.deployments.specialist,
                  config.reasoning.deep)


def get_cross_ref_model(config: Config) -> BaseChatModel:
    return _build(config, "cross_reference", *config.model_settings("cross_reference"))


def get_synthesis_model(config: Config) -> BaseChatModel:
    return _build(config, "synthesis", *config.model_settings("synthesis"))
