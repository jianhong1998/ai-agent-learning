from typing import Literal, cast, get_args

from langchain.messages import AIMessage
from langchain.tools import BaseTool
from langchain_core.language_models import LanguageModelInput
from langchain_core.runnables import Runnable

from custom_agents.agents.ollama import init_model as init_ollamaa
from custom_agents.agents.xai import init_model as init_xai
from http_error.bad_request import BadRequestException

ModelProvider = Literal['xai', 'ollama']


def parse_model_provider(model_provider_str: str) -> ModelProvider:
  VALID_SET = set(get_args(ModelProvider))
  if model_provider_str in VALID_SET:
    return cast(ModelProvider, model_provider_str)
  raise BadRequestException(f'Invalid model provider: {model_provider_str}')


def init_model(
  model_provider: ModelProvider, tools: list[BaseTool]
) -> Runnable[LanguageModelInput, AIMessage] | None:
  if model_provider == 'xai':
    return init_xai(tools)

  if model_provider == 'ollama':
    return init_ollamaa(tools)

  return None
