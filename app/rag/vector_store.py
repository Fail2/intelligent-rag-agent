from langchain_chroma import Chroma

from app.core.config import settings
from app.rag.embeddings import get_embeddings
from langchain_core.documents import Document



def get_vector_store() -> Chroma:
    """Initialize the persistent ChromaDB vector store.

    Function: get_vector_store
    Args:
        None.
    Returns:
        Chroma: Initialized persistent vector store.
    """
    return Chroma(
        collection_name="knowledge_base",
        embedding_function=get_embeddings(),
        persist_directory=settings.chroma_persist_directory,
    )


def add_documents(documents: list[Document]) -> list[str]:
    """Add document chunks to ChromaDB.

    Function: add_documents
    Args:
        documents (list[Document]): Document chunks to store.
    Returns:
        list[str]: IDs of the stored documents.
    """
    vector_store = get_vector_store()
    return vector_store.add_documents(documents)
