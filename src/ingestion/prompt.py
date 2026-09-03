import re

import chromadb
from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def load_model():
    return SentenceTransformer(MODEL_NAME)

def get_relevant_chunks(
    question,
    persist_directory="tmp/chroma",
    n_results=5
):
    model = load_model()

    question_embedding = model.encode(question).tolist()

    client = chromadb.PersistentClient(
        path=persist_directory
    )

    collection = client.get_collection(
        name="cod_fiscal"
    )

    # Luăm mai multe rezultate semantic
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=50
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    question_lower = question.lower()

    # Cuvinte importante din întrebare
    important_words = [
        word.strip(".,?!:;()")
        for word in question_lower.split()
        if len(word.strip(".,?!:;()")) >= 4
    ]

    scored_chunks = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):
        document_lower = document.lower()

        score = 0

        # Potrivire lexicală
        for word in important_words:
            if word in document_lower:
                score += 3

        # Potrivire pentru expresii importante
        if "profit reinvestit" in question_lower:
            if "profit reinvestit" in document_lower:
                score += 30

            if "art. 22" in document_lower:
                score += 40

        if "impozit pe profit" in question_lower:
            if "impozit pe profit" in document_lower:
                score += 20

        if "tva" in question_lower:
            if "tva" in document_lower:
                score += 20

        if "cota standard" in question_lower:
            if "cota standard" in document_lower:
                score += 30

        # Penalizăm rezultatele foarte îndepărtate semantic
        score -= distance * 10

        scored_chunks.append({
            "text": document,
            "metadata": metadata,
            "score": score
        })

    # Cele mai relevante primele
    scored_chunks.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return scored_chunks[:n_results]


def create_prompt(question, chunks):

    context = "\n\n".join(
        chunk["text"]
        for chunk in chunks
    )

    prompt = f"""
Ești un asistent specializat în Codul fiscal din România.

Răspunde la întrebarea utilizatorului folosind DOAR informațiile
din contextul furnizat.

REGULI IMPORTANTE:
- Prioritizează textul propriu-zis al Codului fiscal.
- Nu confunda exemplele de calcul sau normele metodologice cu
  regula fiscală din articol.
- Dacă un exemplu menționează o valoare diferită de regula din
  articol, nu folosi exemplul ca răspuns.
- Nu inventa informații.
- Dacă informația necesară nu poate fi determinată clar din
  context, spune că nu ai suficiente informații.

CONTEXT:
{context}

ÎNTREBAREA:
{question}

RĂSPUNS:
"""

    return prompt