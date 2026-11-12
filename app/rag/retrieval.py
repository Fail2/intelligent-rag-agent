from langchain_core.documents import Document

from app.rag.vector_store import get_vector_store


def search_documents(query: str, k: int = 3) -> list[Document]:
    """Retrieve the most relevant document chunks from ChromaDB.

    Function: search_documents
    Args:
        query (str): User's search query.
        k (int): Maximum number of results to retrieve.
    Returns:
        list[Document]: Relevant document chunks with metadata.
    """
    vector_store = get_vector_store()
    return vector_store.similarity_search(query, k=k)
