from graph import create_graph


def main():

    question = input(
        "\nScrie întrebarea: "
    )

    graph = create_graph()

    result = graph.invoke({
        "question": question
    })

    result = graph.invoke({
    "question": question
})

    print("\nCHUNKS GĂSITE:\n")

    for chunk in result["chunks"]:
        print(chunk["text"])
        print("-" * 80)

    print("\nRĂSPUNS:\n")
    print(result["answer"])


if __name__ == "__main__":
    main()