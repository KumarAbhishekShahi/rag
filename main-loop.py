"""
RAG Complete Guide — Main Entry Point
=====================================

This file is the main entry point of the project.

What this program can do:
1. Run a built-in demo using sample text.
2. Ingest one file or an entire directory of files.
3. Ask one question and return one answer.
4. Start an interactive prompt loop so the user can ask many questions.

Why this file matters:
- It connects all the other modules together.
- It explains the high-level workflow of the RAG application.
- It is a good place for beginners to understand the overall sequence.

Typical beginner usage:
    python main.py --demo
    python main.py --ingest .\\documents
    python main.py
    python main.py --query "What is the refund policy?"
"""

import argparse
import os

# Import the helper functions from the project's internal modules.
# Each module has one responsibility:
# - loader.py    -> reads documents
# - embedder.py  -> creates embeddings and stores them in ChromaDB
# - retriever.py -> finds the most relevant chunks for a question
# - generator.py -> sends context + question to the language model
from rag.loader import load_file, load_directory, load_text_string
from rag.embedder import build_vectorstore, load_vectorstore
from rag.retriever import get_retriever, retrieve_with_scores
from rag.generator import build_rag_chain, ask


# ------------------------------------------------------------------------------
# Configuration values
# ------------------------------------------------------------------------------

# These values are read from environment variables if they exist.
# If the environment variables are not set, the default values are used.
PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "rag_docs")


# ------------------------------------------------------------------------------
# Demo data
# ------------------------------------------------------------------------------

# This demo data allows a beginner to run the project without collecting real files.
# Each item is a tuple:
#   (document_text, source_name)
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


# ------------------------------------------------------------------------------
# Helper function: print a section separator
# ------------------------------------------------------------------------------

def print_banner(title: str):
    """
    Print a simple visual banner so the user can clearly see the current stage.

    Example:
    ============================================================
      RAG COMPLETE GUIDE — DEMO MODE
    ============================================================
    """
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


# ------------------------------------------------------------------------------
# Demo mode
# ------------------------------------------------------------------------------

def run_demo():
    """
    Run a small built-in demo.

    This function is designed for beginners who want to test the RAG flow
    before working with their own files.

    What happens here:
    1. Demo text is converted into document objects.
    2. Those documents are embedded and stored in ChromaDB.
    3. A retriever is created.
    4. A RAG chain is built using the configured LLM.
    5. The user can ask questions in a loop.
    """
    print_banner("RAG COMPLETE GUIDE — DEMO MODE")

    print("[STEP 1] Starting demo mode.")
    print("[INFO] In demo mode, we use built-in sample text instead of reading external files.")
    print("[INFO] This is useful for checking whether the RAG pipeline works correctly.\n")

    docs = []

    print("[STEP 2] Converting demo text into LangChain Document objects.")
    print("[INFO] Each small sample text will be wrapped as a document and then chunked if needed.\n")

    for text, source in DEMO_TEXTS:
        print(f"[INFO] Loading demo content from source label: {source}")
        loaded_docs = load_text_string(text, source=source)
        docs.extend(loaded_docs)

    print(f"\n[INFO] Total demo chunks created: {len(docs)}")

    print("\n[STEP 3] Building the vector store.")
    print("[INFO] This step creates embeddings for the chunks and stores them in ChromaDB.")
    print("[INFO] Embeddings are numerical representations of text that help semantic search work.\n")

    vectorstore = build_vectorstore(docs, PERSIST_DIR, COLLECTION_NAME)

    print("\n[STEP 4] Creating the retriever.")
    print("[INFO] The retriever is the component that searches the vector database.")
    print("[INFO] It will later fetch the most relevant chunks for each user question.\n")

    retriever = get_retriever(vectorstore)

    print("[STEP 5] Building the RAG chain.")
    print("[INFO] The RAG chain combines retrieval + prompt template + language model.")
    print("[INFO] This means your question will be answered using retrieved context.\n")

    chain = build_rag_chain(retriever)

    print("[STEP 6] Demo setup complete.")
    print("[INFO] You can now ask questions about the demo data.")
    print("[INFO] Type 'quit', 'exit', or 'q' to stop.\n")

    while True:
        question = input("❓ Your question: ").strip()

        if question.lower() in ("quit", "exit", "q"):
            print("\n[INFO] Exiting demo mode. Goodbye.")
            break

        if not question:
            print("[WARN] You entered an empty question. Please type something.\n")
            continue

        try:
            print("\n[STEP 7] Retrieving the most relevant chunks for your question...")
            print("[STEP 8] Sending the retrieved context to the language model...")
            print("[INFO] Please wait while the model generates an answer.\n")

            answer = ask(chain, question)

            print("✅ Answer:")
            print(answer)
            print()

        except Exception as e:
            print("\n[ERROR] Something went wrong while generating the answer.")
            print(f"[ERROR DETAILS] {e}\n")


# ------------------------------------------------------------------------------
# Interactive mode
# ------------------------------------------------------------------------------

def interactive_mode():
    """
    Start interactive question-answer mode using the existing vector database.

    This mode assumes that:
    - documents have already been ingested, and
    - a vector store already exists on disk.

    If no vector store exists yet, the user should ingest files first.
    """
    print_banner("RAG INTERACTIVE MODE")

    print("[STEP 1] Loading the existing vector database from disk.")
    print(f"[INFO] Vector store folder: {PERSIST_DIR}")
    print(f"[INFO] Collection name    : {COLLECTION_NAME}\n")

    vectorstore = load_vectorstore(PERSIST_DIR, COLLECTION_NAME)

    print("[STEP 2] Creating the retriever.")
    retriever = get_retriever(vectorstore)

    print("[STEP 3] Building the RAG chain using the configured language model.\n")
    chain = build_rag_chain(retriever)

    print("[READY] The system is ready.")
    print("[INFO] Ask any question related to the ingested documents.")
    print("[INFO] Type 'quit', 'exit', or 'q' to stop.\n")

    while True:
        question = input("❓ Your question: ").strip()

        if question.lower() in ("quit", "exit", "q"):
            print("\n[INFO] Exiting interactive mode. Goodbye.")
            break

        if not question:
            print("[WARN] Empty input received. Please enter a question.\n")
            continue

        try:
            print("\n[INFO] Searching the vector database for relevant chunks...")
            print("[INFO] Sending context and question to the model...")
            print("[INFO] Generating answer...\n")

            answer = ask(chain, question)

            print("✅ Answer:")
            print(answer)
            print()

        except Exception as e:
            print("\n[ERROR] Failed to answer the question.")
            print(f"[ERROR DETAILS] {e}\n")


# ------------------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------------------

def main():
    """
    Parse command-line arguments and decide what mode to run.

    Supported modes:
    - --demo
    - --ingest PATH
    - --query "some question"
    - no arguments -> start interactive mode
    """
    print_banner("RAG COMPLETE GUIDE — APPLICATION START")

    print("[INFO] Initializing command-line argument parser.")
    print("[INFO] This program supports demo mode, ingestion mode, one-shot query mode,")
    print("[INFO] and interactive chat mode.\n")

    parser = argparse.ArgumentParser(
        description="RAG Complete Guide — index documents and ask questions"
    )

    parser.add_argument(
        "--ingest",
        metavar="PATH",
        help="File or directory to ingest into the vector store"
    )

    parser.add_argument(
        "--query",
        metavar="QUESTION",
        help="Ask a single question and exit"
    )

    parser.add_argument(
        "--scores",
        action="store_true",
        help="Show retrieval scores alongside retrieved chunks"
    )

    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run the built-in demo and enter prompt loop"
    )

    args = parser.parse_args()

    print("[INFO] Parsed command-line arguments successfully.")
    print(f"[INFO] --demo   = {args.demo}")
    print(f"[INFO] --ingest = {args.ingest}")
    print(f"[INFO] --query  = {args.query}")
    print(f"[INFO] --scores = {args.scores}\n")

    # --------------------------------------------------------------------------
    # Case 1: Demo mode
    # --------------------------------------------------------------------------
    if args.demo:
        print("[DECISION] Demo mode selected.\n")
        run_demo()
        return

    # --------------------------------------------------------------------------
    # Case 2: Ingest documents first
    # --------------------------------------------------------------------------
    if args.ingest:
        print("[DECISION] Ingestion mode selected.")
        print(f"[INFO] Path provided for ingestion: {args.ingest}\n")

        path = args.ingest

        if os.path.isdir(path):
            print("[INFO] The provided path is a directory.")
            print("[INFO] The program will scan the folder and ingest all supported files.\n")
            docs = load_directory(path)
        else:
            print("[INFO] The provided path is treated as a single file.")
            print("[INFO] The program will detect the file type and load it.\n")
            docs = load_file(path)

        print(f"\n[INFO] Total chunks prepared for embedding: {len(docs)}")

        print("\n[STEP] Building the vector store from the ingested documents.")
        build_vectorstore(docs, PERSIST_DIR, COLLECTION_NAME)

        print(f"\n✅ Ingestion complete. Vector store saved at: {PERSIST_DIR}")

        # If the user also supplied a one-time query, answer it immediately.
        if args.query:
            print("\n[INFO] A query was also provided, so the program will answer it now.")
            print("[INFO] Reloading vector store, preparing retriever, and building chain.\n")

            vectorstore = load_vectorstore(PERSIST_DIR, COLLECTION_NAME)
            retriever = get_retriever(vectorstore)
            chain = build_rag_chain(retriever)

            if args.scores:
                print("[INFO] Retrieval score display is enabled.")
                print("[INFO] The system will show which chunks were retrieved and their scores.\n")

                results = retrieve_with_scores(vectorstore, args.query)

                print("📚 Retrieved chunks:")
                for doc, score in results:
                    print(
                        f"  [{score:.3f}] {doc.metadata.get('source', '?')} — "
                        f"{doc.page_content[:120]}..."
                    )
                print()

            print("[INFO] Asking the language model to answer the provided question.\n")
            answer = ask(chain, args.query)

            print("✅ Answer:")
            print(answer)
            return

        print("\n[INFO] No one-time query was provided.")
        print("[INFO] The program will now start interactive mode so you can ask many questions.\n")
        interactive_mode()
        return

    # --------------------------------------------------------------------------
    # Case 3: One-shot query using an already existing vector store
    # --------------------------------------------------------------------------
    if args.query:
        print("[DECISION] One-shot query mode selected.")
        print("[INFO] The program will load the existing vector store and answer one question.\n")

        vectorstore = load_vectorstore(PERSIST_DIR, COLLECTION_NAME)
        retriever = get_retriever(vectorstore)
        chain = build_rag_chain(retriever)

        if args.scores:
            print("[INFO] Retrieval score display is enabled.\n")
            results = retrieve_with_scores(vectorstore, args.query)

            print("📚 Retrieved chunks:")
            for doc, score in results:
                print(
                    f"  [{score:.3f}] {doc.metadata.get('source', '?')} — "
                    f"{doc.page_content[:120]}..."
                )
            print()

        print("[INFO] Sending question to the RAG chain.\n")
        answer = ask(chain, args.query)

        print("✅ Answer:")
        print(answer)
        return

    # --------------------------------------------------------------------------
    # Case 4: No arguments -> interactive mode
    # --------------------------------------------------------------------------
    print("[DECISION] No special arguments were provided.")
    print("[INFO] Starting interactive mode using the existing vector database.\n")
    interactive_mode()


# ------------------------------------------------------------------------------
# Python entry point
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    # This special condition means:
    # “Run main() only when this file is executed directly.”
    # It prevents main() from running automatically if this file is imported elsewhere.
    main()