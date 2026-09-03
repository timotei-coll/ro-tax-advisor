from parse import parse_html
from chunk import create_chunks, extract_metadata, attach_metadata
from embeddings import load_embedding_model, create_embeddings
from vectorstore import create_vectorstore


HTML_PATH = "src/ingestion/Legea nr.227_2015.html"


def main():

    # 1. Parse HTML
    document = parse_html(HTML_PATH)

    # 2. Creează chunk-uri
    chunks = create_chunks(document)

    # 3. Creează metadata
    metadata = extract_metadata(document)

    chunks = attach_metadata(
        chunks,
        metadata
    )


    print("Chunk-uri:", len(chunks))

    # 4. Creează embeddings
    model = load_embedding_model()

    embeddings = create_embeddings(
        chunks,
        model
    )

    print("Embeddings:", embeddings.shape)

    # 5. Salvează în ChromaDB
    collection = create_vectorstore(
        chunks,
        embeddings
    )

    print(
        "Documente în ChromaDB:",
        collection.count()
    )


if __name__ == "__main__":
    main()