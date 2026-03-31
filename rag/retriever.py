"""
Retriever
=========
Wraps a Chroma vector store with configurable search strategies:
  - similarity       : cosine/MMR retrieval
  - mmr              : Maximal Marginal Relevance (diverse results)
  - similarity_score : returns scores alongside documents
"""

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document


def get_retriever(
    vectorstore: Chroma,
    search_type: str = "mmr",
    k: int = 5,
    fetch_k: int = 20,
    lambda_mult: float = 0.5,
):
    """
    Build a LangChain retriever from a Chroma vector store.

    Parameters
    ----------
    search_type  : 'similarity' | 'mmr'
    k            : number of documents to return
    fetch_k      : candidates fetched before MMR re-ranking
    lambda_mult  : MMR diversity factor (0 = max diversity, 1 = max relevance)
    """
    if search_type == "mmr":
        return vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": k, "fetch_k": fetch_k, "lambda_mult": lambda_mult},
        )
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )


def retrieve_with_scores(
    vectorstore: Chroma,
    query: str,
    k: int = 5,
) -> list[tuple[Document, float]]:
    """Return documents AND their similarity scores (useful for debugging)."""
    return vectorstore.similarity_search_with_relevance_scores(query, k=k)
