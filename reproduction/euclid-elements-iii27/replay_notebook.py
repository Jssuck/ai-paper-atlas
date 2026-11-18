"""Run plain Python notebook cells in one namespace; not Jupyter execution."""
import json
import sys
from pathlib import Path

if __name__ == "__main__":
    path = Path(__file__).with_name("euclid-iii27.ipynb")
    notebook = json.loads(path.read_text(encoding="utf-8"))
    scope = {"__name__": "__main__"}
    print("Python", sys.version.split()[0], "| compile/exec; no Jupyter kernel")
    for n, cell in enumerate(notebook["cells"], 1):
        if cell["cell_type"] == "code":
            print(f"cell {n}")
            exec(compile("".join(cell["source"]), f"{path.name}:cell-{n}", "exec"), scope)
    print("Replay completed")
