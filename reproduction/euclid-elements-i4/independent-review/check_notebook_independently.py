"""Independently rerun saved Python cells and compare their recorded outputs.

This uses Python's standard library, NOT a Jupyter kernel or nbformat validator.
It does not modify the notebook. Run from the reproduction directory.
"""

from contextlib import redirect_stderr, redirect_stdout
from hashlib import sha256
import io
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    os.chdir(ROOT)
    path = ROOT / "euclid_i4_tutorial.ipynb"
    saved = path.read_bytes()
    notebook = json.loads(saved)
    require(notebook["nbformat"] == 4, "unexpected major notebook version")
    namespace = {"__name__": "__independent_notebook_review__"}
    cells = [c for c in notebook["cells"] if c["cell_type"] == "code"]
    for count, cell in enumerate(cells, start=1):
        actual = io.StringIO()
        with redirect_stdout(actual), redirect_stderr(actual):
            exec(compile("".join(cell["source"]), f"notebook_cell_{count}", "exec"), namespace)
        expected = []
        for output in cell["outputs"]:
            require(output["output_type"] == "stream" and output["name"] == "stdout",
                    "audit supports only stdout stream output")
            expected.append("".join(output["text"]))
        require(actual.getvalue() == "".join(expected), f"cell {count} saved output mismatch")
        require(cell["execution_count"] == count, "execution counter mismatch")
        print(f"code cell {count}: re-executed; saved output exactly matches")
    require(notebook["metadata"]["reproduction"]["executed_code_cells"] == len(cells),
            "notebook metadata code-cell count mismatch")
    require(path.read_bytes() == saved, "audit unexpectedly modified the notebook")
    report = {"result": "PASS", "method": "independent standard-library compile/exec; not Jupyter",
              "code_cells": len(cells), "all_saved_outputs_match": True,
              "notebook_unchanged": True, "notebook_sha256": sha256(saved).hexdigest(),
              "audit_script_sha256": sha256(Path(__file__).read_bytes()).hexdigest()}
    Path(__file__).with_name("notebook-results.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
