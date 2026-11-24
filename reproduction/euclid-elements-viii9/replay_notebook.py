"""Execute this trusted repository notebook's code cells as plain Python."""
import json
from pathlib import Path


def replay():
    path = Path(__file__).with_name("euclid-viii9.ipynb")
    cells = [c for c in json.loads(path.read_text(encoding="utf-8"))["cells"]
             if c["cell_type"] == "code"]
    if len(cells) != 3:
        raise ValueError("expected three code cells")
    namespace = {}
    for i, cell in enumerate(cells, 1):
        print(f"code cell {i}")
        exec(compile("".join(cell["source"]), f"{path.name}:{i}", "exec"), namespace)
    print(f"Executed {len(cells)} cells with stdlib, not a Jupyter kernel.")


if __name__ == "__main__":
    replay()
