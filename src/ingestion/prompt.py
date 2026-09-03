import chromadb
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def get_relevant_chunks(
    question,
    persist_directory="tmp/chroma",
    n_results=5
):

 

    model = SentenceTransformer(MODEL_NAME)



    question_embedding = model.encode(question).tolist()



    client = chromadb.PersistentClient(
        path=persist_directory
    )


    collection = client.get_collection(
        name="cod_fiscal"
    )

    print("Număr documente în Chroma:", collection.count())



    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )



    print(results)

    chunks = []

    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i]
        })

   

    return chunks

def create_prompt(question, chunks):
    context = "\n\n".join(
        chunk["text"]
        for chunk in chunks
    )

    prompt = f"""
Ești un asistent specializat în Codul fiscal din România.

Răspunde la întrebarea utilizatorului folosind DOAR
informațiile din contextul furnizat.

Dacă informația nu se găsește în context, spune că
nu ai suficiente informații pentru a răspunde.

CONTEXT:
{context}

ÎNTREBAREA:
{question}

RĂSPUNS:
"""

    return prompt