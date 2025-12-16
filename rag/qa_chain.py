from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from rank_bm25 import BM25Okapi
from langchain_core.documents import Document
import re
import json


class QAChainError(Exception):
    pass


# -----------------------------
# Load FAISS Vector Store
# -----------------------------
def load_vectorstore(index_path: str = "faiss_index") -> FAISS:
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return FAISS.load_local(
        index_path,
        embeddings,
        allow_dangerous_deserialization=True
    )


# -----------------------------
# Load documents (same ones used for FAISS)
# -----------------------------
def load_documents(file_path: str = "data_sentences.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        sentences = json.load(f)

    return [Document(page_content=s) for s in sentences]


# -----------------------------
# Build BM25 Retriever
# -----------------------------
def build_bm25(documents):
    corpus = [doc.page_content for doc in documents]
    tokenized_corpus = [
        re.findall(r"\w+", text.lower()) for text in corpus
    ]
    return BM25Okapi(tokenized_corpus)


# -----------------------------
# Load LLM
# -----------------------------
def load_llm() -> HuggingFacePipeline:
    hf_pipeline = pipeline(
        "text2text-generation",
        model="google/flan-t5-base",
        max_new_tokens=200
    )
    return HuggingFacePipeline(pipeline=hf_pipeline)


# -----------------------------
# Prompt
# -----------------------------
def build_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are an assistant that answers questions strictly based on the provided context.

Context:
{context}

Question:
{question}

Answer:
"""
    )


# -----------------------------
# HYBRID RETRIEVAL (BM25 + FAISS)
# -----------------------------
def hybrid_retrieve(question: str, k: int = 3):
    # Load resources
    documents = load_documents()
    vectorstore = load_vectorstore()

    # FAISS retrieval (semantic)
    faiss_retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )
    faiss_docs = faiss_retriever.invoke(question)

    # BM25 retrieval (keyword)
    bm25 = build_bm25(documents)
    tokenized_query = re.findall(r"\w+", question.lower())
    scores = bm25.get_scores(tokenized_query)

    top_bm25_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:k]

    bm25_docs = [documents[i] for i in top_bm25_indices]

    # Merge & deduplicate
    combined_docs = {
        doc.page_content: doc
        for doc in (faiss_docs + bm25_docs)
    }

    return list(combined_docs.values())


# -----------------------------
# QA ENTRY POINT
# -----------------------------
def answer_question(question: str, k: int = 3) -> str:
    try:
        retrieved_docs = hybrid_retrieve(question, k=k)
        context = "\n\n".join(doc.page_content for doc in retrieved_docs)

        llm = load_llm()
        prompt = build_prompt()

        response = llm.invoke(
            prompt.format(context=context, question=question)
        )

        return response

    except Exception as e:
        raise QAChainError(f"Failed to answer question: {e}")


# -----------------------------
# TEST
# -----------------------------
if __name__ == "__main__":
    q = "What is the ISO Businessowners Program?"
    print("Question:", q)
    print("Answer:", answer_question(q))
