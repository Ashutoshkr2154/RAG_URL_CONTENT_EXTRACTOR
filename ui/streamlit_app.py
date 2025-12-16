import streamlit as st
import requests

# Page config
st.set_page_config(
    page_title="RAG URL Content Extractor",
    page_icon="🤖",
    layout="centered"
)

# Backend API URL
API_URL = "http://127.0.0.1:8000/ask"

# Title
st.title("🤖 RAG URL Content Extractor")

st.markdown(
    """
Ask questions based on the ingested URL content.  
This system uses **Hybrid RAG (BM25 + FAISS)** for accurate answers.
"""
)

# Input
question = st.text_input(
    "Enter your question:",
    placeholder="What is the ISO Businessowners Program?"
)

# Button
ask_button = st.button("Get Answer")

# Output
if ask_button:
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"question": question},
                    timeout=120
                )

                if response.status_code == 200:
                    answer = response.json().get("answer", "")
                    st.success("Answer")
                    st.write(answer)
                else:
                    st.error("Error from backend API.")

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to FastAPI server. Is it running?")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
