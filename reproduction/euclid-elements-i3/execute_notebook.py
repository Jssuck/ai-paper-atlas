"""Execute this tutorial's plain Python cells using only the standard library.

This is not Jupyter execution: no kernel, magics, display protocol, or isolation.
The tutorial intentionally needs none of them. Outputs are captured from real
execution in order in one shared namespace, then saved to the notebook.
"""
import contextlib
import io
import json
from pathlib import Path


def main():
    path = Path(__file__).with_name("tutorial.ipynb")
    notebook = json.loads(path.read_text(encoding="utf-8"))
    if notebook.get("nbformat") != 4 or len(notebook["cells"]) != 5:
        raise ValueError("expected this five-cell nbformat-4 tutorial")
    namespace = {"__name__": "__notebook__"}
    count = 0
    for index, cell in enumerate(notebook["cells"], 1):
        if cell["cell_type"] == "markdown":
            continue
        if cell["cell_type"] != "code":
            raise ValueError("unexpected cell type")
        count += 1
        capture = io.StringIO()
        with contextlib.redirect_stdout(capture):
            exec(compile("".join(cell["source"]), f"<tutorial cell {index}>", "exec"), namespace)
        output = capture.getvalue()
        cell["execution_count"] = count
        cell["outputs"] = ([{"output_type": "stream", "name": "stdout",
                             "text": output.splitlines(keepends=True)}] if output else [])
        print(f"cell {index}: executed as Python code cell {count}")
        print(output, end="")
    notebook["metadata"]["execution_evidence"] = {
        "method": "stdlib compile/exec; shared namespace; captured stdout",
        "jupyter_kernel_used": False,
        "executed_code_cells": count,
    }
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"PASS: {count} code cells executed top-to-bottom; 5 total cells")


if __name__ == "__main__":
    main()
