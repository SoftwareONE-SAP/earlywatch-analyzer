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


def get_orchestrator_model(config: Config) -> AzureChatOpenAI:
    return _model(config, config.azure_openai.deployments.orchestrator,
                  config.reasoning.orchestrator, config.planning_timeout_seconds)


def get_subagent_model(config: Config) -> AzureChatOpenAI:
    return _model(config, config.azure_openai.deployments.specialist, config.reasoning.deep)


def get_cross_ref_model(config: Config) -> AzureChatOpenAI:
    return _model(config, *config.model_settings("cross_reference"))


def get_synthesis_model(config: Config) -> AzureChatOpenAI:
    return _model(config, *config.model_settings("synthesis"))
