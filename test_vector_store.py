from pathlib import Path

from app.rag.ingestion import load_pdf, split_documents
from app.rag.vector_store import add_documents, get_vector_store


def main() -> None:
    """Load, split, and store PDF documents in ChromaDB.

    Function: main
    Args:
        None.
    Returns:
        None: Prints the ingestion result.
    """
    file_path = Path("documents/W3_Engineers_Knowledge_Base.pdf")

    documents = load_pdf(file_path)
    chunks = split_documents(documents)

    ids = add_documents(chunks)

    print("Total chunks:", len(chunks))
    print("Stored chunks:", len(ids))

    vector_store = get_vector_store()
    print("Collection count:", vector_store._collection.count())


if __name__ == "__main__":
    main()
