from langchain.messages import ToolCall, ToolMessage

from tools.transcript import get_transcript


def execute_tool(tool_call: ToolCall) -> ToolMessage:
  function_name = tool_call['name']
  tool_call_id = tool_call['id']

  if function_name == get_transcript.name:
    result = get_transcript.invoke(tool_call)  # type: ignore
    return ToolMessage(content=result, tool_call_id=tool_call_id)

  return ToolMessage(content='Tool not found.', tool_call_id=tool_call_id)
