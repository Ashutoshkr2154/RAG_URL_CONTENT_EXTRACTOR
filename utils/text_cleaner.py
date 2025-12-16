import json
from typing import List


class TextCleaningError(Exception):
    """Custom exception for text cleaning failures."""
    pass


def split_text_by_fullstop(text: str) -> List[str]:
    """
    Split text into sentence-like units using full stops.
    SAME logic as notebook.
    """
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    return sentences


def process_data_file(
    input_file: str = "data.txt",
    output_file: str = "data_sentences.txt"
) -> None:
    """
    Read data.txt, split text by full stop,
    and save as list of strings.
    """
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()

        sentences = split_text_by_fullstop(text)

        # Save as list format: ["text1", "text2", ...]
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(sentences, f, ensure_ascii=False)

        print(f"Processed {len(sentences)} sentences → {output_file}")

    except Exception as e:
        raise TextCleaningError(f"Text cleaning failed: {e}")
if __name__ == "__main__":
    process_data_file()
