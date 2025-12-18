from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from rag.qa_chain import answer_question, QAChainError

app = FastAPI(
    title="RAG URL Questions Answering API",
    description="Gemini-powered Hybrid BM25 + FAISS RAG system",
    version="2.0"
)

# -----------------------------
# Request Schema
# -----------------------------

class QuestionRequest(BaseModel):
    question: str
    debug: Optional[bool] = False   # optional flag for transparency

# -----------------------------
# Response Schema
# -----------------------------

class AnswerResponse(BaseModel):
    question: str
    totalChunksReceived: int
    chunks: List[str]
    answer: str

# -----------------------------
# API Endpoint
# -----------------------------

@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    try:
        # answer_question already handles:
        # - Gemini expansion
        # - Hybrid BM25 + FAISS retrieval
        # - Deduplication
        result = answer_question(request.question)

        response = {
            "question": result["question"],
            "totalChunksReceived": result["totalChunksReceived"],
            "chunks": result["chunks"],
            "answer": result["answer"]
        }

        return response

    except QAChainError as e:
        raise HTTPException(status_code=500, detail=str(e))

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {e}"
        )

# -------------------------
# Health Check
# -------------------------

@app.get("/")
def health_check():
    return {"status": "API is running"}
