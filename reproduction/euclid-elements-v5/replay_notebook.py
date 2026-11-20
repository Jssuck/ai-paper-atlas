"""Replay the Python cells of the companion notebook without a kernel."""
import json
import sys
from pathlib import Path

notebook = Path(__file__).with_name("euclid-v5.ipynb")
data = json.loads(notebook.read_text(encoding="utf-8"))
cells = [c for c in data["cells"] if c["cell_type"] == "code"]
if not cells:
    raise ValueError("empty notebook")
ns = {"__name__":"__notebook__"}
print(sys.version.split()[0], "| plain compile/exec (no Jupyter kernel)")
for i, cell in enumerate(cells, 1):
    print("cell", i)
    exec(compile("".join(cell["source"]), f"{notebook.name}:cell-{i}", "exec"), ns)
print("Replay completed:", len(cells), "code cells")
