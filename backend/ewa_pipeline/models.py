from langchain_openai import AzureChatOpenAI
from ewa_pipeline.config import Config


def get_orchestrator_model(config: Config) -> AzureChatOpenAI:
    return AzureChatOpenAI(
        azure_deployment=config.azure_openai.deployments.orchestrator,
        azure_endpoint=config.azure_openai.endpoint,
        api_key=config.azure_openai.api_key,
        api_version=config.azure_openai.api_version,
        use_responses_api=True,
        reasoning_effort=config.reasoning.orchestrator,
        temperature=0.1,
        max_retries=6,
    )


def get_subagent_model(config: Config) -> AzureChatOpenAI:
    return AzureChatOpenAI(
        azure_deployment=config.azure_openai.deployments.specialist,
        azure_endpoint=config.azure_openai.endpoint,
        api_key=config.azure_openai.api_key,
        api_version=config.azure_openai.api_version,
        use_responses_api=True,
        reasoning_effort=config.reasoning.deep,
        temperature=0.1,
        max_retries=6,
    )


def get_cross_ref_model(config: Config) -> AzureChatOpenAI:
    return AzureChatOpenAI(
        azure_deployment=config.azure_openai.deployments.orchestrator,
        azure_endpoint=config.azure_openai.endpoint,
        api_key=config.azure_openai.api_key,
        api_version=config.azure_openai.api_version,
        use_responses_api=True,
        reasoning_effort=config.reasoning.orchestrator,
        temperature=0.1,
        max_retries=6,
    )


def get_indexer_model_name(config: Config) -> str:
    return f"azure/{config.azure_openai.deployments.router}"
