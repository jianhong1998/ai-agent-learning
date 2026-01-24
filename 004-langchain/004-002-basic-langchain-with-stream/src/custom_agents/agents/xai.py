import os

from langchain.messages import AIMessage
from langchain.tools import BaseTool
from langchain_core.language_models import LanguageModelInput
from langchain_core.runnables import Runnable
from langchain_xai import ChatXAI
from pydantic.types import SecretStr


def init_model(tools: list[BaseTool]) -> Runnable[LanguageModelInput, AIMessage]:
  xai_api_key = SecretStr(os.getenv('XAI_API_KEY', ''))

  model = ChatXAI(
    name='transcript_summarizer',
    api_key=xai_api_key,
    model='grok-4-fast-non-reasoning',
    timeout=3600,
    temperature=0.8,
    max_retries=3,
  )
  model_with_tool = model.bind_tools(tools=tools, parallel_tool_calls=False, tool_choice='auto')  # type: ignore

  return model_with_tool
