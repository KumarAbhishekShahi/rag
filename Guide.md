# documentation.md

# RAG Complete Guide — Detailed Learning Notes

This document explains the project in a beginner-friendly way. It covers what each file does, what every command means, how to run the system, how to troubleshoot common errors, and where to edit the code when you want to customize the behavior.

---

## 1. What this project is

This project is a **RAG system**.

RAG stands for **Retrieval-Augmented Generation**.

That means:
1. You provide documents such as PDF, HTML, TXT, or CSV.
2. The program reads those files.
3. The program breaks the content into small pieces called **chunks**.
4. The program converts those chunks into **embeddings**.
5. The embeddings are stored in a **vector database**.
6. When you ask a question, the program retrieves the most relevant chunks.
7. Those chunks are sent to the language model.
8. The language model uses that retrieved context to answer your question.

This helps reduce hallucinations and helps the model answer based on your own files.

---

## 2. High-level flow of the project

The project works in this order:

1. **Load documents**
2. **Split documents into chunks**
3. **Create embeddings**
4. **Store embeddings in ChromaDB**
5. **Retrieve relevant chunks for a question**
6. **Send the question + retrieved context to Ollama model**
7. **Print the answer**

---

## 3. Folder structure and purpose of each file

```text
rag-complete-guide/
├── main.py
├── config.py
├── requirements.txt
├── .env.example
├── README.md
├── documentation.md
├── rag/
│   ├── __init__.py
│   ├── loader.py
│   ├── embedder.py
│   ├── retriever.py
│   └── generator.py
├── documents/
│   ├── sample.txt
│   ├── products.csv
│   └── faq.html
└── tests/
    └── test_loader.py
```

### `main.py`
This is the entry point of the application.

It does things like:
- parse command-line arguments,
- run demo mode,
- ingest files,
- start prompt loop,
- call the retriever and generator,
- print answers.

### `config.py`
This stores configuration values such as:
- vector database folder,
- chunk size,
- chunk overlap,
- model name,
- backend name.

### `requirements.txt`
This file lists all Python packages needed for the project.

### `rag/loader.py`
This file loads files such as:
- PDF
- HTML
- TXT
- CSV

Then it chunks them.

### `rag/embedder.py`
This file creates embeddings and stores them into ChromaDB.

### `rag/retriever.py`
This file retrieves relevant chunks from the vector database.

### `rag/generator.py`
This file sends the question and context to the LLM using Ollama or another backend.

### `documents/`
This folder contains example documents for testing.

### `tests/`
This folder contains test code.

---

## 4. Required software you need

You need the following installed on your machine:

1. **Python**
2. **pip**
3. **virtual environment support (venv)**
4. **Ollama**
5. A local model such as **deepseek-r1:8b** or another Ollama-supported model

---

## 5. Step-by-step command explanation

### Step 1: Create a project folder

```bat
mkdir rag-complete-guide
cd rag-complete-guide
```

What this does:
- `mkdir` creates a folder.
- `cd` moves into that folder.

### Step 2: Create a Python virtual environment

```bat
python -m venv .venv
```

What this does:
- `python -m venv` creates an isolated Python environment.
- `.venv` is the folder name for the environment.

Why we do this:
- It prevents package conflicts.
- It keeps project dependencies separate from system Python.

### Step 3: Activate the virtual environment on Windows CMD

```bat
.\.venv\Scripts\activate.bat
```

What this does:
- It activates the local environment.
- Your prompt will start showing something like `(.venv)`.

### Step 4: Upgrade pip

```bat
python -m pip install --upgrade pip
```

Why this is helpful:
- Newer pip handles dependency installation better.
- It reduces package resolution issues.

### Step 5: Install required packages

```bat
python -m pip install -r requirements.txt
```

What this does:
- Reads `requirements.txt`
- Installs all required libraries

---

## 6. Updated recommended requirements.txt

Use this:

```txt
langchain>=0.3.0
langchain-core>=0.3.0
langchain-community>=0.3.0
langchain-text-splitters>=0.3.0
chromadb>=0.5.0
sentence-transformers>=3.0.0
langchain-huggingface>=0.1.0
huggingface-hub>=0.24.0
transformers>=4.44.0
pypdf>=4.0.0
beautifulsoup4>=4.12.0
lxml>=5.0.0
unstructured>=0.15.0
langchain-ollama>=0.2.0
langchain-openai>=0.2.0
langchain-anthropic>=0.2.0
python-dotenv>=1.0.0
pytest>=8.0.0
```

---

## 7. Important code updates you should keep

### In `rag/loader.py`
Use:

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
```

Do **not** use:

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
```

### In `rag/embedder.py`
Use:

```python
from langchain_huggingface import HuggingFaceEmbeddings
```

instead of deprecated import from `langchain_community.embeddings`.

---

## 8. How Ollama fits into this project

Ollama runs the local LLM on your machine.

Your Python code does not directly run the model weights.

Instead:
1. Python sends a request to the local Ollama server.
2. Ollama loads the model.
3. Ollama generates a response.
4. Python receives that response and prints it.

That is why Ollama must be installed and running.

---

## 9. How to set the model name on Windows CMD

Example:

```bat
set LLM_BACKEND=ollama
set LLM_MODEL=deepseek-r1:8b
```

This means:
- `LLM_BACKEND=ollama` → use local Ollama backend
- `LLM_MODEL=deepseek-r1:8b` → use that specific model tag

To verify:

```bat
python -c "import os; print(os.getenv('LLM_BACKEND')); print(os.getenv('LLM_MODEL'))"
```

---

## 10. Common commands you will use often

### List local Ollama models

```bat
ollama list
```

### Check running models

```bat
ollama ps
```

### Pull a model

```bat
ollama pull deepseek-r1:8b
```

### Run the model directly in Ollama

```bat
ollama run deepseek-r1:8b
```

### Start the RAG app

```bat
python main.py
```

### Run demo mode

```bat
python main.py --demo
```

### Ingest a folder

```bat
python main.py --ingest .\documents
```

### Ask one question

```bat
python main.py --query "What is the refund policy?"
```

---

## 11. Example beginner-friendly print statements

Below is the style of print statements you should add to help a beginner understand what the program is doing.

### Example idea for `main.py`

```python
print("\n[STEP 1] Starting the RAG application...")
print("[STEP 2] Loading or creating the vector database...")
print("[STEP 3] Preparing the retriever...")
print("[STEP 4] Connecting to the language model through Ollama...")
print("[STEP 5] You can now ask questions about your documents. Type 'quit' to exit.\n")
```

### Example idea while ingesting documents

```python
print(f"[INFO] Reading documents from: {path}")
print(f"[INFO] Total chunks created: {len(docs)}")
print("[INFO] Creating embeddings for all chunks. This may take a moment...")
print("[INFO] Storing embeddings in ChromaDB so they can be searched later...")
```

### Example idea before model invocation

```python
print("[INFO] Retrieving the most relevant chunks for your question...")
print("[INFO] Sending the retrieved context to the local LLM...")
print("[INFO] Waiting for model response...\n")
```

---

## 12. Common errors and how to understand them

### Error: `ModuleNotFoundError: No module named 'langchain_core'`
Meaning:
- dependencies are not installed in the active environment.

Fix:
```bat
python -m pip install -r requirements.txt
```

### Error: `ModuleNotFoundError: No module named 'langchain.text_splitter'`
Meaning:
- old import path is being used.

Fix:
- change import to `from langchain_text_splitters import RecursiveCharacterTextSplitter`

### Error: `ModuleNotFoundError: No module named 'sentence_transformers'`
Meaning:
- embedding package is missing.

Fix:
```bat
python -m pip install sentence-transformers
```

### Error: `ModuleNotFoundError: No module named 'langchain_ollama'`
Meaning:
- Ollama integration package is missing.

Fix:
```bat
python -m pip install langchain-ollama
```

### Error: `ConnectError [WinError 10061]`
Meaning:
- Python tried to connect to Ollama, but Ollama server was not running.

Fix:
```bat
ollama list
```
or start Ollama application and ensure service is running.

### Error: `model 'llama3.2' not found`
Meaning:
- code is still using a model name that is not installed locally.

Fix:
```bat
ollama list
set LLM_MODEL=deepseek-r1:8b
```

---

## 13. Suggested beginner workflow every time

1. Open CMD
2. Go to project folder
3. Activate venv
4. Set backend and model
5. Verify model exists in Ollama
6. Run the program

Commands:

```bat
cd C:\Users\abhis\rag-complete-guide
.\.venv\Scripts\activate.bat
ollama list
set LLM_BACKEND=ollama
set LLM_MODEL=deepseek-r1:8b
python main.py --demo
```

---

## 14. If you want a clean prompt loop in main.py

You asked to change `main.py` to loop prompt mode.
That is a good idea for learners because it feels like a chat session.

The behavior should be:
- keep asking for a question,
- answer it,
- continue until user types `quit`.

---

## 15. Good beginner learning path

A good way to learn this project is in this order:

1. Understand what RAG means
2. Understand document loading
3. Understand chunking
4. Understand embeddings
5. Understand vector store
6. Understand retrieval
7. Understand prompt template
8. Understand LLM invocation
9. Understand CLI flow in `main.py`
10. Understand how environment variables control model selection

---

## 16. Final advice for beginners

If something fails, do not panic.
Most errors in this project come from one of these categories:
- wrong package not installed,
- wrong import path,
- wrong model name,
- Ollama not running,
- wrong terminal session environment variable.

Always solve issues one layer at a time.
First fix Python imports.
Then fix embeddings.
Then fix Ollama connectivity.
Then fix model name.
Then run the RAG prompt loop.

