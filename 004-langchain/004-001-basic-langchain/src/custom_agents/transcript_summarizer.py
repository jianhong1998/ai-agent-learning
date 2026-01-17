import os

from langchain.messages import AIMessage, AnyMessage, HumanMessage, SystemMessage
from langchain_core.language_models import LanguageModelInput
from langchain_core.runnables import Runnable
from langchain_xai import ChatXAI
from pydantic.types import SecretStr

from tools.index import execute_tool
from tools.transcript import get_transcript


def init_model() -> Runnable[LanguageModelInput, AIMessage]:
  #################################################################
  # Step 1 - Define tools for agents
  #################################################################

  TOOLS = [get_transcript]

  #################################################################
  # Step 2 - Define model client
  #################################################################
  xai_api_key = SecretStr(os.getenv('XAI_API_KEY', ''))

  model = ChatXAI(
    name='transcript_summarizer',
    api_key=xai_api_key,
    model='grok-4-fast-non-reasoning',
    timeout=3600,
    temperature=0.8,
    max_retries=3,
  )
  model_with_tool = model.bind_tools(tools=TOOLS, parallel_tool_calls=False, tool_choice='auto')  # type: ignore

  return model_with_tool


class RunAgent:
  def __init__(self, summaried_transcript: str, total_token: int) -> None:
    self.summarised_transcript = summaried_transcript
    self.total_token = total_token


def run_agent(video_url: str, max_steps: int = 8):
  model = init_model()

  system_prompt = SystemMessage(
    'You are a world class content summarizer. You are given a youtube video transcript, summarize to make it be able to be read finish within 5 minutes.'
  )
  user_prompt = HumanMessage(f'Summarize this YouTube video: {video_url}')

  result: str = ''

  messages: list[AnyMessage] = [system_prompt, user_prompt]
  token: int = 0

  for step in range(1, max_steps + 1):
    print(f'Running step {step}...')

    res = model.invoke(input=messages)

    # Ignoring type because the model output can be str, list[str] or list[dict]
    # In current implementation, no specific format we want to get from LLM, so expected output to be str
    message = res.content  # type: ignore
    tool_calls = res.tool_calls

    print(f'Message length for step {step}: {len(message)}')  # type: ignore
    print(f'Tool calls for step {step}: {tool_calls}')
    print(f'Token for step {step}: {res.usage_metadata}')

    token += res.usage_metadata['total_tokens'] if res.usage_metadata is not None else 0

    if len(message) >= 1:  # type: ignore
      messages.append(AIMessage(content=message))

    if not tool_calls:
      print('\n ✅ Completed.')
      # Ignoring type because the model output can be str, list[str] or list[dict]
      # In current implementation, no specific format we want to get from LLM, so expected output to be str
      result = message  # type: ignore
      break

    for tool_call in tool_calls:
      tool_message = execute_tool(tool_call)
      messages.append(tool_message)

  return RunAgent(result, total_token=token)
