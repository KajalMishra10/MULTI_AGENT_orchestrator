from orchestrator.workflow import run_workflow


def main():

    requirement = input("Enter Product Idea: ")

    result = run_workflow(requirement)

    print("\n\nFINAL RESULT\n")

    for key, value in result.items():

        print("\n====================")
        print(key)
        print("====================")
        print(value)


if __name__ == "__main__":
    main()