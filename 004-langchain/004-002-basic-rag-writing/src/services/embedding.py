from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from agents.embedding import create_agent
from db.connection import get_vector_store


class EmbeddingService:
  def __init__(self) -> None:
    pass

  async def embedding(self, original_text: str):
    agent = create_agent()
    vector_store = get_vector_store(agent)
    text_splitter = RecursiveCharacterTextSplitter(
      separators=['\n\n', '\n', '.', ' ', ''], chunk_size=800, chunk_overlap=120
    )

    raw_documents = [Document(page_content=original_text)]
    splitted_docs = text_splitter.split_documents(documents=raw_documents)

    return vector_store.add_documents(documents=splitted_docs)

  async def retrive(self, query: str):
    agent = create_agent()
    agent.embed_query(query)
