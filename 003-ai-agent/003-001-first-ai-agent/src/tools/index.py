import json

from xai_sdk.types.chat import chat_pb2
from xai_sdk.chat import tool_result

from tools.transcript import get_transcript

def execute_tool(tool_call: chat_pb2.ToolCall) -> chat_pb2.Message:
  function_name = tool_call.function.name
  args = json.loads(tool_call.function.arguments)
  
  if function_name == get_transcript.__name__:
    url = args.get('url', '')
    languages = args.get('languages', ['en'])
    result = get_transcript(url, languages)
    return tool_result(result)
  
  return tool_result('Tool not found.')