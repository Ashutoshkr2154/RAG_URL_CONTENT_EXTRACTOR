import json
from typing import List
from langchain_core.documents import Document


class DocumentLoadingError(Exception):
    """Custom exception for document loading failures."""
    pass


def load_documents(
    input_file: str = "data_sentences.txt"
) -> List[Document]:
    """
    Load sentence list from file and convert to LangChain Documents.
    SAME logic as notebook.
    """
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            sentences = json.load(f)

        documents = [Document(page_content=sentence) for sentence in sentences]

        return documents

    except Exception as e:
        raise DocumentLoadingError(f"Failed to load documents: {e}")
"""
if __name__ == "__main__":
    docs = load_documents()
    print(f"Total documents loaded: {len(docs)}")
    print("Sample document:")
    print(docs[0].page_content)
"""