from langchain.embeddings import Embeddings
from langchain_ollama.embeddings import OllamaEmbeddings


def create_agent(base_url: str = 'http://localhost:11434') -> Embeddings:
  model = OllamaEmbeddings(model='nomic-embed-text', base_url=base_url)
  return model
