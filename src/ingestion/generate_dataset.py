import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from ragas.testset import TestsetGenerator
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()


CHROMA_PATH = "tmp/chroma"
COLLECTION_NAME = "cod_fiscal"

MODEL_NAME = (
    "sentence-transformers/"
    "paraphrase-multilingual-MiniLM-L12-v2"
)

TESTSET_SIZE = 20
OUTPUT_PATH = "tmp/ragas_testset.csv"


def load_chunks():

    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    result = collection.get(
        include=["documents"]
    )

    return result["documents"]


def create_generator():

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0
    )

    generator_llm = LangchainLLMWrapper(llm)

    embeddings = HuggingFaceEmbeddings(
        model_name=MODEL_NAME
    )

    generator_embeddings = LangchainEmbeddingsWrapper(
        embeddings
    )

    generator = TestsetGenerator(
        llm=generator_llm,
        embedding_model=generator_embeddings,
        llm_context=(
            "Generează întrebări în limba română "
            "despre Codul fiscal din România."
        )
    )

    return generator


def generate_dataset():

    print("Încarc chunk-urile...")

    chunks = load_chunks()

    print(
        f"Chunk-uri disponibile: {len(chunks)}"
    )

    print("Construiesc generatorul Ragas...")

    generator = create_generator()

    print(
        f"Generez {TESTSET_SIZE} întrebări..."
    )

    testset = generator.generate_with_chunks(
        chunks=chunks,
        testset_size=TESTSET_SIZE
    )

    output_path = Path(OUTPUT_PATH)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    testset.to_csv(
        output_path
    )

    print()
    print("Dataset generat cu succes!")
    print(
        f"Salvat în: {output_path}"
    )

    print()
    print(
        testset.to_pandas()
    )


if __name__ == "__main__":
    generate_dataset()