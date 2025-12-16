from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from loader import load_documents


class VectorStoreBuildError(Exception):
    """Custom exception for vector store build failures."""
    pass


def build_and_save_vectorstore(
    index_path: str = "faiss_index"
) -> None:
    """
    Build FAISS vector store from documents and save to disk.
    SAME logic as notebook.
    """
    try:
        # STEP 1: load documents
        documents = load_documents()

        # STEP 2: chunking (same parameters as notebook)
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(documents)

        # STEP 3: embeddings (same model)
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        # STEP 4: build FAISS vector store
        vectorstore = FAISS.from_documents(
            documents=chunks,
            embedding=embeddings
        )

        # STEP 5: save FAISS index
        vectorstore.save_local(index_path)

        print(f"FAISS vector store saved to '{index_path}'")

    except Exception as e:
        raise VectorStoreBuildError(f"Vector store build failed: {e}")

if __name__ == "__main__":
    build_and_save_vectorstore()