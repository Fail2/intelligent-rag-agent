import hashlib

from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.core.config import settings
from app.rag.embeddings import get_embeddings


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


def replace_documents(documents: list[Document]) -> list[str]:
    """Upsert document chunks and remove outdated records for their source.

    Function: replace_documents
    Args:
        documents (list[Document]): New document chunks.
    Returns:
        list[str]: Stable IDs of the stored documents.
    """
    if not documents:
        raise ValueError("No documents provided.")

    sources = {doc.metadata["source"] for doc in documents}

    if len(sources) != 1:
        raise ValueError("All documents must belong to the same source.")

    source = sources.pop()
    vector_store = get_vector_store()

    existing_records = vector_store.get(
        where={"source": source}
    )
    existing_ids = set(existing_records["ids"])

    section_counters = {}
    document_ids = []

    for document in documents:
        section_id = document.metadata["section_id"]
        chunk_index = section_counters.get(section_id, 0)

        section_counters[section_id] = chunk_index + 1

        raw_id = f"{source}:{section_id}:{chunk_index}"
        document_id = hashlib.sha256(raw_id.encode()).hexdigest()

        document_ids.append(document_id)

        # ChromaDB metadata should not contain None values.
        document.metadata = {
            key: value
            for key, value in document.metadata.items()
            if value is not None
        }

    # Upsert: insert new records or update existing records.
    vector_store.add_documents(
        documents=documents,
        ids=document_ids,
    )

    # Remove old records that are no longer part of the new ingestion.
    stale_ids = existing_ids - set(document_ids)

    if stale_ids:
        vector_store.delete(ids=list(stale_ids))

    return document_ids