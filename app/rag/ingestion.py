from pathlib import Path
import re
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
    if not isinstance(file_path, Path):
        raise TypeError("file_path must be a Path object.")
        
    if file_path.suffix.lower() != ".pdf":
            raise ValueError("Only PDF files are supported.")
    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    if not file_path.is_file():
        raise ValueError("file_path must point to a file.")

    

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

    if not documents:
        raise ValueError("The PDF contains no extractable text.")

    return documents



def split_documents(documents: list[Document]) -> list[Document]:
    """Split extracted documents by numbered sections and then by size.

    Function: split_documents
    Args:
        documents (list[Document]): Page-level documents extracted from PDFs.
    Returns:
        list[Document]: Section-aware chunks with hierarchical metadata.
    """
    if not isinstance(documents, list):
        raise TypeError("documents must be a list.")

    if not documents:
        raise ValueError("No documents provided.")

    for index, document in enumerate(documents):
        if not isinstance(document, Document):
            raise TypeError(
                f"Item at index {index} must be a Document object."
            )

        if not document.page_content or not document.page_content.strip():
            raise ValueError(
                f"Document at index {index} contains empty text."
            )

        if not isinstance(document.metadata, dict):
            raise TypeError(
                f"Metadata at index {index} must be a dictionary."
            )

        source = document.metadata.get("source")
        page = document.metadata.get("page")

        if not isinstance(source, str) or not source.strip():
            raise ValueError(
                f"Document at index {index} has an invalid source."
            )

        if isinstance(page, bool) or not isinstance(page, int) or page < 1:
            raise ValueError(
                f"Document at index {index} has an invalid page number."
            )

    sections = []
    current_section = None

    heading_pattern = re.compile(r"^(\d+(?:\.\d+)?)\.?\s+(.+)$")

    for document in documents:
        page_number = document.metadata["page"]

        for line in document.page_content.splitlines():
            line = line.strip()

            if not line or line.startswith("W3 Engineers Ltd. – Knowledge Base"):
                continue

            if re.fullmatch(r"Page \d+", line):
                continue

            match = heading_pattern.match(line)

            if match:
                if current_section:
                    sections.append(current_section)

                section_id, section_title = match.groups()

                current_section = {
                    "section_id": section_id,
                    "section_title": section_title,
                    "source": document.metadata["source"],
                    "pages": {page_number},
                    "lines": [line],
                }
                continue

            if current_section:
                current_section["lines"].append(line)
                current_section["pages"].add(page_number)

    if current_section:
        sections.append(current_section)
    
    if not sections:
        raise ValueError("No numbered sections found in the documents.")

    section_titles = {
        section["section_id"]: section["section_title"]
        for section in sections
    }

    section_documents = []

    for section in sections:
        pages = sorted(section["pages"])
        section_id = section["section_id"]

        parent_section_id = (
            section_id.rsplit(".", 1)[0]
            if "." in section_id
            else None
        )

        parent_section_title = (
            section_titles.get(parent_section_id)
            if parent_section_id
            else None
        )

        section_documents.append(
            Document(
                page_content="\n".join(section["lines"]),
                metadata={
                    "source": section["source"],
                    "section_id": section_id,
                    "section_title": section["section_title"],
                    "parent_section_id": parent_section_id,
                    "parent_section_title": parent_section_title,
                    "page": pages[0],
                    "pages": pages,
                },
            )
        )

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
    )

    return text_splitter.split_documents(section_documents)
