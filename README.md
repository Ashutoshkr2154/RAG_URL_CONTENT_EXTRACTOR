# RAG_URL_CONTENT_EXTRACTOR 
# RAG_URL_CONTENT_EXTRACTOR

This project is an end-to-end **Retrieval-Augmented Generation (RAG)** system that extracts content from a main URL and its child URLs, builds a searchable knowledge base, and answers user questions via an API.

The system uses **Hybrid Retrieval (BM25 + FAISS)** for accurate and context-aware question answering.

---

## Features
- Extracts content from a main URL and linked child URLs
- Inline replacement of child URL content into the main document
- Sentence-level preprocessing and chunking
- Semantic search using FAISS
- Keyword search using BM25
- Hybrid BM25 + FAISS RAG pipeline
- Question answering using HuggingFace FLAN-T5
- FastAPI backend with JSON input/output

---

## Tech Stack
- Python
- LangChain
- FAISS
- BM25
- HuggingFace Transformers
- FastAPI

---

## How to Run
```bash
pip install -r requirements.txt
uvicorn app:app --reload
