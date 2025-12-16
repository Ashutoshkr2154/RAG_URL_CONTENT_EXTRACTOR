from fastapi import FastAPI , HTTPException
from pydantic import BaseModel 

from rag.qa_chain import answer_question , QAChainError 

app = FastAPI(
    title = "RAG URL Questions Answering API" , 
    description="Hybrid BM25 + FAISS RAG system",
    version = "1.0"
)
# -----------------------------
# Request Schema
# -----------------------------

class QuestionRequest(BaseModel):
    question : str 

#-------------------------------
# Response Schema 
# -----------------------------

class AnswerResponse(BaseModel):
    answer:str 

#-------------------------------
# API Endpoint 
# -----------------------------

@app.post("/ask" , response_model = AnswerResponse)
def ask_question(request:QuestionRequest):
    try : 
        answer = answer_question(request.question)
        return {"answer":answer}
    
    except QAChainError as e : 
        raise HTTPException(status_code = 500 , detail = str(e))
    
    except Exception : 
        raise HTTPException(
            status_code = 500 ,
            detail = "Internal Server error"

        )
    
#-------------------------
# Health Check 
#-------------------------
@app.get("/")
def health_check():
    return{"status":"API is running"}