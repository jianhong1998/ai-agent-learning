import os

from langchain.embeddings import Embeddings
from langchain_postgres import PGVector


def get_vector_store(embedding: Embeddings):
  connection_string = os.environ.get(
    'PG_CONNECTION_STRING', 'postgresql+psycopg://postgres:postgres@localhost:5434/trial_db'
  )

  vector_store = PGVector(
    embeddings=embedding, connection=connection_string, collection_name='test-collection'
  )

  return vector_store
