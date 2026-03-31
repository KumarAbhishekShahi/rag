"""
Unit tests for document loaders.
Run: pytest tests/
"""
import os
import pytest
from rag.loader import load_text_string, load_text, load_csv, load_html


def test_load_text_string():
    docs = load_text_string("Hello world! This is a test document.", source="test")
    assert len(docs) >= 1
    assert "Hello world" in docs[0].page_content


def test_load_text_file(tmp_path):
    f = tmp_path / "sample.txt"
    f.write_text("LangChain is a framework for building LLM applications.\n" * 10)
    docs = load_text(str(f))
    assert len(docs) >= 1


def test_load_csv_file(tmp_path):
    f = tmp_path / "products.csv"
    f.write_text("name,price,category\nWidget A,19.99,tools\nWidget B,39.99,tools\n")
    docs = load_csv(str(f))
    assert len(docs) == 2


def test_load_html_file(tmp_path):
    f = tmp_path / "page.html"
    f.write_text(
        "<html><body><h1>RAG Guide</h1>"
        "<p>Retrieval-Augmented Generation helps LLMs use external knowledge.</p>"
        "</body></html>"
    )
    docs = load_html(str(f))
    assert len(docs) >= 1
    assert "RAG Guide" in docs[0].page_content or "Retrieval" in docs[0].page_content
