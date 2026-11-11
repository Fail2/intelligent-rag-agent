from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_pdf(file_path: Path) -> list[Document]:
    """Extract text from each PDF page.

    Function: load_pdf
    Args:
        file_path (Path): Path to the PDF document.
    Returns:
        list[Document]: Extracted page contents with metadata.
    """
    reader = PdfReader(file_path)
    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text and text.strip():
            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": file_path.name,
                        "page": page_number,
                    },
                )
            )

    return documents


def split_documents(documents: list[Document]) -> list[Document]:
    """Split documents into smaller overlapping chunks.

    Function: split_documents
    Args:
        documents (list[Document]): Documents extracted from PDFs.
    Returns:
        list[Document]: Smaller document chunks with metadata.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
    )

    return text_splitter.split_documents(documents)
