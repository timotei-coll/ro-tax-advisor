import chromadb


def create_vectorstore(
    chunks,
    embeddings,
    persist_directory="tmp/chroma"
):

    client = chromadb.PersistentClient(
        path=persist_directory
    )

    collection = client.get_or_create_collection(
        name="cod_fiscal"
    )

    batch_size = 1000

    for start in range(0, len(chunks), batch_size):

        end = min(
            start + batch_size,
            len(chunks)
        )

        batch_chunks = chunks[start:end]
        batch_embeddings = embeddings[start:end]

        ids = [
            str(i)
            for i in range(start, end)
        ]

        documents = [
            chunk["text"]
            for chunk in batch_chunks
        ]

        metadatas = []

        for chunk in batch_chunks:

            meta = {}

            for key, value in chunk["metadata"].items():

                if value is None:
                    meta[key] = ""
                else:
                    meta[key] = str(value)

            metadatas.append(meta)

        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=[
                embedding.tolist()
                for embedding in batch_embeddings
            ]
        )

        print(
            f"Salvat {end}/{len(chunks)}"
        )

    return collection