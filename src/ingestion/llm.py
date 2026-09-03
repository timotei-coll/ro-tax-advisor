from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def get_llm():
    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0
    )


def ask_llm(prompt):
    llm = get_llm()
    response = llm.invoke(prompt)
    return response.content