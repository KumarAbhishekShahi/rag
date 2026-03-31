"""
Configuration — override any value via environment variables.
"""
import os

# ── Vector Store ─────────────────────────────────────────────────────────────
CHROMA_PERSIST_DIR  = os.getenv("CHROMA_PERSIST_DIR",  "./chroma_db")
CHROMA_COLLECTION   = os.getenv("CHROMA_COLLECTION",   "rag_docs")

# ── Chunking ──────────────────────────────────────────────────────────────────
CHUNK_SIZE          = int(os.getenv("CHUNK_SIZE",    "1000"))
CHUNK_OVERLAP       = int(os.getenv("CHUNK_OVERLAP", "150"))

# ── Embeddings ────────────────────────────────────────────────────────────────
EMBEDDING_BACKEND   = os.getenv("EMBEDDING_BACKEND", "local")
# local  → sentence-transformers/all-MiniLM-L6-v2 (offline, CPU)
# openai → text-embedding-3-small (requires OPENAI_API_KEY)

# ── LLM ───────────────────────────────────────────────────────────────────────
LLM_BACKEND         = os.getenv("LLM_BACKEND",  "ollama")
# LLM_MODEL           = os.getenv("LLM_MODEL",    "llama3.2")
LLM_MODEL           = os.getenv("LLM_MODEL",    "gemma2:2b")
OLLAMA_BASE_URL     = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
# Backends: ollama | openai | anthropic

# ── Retrieval ─────────────────────────────────────────────────────────────────
RETRIEVER_K         = int(os.getenv("RETRIEVER_K",   "5"))
RETRIEVER_FETCH_K   = int(os.getenv("RETRIEVER_FETCH_K", "20"))
