"""
Embedder & Vector Store
=======================
- Embeddings: sentence-transformers (local, no API key) or OpenAI
- Vector store: ChromaDB with optional persistence
"""

import os
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

# Choose embedding backend: "local" (sentence-transformers) or "openai"
EMBEDDING_BACKEND = os.getenv("EMBEDDING_BACKEND", "local")


def _get_embeddings():
    """Return the configured embedding function."""
    if EMBEDDING_BACKEND == "openai":
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(model="text-embedding-3-small")
    else:
        # Local embeddings — works offline, no API key required
        from langchain_community.embeddings import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )


def build_vectorstore(
    documents: list[Document],
    persist_directory: str = "./chroma_db",
    collection_name: str = "rag_docs",
) -> Chroma:
    """
    Embed documents and store them in ChromaDB.
    If persist_directory already has a collection, it will be extended.
    """
    embeddings = _get_embeddings()
    print(f"\n[EMBED] Building vector store → '{persist_directory}'")
    print(f"        Collection: {collection_name}")
    print(f"        Documents : {len(documents)}")
    print(f"        Backend   : {EMBEDDING_BACKEND}\n")

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name,
    )
    return vectorstore


def load_vectorstore(
    persist_directory: str = "./chroma_db",
    collection_name: str = "rag_docs",
) -> Chroma:
    """Load a previously persisted ChromaDB vector store."""
    embeddings = _get_embeddings()
    print(f"[EMBED] Loading vector store from '{persist_directory}'")
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
        collection_name=collection_name,
    )
