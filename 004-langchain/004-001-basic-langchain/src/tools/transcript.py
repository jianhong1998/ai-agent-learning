from langchain.tools import tool  # type: ignore
from pydantic import BaseModel, Field

from helpers.transcript import get_transcript as get_transcript_helper


class GetTranscriptInput(BaseModel):
  """
  Input for get transcript from YouTube.
  """

  url: str = Field(
    description='YouTube video URL', examples=['https://www.youtube.com/watch?v=zOFxHmjIhvY']
  )
  languages: list[str] = Field(description='List of languages for the transcipt.', default=['en'])


@tool(args_schema=GetTranscriptInput)
def get_transcript(url: str, languages: list[str] = ['en']) -> str:
  """
  Get transcription for a youtube video.
  """

  if len(languages) == 0:
    languages.append('en')

  return get_transcript_helper(url, languages)
