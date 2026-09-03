from docling.chunking import HybridChunker


def create_chunks(document):
    chunker = HybridChunker()
    return list(chunker.chunk(document))


def extract_metadata(document):

    metadata = {}

    current_title = None
    current_chapter = None
    current_article = None

    for item in document.texts:

        text = item.text.strip()
        upper_text = text.upper()

        if upper_text.startswith("TITLUL"):
            current_title = text

        elif upper_text.startswith("CAPITOLUL"):
            current_chapter = text

        elif upper_text.startswith("ART."):
            current_article = text

        metadata[item.self_ref] = {
            "title": current_title,
            "chapter": current_chapter,
            "article": current_article
        }

    return metadata


def attach_metadata(chunks, metadata):
    result = []

    for chunk in chunks:
        chunk_metadata = {
            "title": "",
            "chapter": "",
            "article": ""
        }

        # Căutăm cel mai specific metadata disponibil
        for item in chunk.meta.doc_items:
            item_metadata = metadata.get(item.self_ref)

            if not item_metadata:
                continue

            if item_metadata["article"]:
                chunk_metadata = item_metadata
                break

            if item_metadata["chapter"]:
                chunk_metadata = item_metadata

        result.append({
            "text": chunk.text,
            "metadata": chunk_metadata
        })

    return result

    