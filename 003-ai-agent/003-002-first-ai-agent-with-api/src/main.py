from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
  import uvicorn

  uvicorn.run(
    # To enable reload or worker, the `app` must be string
    app='app:app',
    host='0.0.0.0',
    port=3001,
    reload=True,
  )
