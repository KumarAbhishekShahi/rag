# RAG Complete Guide 🧠📚

A clean, modular **Retrieval-Augmented Generation (RAG)** system in Python that supports
ingesting **PDF, HTML, Text, CSV** documents and querying them with an LLM.

Works locally with **Ollama** (no API key needed) and also supports **OpenAI** and **Anthropic**.

---

## Project Structure

```
rag-complete-guide/
├── main.py                # CLI entry point & demo runner
├── config.py              # All configuration via env vars
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variable template
├── .gitignore
│
├── rag/                   # Core RAG modules
│   ├── __init__.py
│   ├── loader.py          # Document loaders (PDF, HTML, TXT, CSV)
│   ├── embedder.py        # Embedding + ChromaDB vector store
│   ├── retriever.py       # MMR / similarity retrieval
│   └── generator.py       # LLM chain (Ollama / OpenAI / Anthropic)
│
├── documents/             # Drop your documents here
│   ├── sample.txt
│   ├── products.csv
│   └── faq.html
│
└── tests/
    └── test_loader.py     # Pytest unit tests
```

---

## Supported File Types

| Format | Loader Used             | Notes                          |
|--------|-------------------------|--------------------------------|
| `.pdf` | `PyPDFLoader`           | Text-based PDFs                |
| `.html`| `BSHTMLLoader`          | Tags stripped via BeautifulSoup|
| `.txt` | `TextLoader`            | Plain text and Markdown        |
| `.csv` | `CSVLoader`             | Each row → one Document        |
| String | `load_text_string()`    | Inline text (for demos/tests)  |

---

## Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/<your-username>/rag-complete-guide.git
cd rag-complete-guide

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env — choose your LLM backend (ollama / openai / anthropic)
```

### 3. Run the Built-in Demo (no files needed)

```bash
python main.py --demo
```

### 4. Ingest Your Own Documents

```bash
# Single file
python main.py --ingest documents/sample.txt

# Entire folder (auto-detects PDF, HTML, TXT, CSV)
python main.py --ingest ./documents
```

### 5. Ask Questions

```bash
# One-shot query
python main.py --query "What is the refund policy?"

# Interactive mode
python main.py

# Show retrieval scores for debugging
python main.py --query "What products are available?" --scores
```

---

## LLM Backend Options

### Ollama (Local, Default)

```bash
# Install Ollama: https://ollama.ai
ollama pull llama3.2
export LLM_BACKEND=ollama
export LLM_MODEL=llama3.2
```

### OpenAI

```bash
export LLM_BACKEND=openai
export LLM_MODEL=gpt-4o-mini
export OPENAI_API_KEY=sk-...
```

### Anthropic

```bash
export LLM_BACKEND=anthropic
export LLM_MODEL=claude-3-haiku-20240307
export ANTHROPIC_API_KEY=sk-ant-...
```

---

## Architecture

```
User Query
    │
    ▼
┌──────────────┐   embed query    ┌──────────────────┐
│   Question   │ ──────────────►  │  ChromaDB        │
│              │ ◄──────────────  │  Vector Store    │
└──────────────┘  top-k chunks    └──────────────────┘
    │                                      ▲
    │ question + context                   │ embed chunks
    ▼                                      │
┌──────────────┐              ┌──────────────────────┐
│    LLM       │              │  Document Loaders    │
│ (Ollama/GPT) │              │ PDF | HTML | TXT | CSV│
└──────────────┘              └──────────────────────┘
    │
    ▼
  Answer
```

---

## Run Tests

```bash
pip install pytest
pytest tests/ -v
```

---

## License

MIT
