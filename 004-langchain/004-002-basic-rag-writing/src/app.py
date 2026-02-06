from fastapi import FastAPI

from controllers.index import embedding_router

app = FastAPI()
app.include_router(embedding_router)
