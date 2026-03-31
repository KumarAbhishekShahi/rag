"""
Document Loaders
================
Supports: .pdf, .html / .htm, .txt, .csv, and plain strings.
Each loader returns a list of LangChain Document objects.
"""

import os
import csv
from pathlib import Path

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    BSHTMLLoader,
    TextLoader,
    CSVLoader,
    DirectoryLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter


# ─── Chunk Settings ────────────────────────────────────────────────────────────
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n\n", "\n", ".", " ", ""],
)


# ─── Individual File Loaders ───────────────────────────────────────────────────

def load_pdf(path: str) -> list[Document]:
    """Load and chunk a PDF file (text-based or scanned via OCR fallback)."""
    loader = PyPDFLoader(path)
    pages = loader.load()
    chunks = _splitter.split_documents(pages)
    print(f"[PDF]  {path} → {len(pages)} pages → {len(chunks)} chunks")
    return chunks


def load_html(path: str) -> list[Document]:
    """Load and chunk an HTML file; strips tags via BeautifulSoup."""
    loader = BSHTMLLoader(path, open_encoding="utf-8")
    docs = loader.load()
    chunks = _splitter.split_documents(docs)
    print(f"[HTML] {path} → {len(chunks)} chunks")
    return chunks


def load_text(path: str) -> list[Document]:
    """Load and chunk a plain-text file."""
    loader = TextLoader(path, encoding="utf-8")
    docs = loader.load()
    chunks = _splitter.split_documents(docs)
    print(f"[TXT]  {path} → {len(chunks)} chunks")
    return chunks


def load_csv(path: str) -> list[Document]:
    """
    Load a CSV file.
    Each row becomes an individual Document whose content is
    'column1: value1 | column2: value2 | ...'
    """
    loader = CSVLoader(
        file_path=path,
        csv_args={"delimiter": ","},
        encoding="utf-8",
    )
    docs = loader.load()
    print(f"[CSV]  {path} → {len(docs)} rows as documents")
    return docs


def load_text_string(text: str, source: str = "inline") -> list[Document]:
    """Wrap a raw string as a Document and chunk it."""
    doc = Document(page_content=text, metadata={"source": source})
    chunks = _splitter.split_documents([doc])
    print(f"[STR]  source={source} → {len(chunks)} chunks")
    return chunks


# ─── Auto-Detect Loader ────────────────────────────────────────────────────────

EXTENSION_MAP = {
    ".pdf":  load_pdf,
    ".html": load_html,
    ".htm":  load_html,
    ".txt":  load_text,
    ".md":   load_text,
    ".csv":  load_csv,
}


def load_file(path: str) -> list[Document]:
    """Detect file type by extension and call the right loader."""
    ext = Path(path).suffix.lower()
    loader_fn = EXTENSION_MAP.get(ext)
    if loader_fn is None:
        raise ValueError(
            f"Unsupported file type '{ext}'. Supported: {list(EXTENSION_MAP)}"
        )
    return loader_fn(path)


def load_directory(directory: str) -> list[Document]:
    """
    Recursively load all supported documents from a directory.
    Returns a flat list of chunked Documents.
    """
    all_docs: list[Document] = []
    for root, _, files in os.walk(directory):
        for file in files:
            ext = Path(file).suffix.lower()
            if ext in EXTENSION_MAP:
                full_path = os.path.join(root, file)
                try:
                    all_docs.extend(load_file(full_path))
                except Exception as exc:
                    print(f"[WARN] Skipping {full_path}: {exc}")
    print(f"\n[DIR]  Total chunks loaded from '{directory}': {len(all_docs)}")
    return all_docs
