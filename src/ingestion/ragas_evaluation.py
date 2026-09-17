import pandas as pd

from ragas import evaluate
from ragas import EvaluationDataset

from ragas.metrics import (
    faithfulness,
    context_precision,
    context_recall,
)

from ragas.llms import LangchainLLMWrapper
from langchain_groq import ChatGroq

from graph import create_graph


DATASET_PATH = "tmp/ragas_testset.csv"
RESULTS_PATH = "tmp/ragas_results.csv"


def load_dataset():
    dataframe = pd.read_csv(DATASET_PATH)

    # reference_contexts este salvat în CSV ca string.
    # Nu avem nevoie de el aici deoarece contextul este
    # obținut direct din rezultatul RAG.
    dataframe = dataframe[["user_input", "reference"]]

    return EvaluationDataset.from_pandas(dataframe)


def create_evaluator_llm():
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
        max_tokens=2048,
    )

    return LangchainLLMWrapper(llm)


def run_evaluation():
    print("Încarc datasetul...")
    dataset = load_dataset()

    print(f"Dataset încărcat: {len(dataset)} întrebări")

    print("Construiesc graful RAG...")
    graph = create_graph()

    evaluation_rows = []

    print(f"\nRulez RAG pentru {len(dataset)} întrebări...\n")

    for i, sample in enumerate(dataset, start=1):
        question = sample.user_input

        print(f"[{i}/{len(dataset)}] {question}")

        result = graph.invoke({
            "question": question
        })

        answer = result["answer"]

        contexts = [
            chunk["text"]
            for chunk in result["chunks"]
        ]

        evaluation_rows.append({
            "user_input": question,
            "response": answer,
            "retrieved_contexts": contexts,
            "reference": sample.reference,
        })

    print("\nToate întrebările au fost procesate de RAG.")

    evaluation_dataset = EvaluationDataset.from_list(
        evaluation_rows
    )

    print("\nConstruiesc evaluatorul Ragas...")

    evaluator_llm = create_evaluator_llm()

    print("Încep evaluarea Ragas...\n")

    results = evaluate(
        dataset=evaluation_dataset,
        metrics=[
            faithfulness,
            context_precision,
            context_recall,
        ],
        llm=evaluator_llm,
    )

    print("\n==============================")
    print("REZULTATE RAGAS")
    print("==============================")

    results_df = results.to_pandas()

    # Păstrăm doar întrebarea și cele 3 scoruri.
    summary_df = results_df[
        [
            "user_input",
            "faithfulness",
            "context_precision",
            "context_recall",
        ]
    ]

    # Salvăm doar rezultatele scurte.
    summary_df.to_csv(
        RESULTS_PATH,
        index=False,
        encoding="utf-8-sig",
        lineterminator="\n",
    )

    print("\nRezultate:")
    print(summary_df.to_string(index=False))

    print("\n==============================")
    print("EVALUARE FINALIZATĂ")
    print("==============================")

    print("Rezultatele au fost salvate în:")
    print(RESULTS_PATH)


if __name__ == "__main__":
    run_evaluation()