from orchestrator.workflow import build_graph


def main():

    idea = input("Enter Product Idea: ")

    graph = build_graph()

    result = graph.invoke({"idea": idea})

    print("\nFINAL OUTPUT\n")

    for k, v in result.items():
        print("\n", k)
        print(v)


if __name__ == "__main__":
    main()