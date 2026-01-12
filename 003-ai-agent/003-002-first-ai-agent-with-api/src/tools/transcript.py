from helpers.transcript import get_transcript as get_transcript_helper

def get_transcript(url: str, languages: list[str] = ['en']) -> str:
  """
  Get transcription for a youtube video.
  
  :param url: Youtube video URL. Example: `https://www.youtube.com/watch?v=zOFxHmjIhvY`
  :type url: str
  :param languages: List of languages for the transcipt.
  :type languages: list[str]
  :return: Transcription of the Youtube video.
  :rtype: str
  """

  if len(languages):
    languages.append('en')
  
  return get_transcript_helper(url, languages)