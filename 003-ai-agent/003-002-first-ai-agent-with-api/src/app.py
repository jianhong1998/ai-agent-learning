from urllib.parse import SplitResult, parse_qs, urlsplit

from fastapi import FastAPI, Query

from custom_agents.transcript_summarizer import run_agent
from http_error.bad_request import BadRequestException

#################################################################
# Step 4 - Run agent
#################################################################

app = FastAPI()


@app.get('/transcript')
async def get_summary(
  url: str = Query(
    default='', description='Youtube URL', example='https://www.youtube.com/watch?v=K5KVEU3aaeQ'
  ),
):
  print(f'Received Youtube URL: {url}')

  url_obj: SplitResult = urlsplit(url)
  host = url_obj.hostname
  paths = list(filter(lambda x: x.strip(), url_obj.path.split('/')))
  queries = parse_qs(url_obj.query)

  if host != 'youtube.com' and host != 'www.youtube.com':
    raise BadRequestException(f'Invalid YouTube URL: {url}')

  if len(paths) < 1 or paths[0] != 'watch':
    raise BadRequestException(
      f"Invalid YouTube URL. Path ('/{'/'.join(paths)}') should be '/watch'"
    )

  video_id_list = queries.get('v', [])

  if len(video_id_list) != 1:
    raise BadRequestException(f"Invalid YouTube URL. Query 'v' must be only 1 ID: {url}")

  result = run_agent(url)
  return result
