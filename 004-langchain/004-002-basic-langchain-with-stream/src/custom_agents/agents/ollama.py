from langchain.messages import AIMessage
from langchain.tools import BaseTool
from langchain_core.language_models import LanguageModelInput
from langchain_core.runnables import Runnable
from langchain_ollama import ChatOllama


def init_model(tools: list[BaseTool]) -> Runnable[LanguageModelInput, AIMessage]:
  model = ChatOllama(model='qwen3:4b', base_url='http://localhost:11434', temperature=0.5)

  model_with_tool = model.bind_tools(tools=tools, tool_choice='auto')  # type: ignore

  return model_with_tool
