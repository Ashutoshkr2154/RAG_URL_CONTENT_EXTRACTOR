# STEP 1: Open Terminal 1 (FastAPI backend)

cd C:\rag_url_project

venv\Scripts\activate

uvicorn app:app --reload

# STEP 2: Open Terminal 2 (Streamlit UI)
cd C:\rag_url_project

venv\Scripts\activate

streamlit run ui/streamlit_app.py
