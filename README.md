# STEP 1: Open Terminal 1 (FastAPI backend)

cd C:\rag_url_project

venv\Scripts\activate

uvicorn app:app --reload

# STEP 2: Open Terminal 2 (Streamlit UI)
cd C:\rag_url_project

venv\Scripts\activate

streamlit run ui/streamlit_app.py

# RAG URL Content Extractor

This project is an end-to-end **Retrieval-Augmented Generation (RAG)** application that extracts content from a main URL and its linked child URLs, builds a knowledge base, and answers user questions.

It uses **Hybrid Retrieval (BM25 + FAISS)** for accurate question answering and provides both a **FastAPI backend** and a **Streamlit UI**.

---

## Key Features
- URL content extraction with child URL expansion
- Sentence-level preprocessing and chunking
- Semantic retrieval using FAISS
- Keyword retrieval using BM25
- Hybrid BM25 + FAISS RAG pipeline
- Question answering using HuggingFace FLAN-T5
- FastAPI backend + Streamlit UI

### API Example Questions : 
{
  "question": "What is the ISO Businessowners Program?"
}

{ "question": "What ISO endorsements are available for the Businessowners Program?" }


{ "question": "Explain eligibility criteria for ISO Businessowners coverage." }

{ "question": "What rating considerations are involved in the ISO Businessowners Program?" }

{ "question": "Describe underwriting and rating in the ISO Businessowners Program." }

{ "question": "Summarize the ISO Businessowners Program in simple terms." }

{ "question": "Explain the ISO Businessowners Program as if to a non-technical person." }

{ "question": "What problems does the ISO Businessowners Program solve for small businesses?" }

