from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor

tracer_provider = register()
LangChainInstrumentor().instrument(
    tracer_provider=tracer_provider
)
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from prompt import get_relevant_chunks, create_prompt
from llm import ask_llm


class GraphState(TypedDict):
    question: str
    chunks: list
    prompt: str
    answer: str


def retrieve(state: GraphState):
    chunks = get_relevant_chunks(
        state["question"]
    )

    return {
        "chunks": chunks
    }


def build_prompt(state: GraphState):
    prompt = create_prompt(
        state["question"],
        state["chunks"]
    )

    return {
        "prompt": prompt
    }


def call_llm(state: GraphState):
    answer = ask_llm(
        state["prompt"]
    )

    return {
        "answer": answer
    }


def create_graph():
    graph = StateGraph(GraphState)

    graph.add_node(
        "retrieve",
        retrieve
    )

    graph.add_node(
        "build_prompt",
        build_prompt
    )

    graph.add_node(
        "call_llm",
        call_llm
    )

    graph.add_edge(
        START,
        "retrieve"
    )

    graph.add_edge(
        "retrieve",
        "build_prompt"
    )

    graph.add_edge(
        "build_prompt",
        "call_llm"
    )

    graph.add_edge(
        "call_llm",
        END
    )

    return graph.compile()