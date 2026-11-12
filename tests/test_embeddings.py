from app.rag.embeddings import get_embeddings

embeddings = get_embeddings()

vectors = embeddings.embed_documents(
    [
        "LangGraph manages agent workflows.",
        "ChromaDB stores vector embeddings.",
    ]
)

print("Number of embeddings:", len(vectors))
print("Embedding dimensions:", len(vectors[0]))