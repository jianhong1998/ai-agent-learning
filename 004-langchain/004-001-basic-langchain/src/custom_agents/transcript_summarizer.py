from langchain.messages import AIMessage, AnyMessage, HumanMessage, SystemMessage
from langchain_core.language_models import LanguageModelInput
from langchain_core.runnables import Runnable

from custom_agents.agents.index import ModelProvider, init_model as init_model_helper
from tools.index import execute_tool
from tools.transcript import get_transcript


def init_model(model_provider: ModelProvider) -> Runnable[LanguageModelInput, AIMessage]:
  TOOLS = [get_transcript]

  model = init_model_helper(model_provider, TOOLS)

  if not model:
    raise Exception('Invalid model')

  return model


class RunAgent:
  def __init__(self, summaried_transcript: str, total_token: int) -> None:
    self.total_token = total_token
    self.summarised_transcript = summaried_transcript


def run_agent(video_url: str, model_provider: ModelProvider, max_steps: int = 8):
  model = init_model(model_provider)

  system_prompt = SystemMessage(
    'You are a world class content summarizer. You are given a youtube video transcript, summarize to make it be able to be read finish within 5 minutes. Output with only the summay.'
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
    current_token_usage = (
      res.usage_metadata['total_tokens'] if res.usage_metadata is not None else 0
    )

    print(f'Message length for step {step}: {len(message)}')  # type: ignore
    print(f'Tool calls for step {step}: {tool_calls}')
    print(f'Token for step {step}: {current_token_usage}')

    token += current_token_usage

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
