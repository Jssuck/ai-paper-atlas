"""Compile and run the plain Python cells; this is not a Jupyter kernel run."""
import json
from pathlib import Path
import sys


def main():
    path = Path(__file__).with_name("euclid-iii28.ipynb")
    nb = json.loads(path.read_text(encoding="utf-8"))
    scope = {"__name__": "__main__"}
    if nb["nbformat"] != 4:
        raise ValueError("expected notebook format 4")
    print(f"Python {sys.version.split()[0]} | plain compile/exec (no Jupyter kernel)")
    runs = 0
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            runs += 1
            print(f"cell {cell['id']}")
            exec(compile("".join(cell["source"]), f"{path.name}:{cell['id']}", "exec"), scope)
    print(f"Replay completed: {runs} code cells")


if __name__ == "__main__":
    main()
