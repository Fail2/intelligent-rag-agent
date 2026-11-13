from langchain_core.documents import Document

from app.rag.vector_store import get_vector_store


def search_documents(query: str, k: int = 5, section_title: str | None = None,) -> list[Document]:
    """Retrieve the most relevant document chunks from ChromaDB.

    Function: search_documents
    Args:
        query (str): User's search query.
        k (int): Maximum number of results to retrieve.
        section_title (str): Optional section title to filter the search.
            When provided, retrieve documents only from the specified
            knowledge-base section. When None, search across all sections.

    Returns:
        list[Document]: Relevant document chunks with metadata.
    """
    vector_store = get_vector_store()

    filter = (
        {"section_title": section_title}
        if section_title is not None
        else None
    )

    return vector_store.similarity_search(
        query,
        k=k,
        filter=filter,
    )