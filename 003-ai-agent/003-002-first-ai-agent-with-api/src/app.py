from fastapi import FastAPI

from custom_agents.transcript_summarizer import run_agent

#################################################################
# Step 4 - Run agent
#################################################################

app = FastAPI()

@app.get('/transcript')
async def get_summary(url: str):
  print(f'Received Youtube URL: {url}')
  result = run_agent(url)
  return result
