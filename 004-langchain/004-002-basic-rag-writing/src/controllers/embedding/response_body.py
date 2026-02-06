from pydantic import BaseModel


class CreateEmbeddingResponseBody(BaseModel):
  result: list[str]
