from fastapi import APIRouter

from controllers.embedding.request_body import CreateEmbeddingRequestBody
from controllers.embedding.response_body import CreateEmbeddingResponseBody
from services.embedding import EmbeddingService

router = APIRouter(
  prefix='/embedding', tags=['embedding'], responses={404: {'description': 'Not found'}}
)


@router.post('/embedding')
async def createEmbedding(body: CreateEmbeddingRequestBody) -> CreateEmbeddingResponseBody:
  service = EmbeddingService()
  result = await service.embedding(body.text)
  return CreateEmbeddingResponseBody(result=result)
