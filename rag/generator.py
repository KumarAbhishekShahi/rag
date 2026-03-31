"""
Generator (LLM Backend)
========================
Supports:
  - Ollama (local)  — set LLM_BACKEND=ollama
  - OpenAI          — set LLM_BACKEND=openai  + OPENAI_API_KEY
  - Anthropic       — set LLM_BACKEND=anthropic + ANTHROPIC_API_KEY
"""

import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

LLM_BACKEND = os.getenv("LLM_BACKEND", "ollama")
# LLM_MODEL   = os.getenv("LLM_MODEL",   "llama3.2")
LLM_MODEL   = os.getenv("LLM_MODEL",   "gemma2:2b")


# ─── RAG Prompt Template ──────────────────────────────────────────────────────

RAG_PROMPT = ChatPromptTemplate.from_template("""
You are an intelligent assistant. Use ONLY the context below to answer the question.
If you cannot find the answer in the context, say "I don't have enough information."
Do NOT make up answers.

### Context:
{context}

### Question:
{question}

### Answer:
""".strip())


# ─── LLM Factory ─────────────────────────────────────────────────────────────

def _get_llm():
    if LLM_BACKEND == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=LLM_MODEL or "gpt-4o-mini", temperature=0)

    elif LLM_BACKEND == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(model=LLM_MODEL or "claude-3-haiku-20240307", temperature=0)

    else:  # default: ollama (local)
        from langchain_ollama import ChatOllama
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        return ChatOllama(model=LLM_MODEL, base_url=base_url, temperature=0)


# ─── RAG Chain Builder ────────────────────────────────────────────────────────

def _format_docs(docs) -> str:
    return "\n\n---\n\n".join(
        f"[Source: {d.metadata.get('source', 'unknown')}]\n{d.page_content}"
        for d in docs
    )


def build_rag_chain(retriever):
    """
    Build a LCEL RAG chain:
      query → retriever → format docs → LLM → string output
    """
    llm = _get_llm()
    chain = (
        {"context": retriever | _format_docs, "question": RunnablePassthrough()}
        | RAG_PROMPT
        | llm
        | StrOutputParser()
    )
    print(f"[LLM]  Backend={LLM_BACKEND}  Model={LLM_MODEL}")
    return chain


def ask(chain, question: str) -> str:
    """Run a question through the RAG chain and return the answer string."""
    return chain.invoke(question)
