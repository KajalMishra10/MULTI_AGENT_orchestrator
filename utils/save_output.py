import json
import os
from datetime import datetime


OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")


def get_run_dir():
    """Create a timestamped directory for this run's outputs."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(OUTPUT_DIR, f"run_{timestamp}")
    os.makedirs(run_dir, exist_ok=True)
    return run_dir


def save_agent_output(run_dir: str, agent_name: str, data):
    """Save a single agent's output as a JSON file."""
    filepath = os.path.join(run_dir, f"{agent_name}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[Saved] {agent_name} -> {filepath}")


def save_full_output(run_dir: str, result: dict):
    """Save the complete pipeline result as one combined JSON file."""
    filepath = os.path.join(run_dir, "full_output.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"[Saved] full output -> {filepath}")
