"""Execute plain Python cells sequentially; explicitly NOT a Jupyter kernel."""

from contextlib import redirect_stderr, redirect_stdout
import io
import json
from pathlib import Path
import sys


def execute():
    path = Path("euclid_i4_tutorial.ipynb")
    notebook = json.loads(path.read_text(encoding="utf-8"))
    if notebook.get("nbformat") != 4 or not isinstance(notebook.get("cells"), list):
        raise RuntimeError("Unexpected notebook structure")
    namespace = {"__name__": "__notebook__"}
    count = 0
    print("Execution method: Python standard-library compile/exec; NOT a Jupyter kernel")
    print("Optimization level:", sys.flags.optimize)
    for index, cell in enumerate(notebook["cells"]):
        if cell["cell_type"] != "code":
            continue
        count += 1
        output = io.StringIO()
        with redirect_stdout(output), redirect_stderr(output):
            exec(compile("".join(cell["source"]), f"{path.name}:cell_{index}", "exec"), namespace)
        value = output.getvalue()
        cell["execution_count"] = count
        cell["outputs"] = [{"output_type": "stream", "name": "stdout", "text": value.splitlines(keepends=True)}] if value else []
        print(f"--- code cell {count}: PASS ---")
        print(value, end="")
    notebook["metadata"]["reproduction"]["execution"] = "stdlib compile/exec, sequential shared namespace; not a Jupyter kernel"
    notebook["metadata"]["reproduction"]["executed_code_cells"] = count
    notebook["metadata"]["reproduction"]["optimization_level"] = sys.flags.optimize
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: {count} code cells; saved real captured outputs")


if __name__ == "__main__":
    execute()
