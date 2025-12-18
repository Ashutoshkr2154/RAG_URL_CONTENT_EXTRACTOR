from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from rank_bm25 import BM25Okapi
from langchain_core.documents import Document

import google.generativeai as genai
import os
import re
import json
from typing import List, Set


class QAChainError(Exception):
    pass


# -----------------------------
# Load FAISS Vector Store
# -----------------------------
def load_vectorstore(index_path: str = "faiss_index") -> FAISS:
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L12-v2"
    )
    return FAISS.load_local(
        index_path,
        embeddings,
        allow_dangerous_deserialization=True
    )


# -----------------------------
# Load documents (for BM25)
# -----------------------------
def load_documents(file_path: str = "data_sentences.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        sentences = json.load(f)

    if not isinstance(sentences, list):
        raise QAChainError("data_sentences.txt must be a JSON list of strings")

    return [Document(page_content=s) for s in sentences]


# -----------------------------
# Build BM25 Retriever
# -----------------------------
def build_bm25(documents):
    corpus = [doc.page_content for doc in documents]
    tokenized_corpus = [
        re.findall(r"\w+", text.lower()) for text in corpus
    ]
    return BM25Okapi(tokenized_corpus), corpus


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
        template="""Answer the question using ONLY the information given in the context.

Focus on information that directly answers the question.
Ignore background or structural details.

If the question asks for criteria, rules, or conditions,
summarize those points clearly.

Context:
{context}

Question:
{question}

Answer:

"""
    )


# -----------------------------
# Gemini Question Expansion (SAFE)
# -----------------------------
def expand_question_gemini(question: str, n: int = 5) -> List[str]:

    """
    Expands question using Gemini.
    FAILSAFE: always returns at least [question]
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return [question]

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
Generate {n} different but related questions for the following query.
Keep them concise and relevant.

Original question:
{question}

Return only the questions as a numbered list.
"""

        response = model.generate_content(prompt)

        questions = []
        for line in response.text.split("\n"):
            line = line.strip()
            if line and line[0].isdigit():
                questions.append(line.split(".", 1)[-1].strip())

        # 🔐 FAILSAFE
        if not questions:
            return [question]

        return questions[:n]

    except Exception:
        # 🔐 ABSOLUTE FAILSAFE
        return [question]


# -----------------------------
# HYBRID RETRIEVER (BM25 + FAISS)
# -----------------------------
def retriever_hybrid_chunks(
    main_question: str,
    k: int = 8
) -> List[str]:

    documents = load_documents()
    vectorstore = load_vectorstore()

    bm25, corpus = build_bm25(documents)

    expanded_questions = expand_question_gemini(main_question)

    unique_chunks: Set[str] = set()

    for q in expanded_questions:
        # FAISS retrieval
        faiss_docs = vectorstore.similarity_search(q, k=k)
        for doc in faiss_docs:
            unique_chunks.add(doc.page_content.strip())

        # BM25 retrieval
        tokenized_query = re.findall(r"\w+", q.lower())
        scores = bm25.get_scores(tokenized_query)

        top_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True
        )[:k]

        for idx in top_indices:
            unique_chunks.add(corpus[idx].strip())

    # Add main question explicitly
    unique_chunks.add(main_question.strip())

    return list(unique_chunks)


# -----------------------------
# QA ENTRY POINT
# -----------------------------
def answer_question(question: str) -> dict:
    try:
        llm = load_llm()
        prompt = build_prompt()

        final_chunks = retriever_hybrid_chunks(question)

        context = "\n\n".join(final_chunks)

        response = llm.invoke(
            prompt.format(context=context, question=question)
        )

        return {
            "question": question,
            "totalChunksReceived": len(final_chunks),
            "chunks": final_chunks,
            "answer": response
        }

    except Exception as e:
        raise QAChainError(f"Failed to answer question: {e}")


# -----------------------------
# TEST
# -----------------------------
if __name__ == "__main__":
    q = "What is the ISO Businessowners Program?"
    result = answer_question(q)

    print("Question:", result["question"])
    print("Total Chunks:", result["totalChunksReceived"])
    print("Answer:", result["answer"])
