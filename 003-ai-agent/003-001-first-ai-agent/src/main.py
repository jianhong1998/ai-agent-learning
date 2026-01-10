import os
from dotenv import load_dotenv
from typing import List
import argparse

from xai_sdk import Client
from xai_sdk.tools import web_search, get_tool_call_type
from xai_sdk.chat import system, user, tool
from xai_sdk.types.chat import chat_pb2

from tools.transcript import get_transcript
from tools.index import execute_tool

load_dotenv()

#################################################################
# Step 1 - Define client
#################################################################
xai_api_key = os.getenv("XAI_API_KEY")
xai_management_api_key = os.getenv("XAI_MANAGEMENT_API_KEY")
client = Client(
  api_key=xai_api_key,
  management_api_key=xai_management_api_key,
  timeout=3600,
)

#################################################################
# Step 2 - Define tools for agents
#################################################################
TOOLS: List[chat_pb2.Tool] = [
  web_search(),
  tool(
    name=get_transcript.__name__,
    description='Get YouTube video transcription.',
    parameters={
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "description": "Full YouTube video URL. Example: https://www.youtube.com/watch?v=zOFxHmjIhvY"
        },
        "languages": {
          "type": "array",
          "items": {
            "type": "string"
          },
          "description": "Preferred language codes for transcription (ISO 639-1). Most common: 'en'. Falls back to auto-detected language if not available. Default: ['en']",
          "default": ["en"]
        }
      },
      "required": ["url"],
      "additionalProperties": False
    }
  )
]

#################################################################
# Step 3 - Define run agent function
#################################################################
def run_agent(video_url: str, max_steps: int = 8):
  system_prompt = system('You are a world class content summarizer. You are given a youtube video transcript, summarize to make it be able to be read finish within 5 minutes.')
  user_prompt = user(f'Summarize this YouTube video: {video_url}')

  chat = client.chat.create(
      model='grok-4-1-fast-non-reasoning',
      messages=[
        system_prompt,
        user_prompt
      ],
      tools=TOOLS,
      tool_choice='auto',
      max_tokens=2048,
      temperature=0.7,
      store_messages=True
    )

  for step in range(1, max_steps + 1):
    print(f'Running step {step}...')

    # Using sample will await for the message to be responsed.
    # Alternative way is using stream.
    res = chat.sample()
    chat.append(res)
    
    message = res.content.strip()
    tool_calls = res.tool_calls
    client_side_tool_calls: list[chat_pb2.ToolCall] = []

    print(f'Message: {message}')

    if not tool_calls:
      print('\n✅ Completed.')
      break

    for tool_call in tool_calls:
      tool_type = get_tool_call_type(tool_call)

      if (tool_type == 'client_side_tool'):
        client_side_tool_calls.append(tool_call)
        continue

      print(f'Calling {tool_call.function.name} from {tool_type} ...')
      print(f'Arguments: {tool_call.function.arguments}')

    if not client_side_tool_calls:
      break

    for tool_call in client_side_tool_calls:
      print(f'Client-side tool call: {tool_call.function.name}')
      print(f'Arguments: {tool_call.function.arguments}')
      tool_message = execute_tool(tool_call)
      chat.append(tool_message)


#################################################################
# Step 4 - Run agent
#################################################################
if __name__ == "__main__":
  # url = 'https://www.youtube.com/watch?v=zOFxHmjIhvY'
  parser = argparse.ArgumentParser(
    description='A Youtube video summarizer.',
  )
  parser.add_argument(
    'url',
    type=str,
    help='Youtube video URL. Example: https://www.youtube.com/watch?v=zOFxHmjIhvY'
  )
  
  args = parser.parse_args()
  url = args.url

  if not url:
    print('URL is needed.')
  else:
    print(f'url: {url}')
    run_agent(url)