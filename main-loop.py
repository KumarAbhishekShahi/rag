"""
RAG Complete Guide — Main Entry Point
=====================================
Usage examples:

  # Index a single file:
  python main.py --ingest docs/report.pdf

  # Index an entire folder:
  python main.py --ingest ./documents

  # Ask a one-time question:
  python main.py --query "What is the refund policy?"

  # Start interactive loop:
  python main.py
"""

import argparse
import os

from rag.loader import load_file, load_directory, load_text_string
from rag.embedder import build_vectorstore, load_vectorstore
from rag.retriever import get_retriever, retrieve_with_scores
from rag.generator import build_rag_chain, ask

PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "rag_docs")


DEMO_TEXTS = [
    (
        "Refund Policy: Customers may request a full refund within 30 days of purchase. "
        "After 30 days, only store credit is available. Refunds are processed within 5-7 "
        "business days. Items must be returned in their original packaging.",
        "refund_policy.txt",
    ),
    (
        "Product Catalogue: Model X1 — Price $299, RAM 16GB, Storage 512GB SSD. "
        "Model X2 — Price $499, RAM 32GB, Storage 1TB NVMe SSD. "
        "Model X3 — Price $799, RAM 64GB, Storage 2TB NVMe SSD.",
        "product_catalogue.txt",
    ),
    (
        "Company Overview: Founded in 2010, Acme Corp is a global technology provider "
        "specialising in enterprise software solutions. Headquartered in Pune, India, "
        "with offices in New York, London, and Singapore.",
        "company_overview.txt",
    ),
]


def run_demo():
    print("\n" + "=" * 60)
    print("  RAG COMPLETE GUIDE — DEMO MODE")
    print("=" * 60)

    docs = []
    for text, source in DEMO_TEXTS:
        docs.extend(load_text_string(text, source=source))

    vectorstore = build_vectorstore(docs, PERSIST_DIR, COLLECTION_NAME)
    retriever = get_retriever(vectorstore)
    chain = build_rag_chain(retriever)

    print("\nDemo indexed successfully.")
    print("Type your questions below. Type 'quit' to exit.\n")

    while True:
        question = input("❓ Your question: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            print("Goodbye.")
            break
        if not question:
            continue

        try:
            answer = ask(chain, question)
            print(f"\n✅ {answer}\n")
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


def interactive_mode():
    vectorstore = load_vectorstore(PERSIST_DIR, COLLECTION_NAME)
    retriever = get_retriever(vectorstore)
    chain = build_rag_chain(retriever)

    print("\n🤖 RAG Interactive Mode")
    print("Type your questions below. Type 'quit' to exit.\n")

    while True:
        question = input("❓ Your question: ").strip()
        if question.lower() in ("quit", "exit", "q"):
            print("Goodbye.")
            break
        if not question:
            continue

        try:
            answer = ask(chain, question)
            print(f"\n✅ {answer}\n")
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


def main():
    parser = argparse.ArgumentParser(
        description="RAG Complete Guide — index documents and ask questions"
    )
    parser.add_argument("--ingest", metavar="PATH",
                        help="File or directory to ingest into the vector store")
    parser.add_argument("--query", metavar="QUESTION",
                        help="Ask a single question and exit")
    parser.add_argument("--scores", action="store_true",
                        help="Show retrieval scores alongside retrieved chunks")
    parser.add_argument("--demo", action="store_true",
                        help="Run the built-in demo and enter prompt loop")
    args = parser.parse_args()

    if args.demo:
        run_demo()
        return

    if args.ingest:
        path = args.ingest
        if os.path.isdir(path):
            docs = load_directory(path)
        else:
            docs = load_file(path)

        build_vectorstore(docs, PERSIST_DIR, COLLECTION_NAME)
        print(f"\n✅ Ingested {len(docs)} chunks into '{PERSIST_DIR}'")

        if args.query:
            vectorstore = load_vectorstore(PERSIST_DIR, COLLECTION_NAME)
            retriever = get_retriever(vectorstore)
            chain = build_rag_chain(retriever)

            if args.scores:
                results = retrieve_with_scores(vectorstore, args.query)
                print("\n📚 Retrieved chunks:")
                for doc, score in results:
                    print(
                        f"  [{score:.3f}] {doc.metadata.get('source', '?')} — "
                        f"{doc.page_content[:120]}…"
                    )
                print()

            answer = ask(chain, args.query)
            print(f"\n✅ {answer}")
            return

        print("\n✅ Ingestion complete. Starting prompt loop...\n")
        interactive_mode()
        return

    if args.query:
        vectorstore = load_vectorstore(PERSIST_DIR, COLLECTION_NAME)
        retriever = get_retriever(vectorstore)
        chain = build_rag_chain(retriever)

        if args.scores:
            results = retrieve_with_scores(vectorstore, args.query)
            print("\n📚 Retrieved chunks:")
            for doc, score in results:
                print(
                    f"  [{score:.3f}] {doc.metadata.get('source', '?')} — "
                    f"{doc.page_content[:120]}…"
                )
            print()

        answer = ask(chain, args.query)
        print(f"\n✅ {answer}")
        return

    interactive_mode()


if __name__ == "__main__":
    main()