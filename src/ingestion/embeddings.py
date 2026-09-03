from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def load_embedding_model():
    """
    Încarcă modelul de embeddings.
    """

    model = SentenceTransformer(MODEL_NAME)

    return model


def create_embeddings(chunks, model):
    """
    Creează embedding pentru fiecare chunk.
    """

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    return embeddings