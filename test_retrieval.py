from app.rag.retrieval import search_documents


def main() -> None:
    """Test semantic retrieval from ChromaDB.

    Function: main
    Args:
        None.
    Returns:
        None: Prints retrieved documents and metadata.
    """
    query = "What backend development technologies are covered in the internship training?"

    results = search_documents(query, k=10)

    for index, document in enumerate(results, start=1):
        print(f"\n--- Result {index} ---")
        print("Content:", document.page_content)
        print("Metadata:", document.metadata)


if __name__ == "__main__":
    main()
