from orchestrator.workflow import build_graph
from utils.save_output import get_run_dir, save_full_output


def main():

    idea = input("Enter Product Idea: ")

    run_dir = get_run_dir()
    print(f"\n[Output Directory] {run_dir}\n")

    graph = build_graph()

    result = graph.invoke({"idea": idea, "run_dir": run_dir})

    save_full_output(run_dir, {k: v for k, v in result.items() if k != "run_dir"})

    print("\nFINAL OUTPUT\n")

    for k, v in result.items():
        if k != "run_dir":
            print("\n", k)
            print(v)

    print(f"\nAll outputs saved to: {run_dir}")


if __name__ == "__main__":
    main()
