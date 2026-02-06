from enum import StrEnum
import os

from langchain.agents import create_agent as create_langchain_agent
from langchain.tools import BaseTool
from langchain_xai import ChatXAI
from pydantic import SecretStr


# XAI_MODEL = Literal['grok-4-fast-reasoning', 'grok-4-fast-non-reasoning']
class XAI_MODEL(StrEnum):
  reasoning = 'grok-4-fast-reasoning'
  non_reasoning = 'grok-4-fast-non-reasoning'


class XAIEmbedding(OpenAIEmbeddings):
  def __init__(self) -> None:
    super().__init__()


def create_agent(model: XAI_MODEL, agent_name: str | None = None, tools: list[BaseTool] = []):
  api_key = SecretStr(os.environ.get('XAI_API_KEY', ''))

  agent_model = ChatXAI(
    api_key=(api_key), model=model, timeout=3600, temperature=0.8, max_retries=3
  )
  return create_langchain_agent(model=agent_model, tools=tools, name=agent_name)
