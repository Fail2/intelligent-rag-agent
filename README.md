Step 1: Test load_pdf()
Run these test cases:
```bash
uv run python - <<'PY'
from pathlib import Path
from app.rag.ingestion import load_pdf

# Valid PDF
documents = load_pdf(Path("documents/W3_Engineers_Knowledge_Base.pdf"))
print("Valid PDF:", len(documents), "pages extracted")

# Invalid path type
try:
    load_pdf("documents/W3_Engineers_Knowledge_Base.pdf")
except Exception as e:
    print(type(e).__name__, ":", e)

# Non-existent file
try:
    load_pdf(Path("documents/missing.pdf"))
except Exception as e:
    print(type(e).__name__, ":", e)

# Wrong extension
try:
    load_pdf(Path("README.md"))
except Exception as e:
    print(type(e).__name__, ":", e)
PY
```

Step 2: Test split_documents()
Run these test cases:
```bash
uv run python - <<'PY'
from pathlib import Path
from langchain_core.documents import Document
from app.rag.ingestion import load_pdf, split_documents

# Valid input
documents = load_pdf(Path("documents/W3_Engineers_Knowledge_Base.pdf"))
chunks = split_documents(documents)
print("Valid input:", len(chunks), "chunks generated")

# Empty list
try:
    split_documents([])
except Exception as e:
    print("Empty list:", type(e).__name__, ":", e)

# Invalid input type
try:
    split_documents("invalid")
except Exception as e:
    print("Invalid type:", type(e).__name__, ":", e)

# Invalid document object
try:
    split_documents(["not a document"])
except Exception as e:
    print("Invalid document:", type(e).__name__, ":", e)

# Empty page content
try:
    split_documents([
        Document(page_content="", metadata={"source": "test.pdf", "page": 1})
    ])
except Exception as e:
    print("Empty content:", type(e).__name__, ":", e)

# Missing source metadata
try:
    split_documents([
        Document(page_content="Some content", metadata={"page": 1})
    ])
except Exception as e:
    print("Missing source:", type(e).__name__, ":", e)

# Invalid page metadata
try:
    split_documents([
        Document(page_content="Some content", metadata={"source": "test.pdf", "page": 0})
    ])
except Exception as e:
    print("Invalid page:", type(e).__name__, ":", e)
PY
```