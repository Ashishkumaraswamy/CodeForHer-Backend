from functools import cache
from typing import TypeAlias

from langchain_openai import AzureChatOpenAI, ChatOpenAI

from .settings import settings
from codeforher_backend.schema.models import (AllModelEnum, AnthropicModelName, AWSModelName,
                           AzureOpenAIModelName, DeepseekModelName,
                           FakeModelName, GoogleModelName, GroqModelName,
                           OllamaModelName, OpenAIModelName)

_MODEL_TABLE = {
    OpenAIModelName.GPT_4O_MINI: "gpt-4o-mini",
    OpenAIModelName.GPT_4O: "gpt-4o",
    AzureOpenAIModelName.AZURE_GPT_4O_MINI: settings.AZURE_OPENAI_DEPLOYMENT_MAP.get(
        "gpt-4o-mini", ""
    ),
    AzureOpenAIModelName.AZURE_GPT_4O: settings.AZURE_OPENAI_DEPLOYMENT_MAP.get(
        "gpt-4o", ""
    ),
}

ModelT: TypeAlias = (
    ChatOpenAI
)


@cache
def get_model(model_name: AllModelEnum, /) -> ModelT:
    # NOTE: models with streaming=True will send tokens as they are generated
    # if the /stream endpoint is called with stream_tokens=True (the default)
    api_model_name = _MODEL_TABLE.get(model_name)
    print(
        f"api_model_name: {api_model_name} {model_name} {OpenAIModelName} {model_name in AzureOpenAIModelName}"
    )
    if not api_model_name:
        raise ValueError(f"Unsupported model: {model_name}")

    return AzureChatOpenAI(
        api_key="3e33b1a703db4eaf800657cfff73e2db",
        openai_api_version="2024-02-01",
        azure_deployment="dg-llm-service-gpt-4o",
        azure_endpoint="https://dg-llm-service-dev.openai.azure.com/",
        temperature=0.5,
        streaming=True,
        timeout=60,
        max_retries=3,
    )