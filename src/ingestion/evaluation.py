import os
import requests

from dotenv import load_dotenv
from opentelemetry import trace

from phoenix.evals import LLM
from phoenix.evals.metrics import (
    FaithfulnessEvaluator,
    DocumentRelevanceEvaluator,
)

from prompt import get_relevant_chunks
from graph import create_graph


load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


def send_annotation(
    span_id,
    name,
    label,
    score,
    explanation
):
    response = requests.post(
        "http://localhost:6006/v1/span_annotations",
        json={
            "data": [
                {
                    "span_id": span_id,
                    "name": name,
                    "annotator_kind": "LLM",
                    "result": {
                        "label": label,
                        "score": score,
                        "explanation": explanation,
                    },
                    "metadata": {},
                }
            ]
        },
        timeout=10,
    )

    if response.status_code not in (200, 201, 202):
        print(
            f"Eroare Phoenix pentru {name}: "
            f"{response.status_code} - {response.text}"
        )

    return response


def evaluate_question(question):

    # =====================================================
    # 1. RECUPERĂM CHUNK-URILE
    # =====================================================

    chunks = get_relevant_chunks(question)

    # =====================================================
    # 2. RULĂM APLICAȚIA RAG
    # =====================================================

    tracer = trace.get_tracer("ro-tax-advisor-evaluation")

    with tracer.start_as_current_span(
        "RO Tax Advisor - Evaluation"
    ) as evaluation_span:

        span_context = evaluation_span.get_span_context()

        span_id = format(
            span_context.span_id,
            "016x"
        )

        graph = create_graph()

        result = graph.invoke({
            "question": question
        })

        answer = result["answer"]

    # =====================================================
    # 3. CONSTRUIM CONTEXTUL
    # =====================================================

    context = "\n\n".join(
        chunk["text"]
        for chunk in chunks
    )

    # =====================================================
    # 4. LLM FOLOSIT CA EVALUATOR
    # =====================================================

    evaluator_llm = LLM(
        provider="litellm",
        model="groq/openai/gpt-oss-120b",
        client="litellm",
    )

    # =====================================================
    # 5. RELEVANȚA CHUNK-URILOR
    # =====================================================

    relevance_evaluator = DocumentRelevanceEvaluator(
        llm=evaluator_llm
    )

    print("\n==============================")
    print("RELEVANȚA CHUNK-URILOR")
    print("==============================")

    relevance_evaluations = []

    for i, chunk in enumerate(
        chunks,
        start=1
    ):

        evaluation = relevance_evaluator.evaluate(
            eval_input={
                "input": question,
                "document_text": chunk["text"],
            }
        )

        relevance_evaluations.append(evaluation)

        result = evaluation[0]

        print(f"\nChunk {i}:")
        print(evaluation)

        # Trimitem scorul în Phoenix
        send_annotation(
            span_id=span_id,
            name=f"relevance_chunk_{i}",
            label=result.label,
            score=result.score,
            explanation=result.explanation,
        )

    # =====================================================
    # 6. FAITHFULNESS / HALLUCINATION
    # =====================================================

    faithfulness_evaluator = FaithfulnessEvaluator(
        llm=evaluator_llm
    )

    print("\n==============================")
    print("FAITHFULNESS / HALLUCINATION")
    print("==============================")

    faithfulness_result = faithfulness_evaluator.evaluate(
        eval_input={
            "input": question,
            "output": answer,
            "context": context,
        }
    )

    print(faithfulness_result)

    # Trimitem faithfulness în Phoenix
    result = faithfulness_result[0]

    send_annotation(
        span_id=span_id,
        name="faithfulness",
        label=result.label,
        score=result.score,
        explanation=result.explanation,
    )

    # =====================================================
    # 7. RĂSPUNS
    # =====================================================

    print("\n==============================")
    print("RĂSPUNS")
    print("==============================")

    print(answer)

    print("\n==============================")
    print("PHOENIX")
    print("==============================")

    print(
        "Evaluările au fost trimise în Phoenix."
    )

    print(
        f"Span ID: {span_id}"
    )


if __name__ == "__main__":

    question = input(
        "\nÎntrebarea: "
    )

    evaluate_question(question)