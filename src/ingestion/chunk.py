from docling.chunking import HybridChunker
import re


def create_chunks(document):

    chunker = HybridChunker()

    return list(chunker.chunk(document))


def extract_metadata(document):

    metadata = {}

    current = {
        "title": None,
        "chapter": None,
        "article": None
    }

    for item in document.texts:

        text = item.text.strip()

        if text.upper().startswith("TITLUL"):
            current["title"] = text

        elif text.upper().startswith("CAPITOLUL"):
            current["chapter"] = text

        elif text.upper().startswith("ART."):
            current["article"] = text

        metadata[item.self_ref] = current.copy()

    return metadata


def attach_metadata(chunks, metadata):

    result = []

    for chunk in chunks:

        chunk_metadata = {
            "title": None,
            "chapter": None,
            "article": None
        }

        for item in chunk.meta.doc_items:

            if item.self_ref in metadata:

                chunk_metadata = metadata[item.self_ref]

                break

        result.append(
            {
                "text": chunk.text,
                "metadata": chunk_metadata
            }
        )

    return result