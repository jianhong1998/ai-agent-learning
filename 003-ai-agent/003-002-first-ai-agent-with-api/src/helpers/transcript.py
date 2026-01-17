from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi


def get_transcript(url: str, languages: list[str] = ['en']) -> str:
  url_queries = parse_qs(urlparse(url).query)
  video_id = url_queries.get('v', [''])[0]

  print(f'Video ID: {video_id}\nLanguages: {languages}')

  api = YouTubeTranscriptApi()

  res = api.fetch(video_id, languages)
  contents = res.snippets

  return ' '.join(content.text for content in contents)
