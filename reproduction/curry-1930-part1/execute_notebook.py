"""Execute this package's trusted Python notebook with stdlib exec.

This is not a Jupyter kernel or nbclient run, and it does not emulate rich
IPython display, magics, asynchronous cells, or a security sandbox. All code
cells in the supplied notebook use ordinary Python and explicit print().
"""
import argparse
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime, timezone
import io
import json
import os
from pathlib import Path
import platform
import sys
import traceback

ROOT = Path(__file__).resolve().parent


def validate_shape(book):
    if book.get("nbformat") != 4 or book.get("nbformat_minor") != 5:
        raise ValueError("expected nbformat 4.5")
    ids = set()
    for cell in book["cells"]:
        if cell["id"] in ids:
            raise ValueError("duplicate cell id")
        ids.add(cell["id"])
        if cell["cell_type"] not in ("code", "markdown"):
            raise ValueError("unsupported cell type")
        if not isinstance(cell["source"], (list, str)):
            raise ValueError("invalid source")
        if cell["cell_type"] == "code":
            if not isinstance(cell["outputs"], list):
                raise ValueError("invalid outputs")
    # Minimal structural checks, not the full official nbformat JSON schema.


def execute(book, notebook):
    validate_shape(book)
    namespace = {"__name__": "__main__", "__file__": str(notebook)}
    count = 0
    for cell in book["cells"]:
        if cell["cell_type"] != "code":
            continue
        count += 1
        cell["execution_count"] = count
        cell["outputs"] = []
        stdout, stderr = io.StringIO(), io.StringIO()
        source = "".join(cell["source"]) if isinstance(cell["source"], list) else cell["source"]
        error = None
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                exec(compile(source, f"{notebook.name}:{cell['id']}", "exec"), namespace)
            except Exception as exc:
                error = exc
                tb = traceback.format_exc().splitlines()
        for name, text in (("stdout", stdout.getvalue()), ("stderr", stderr.getvalue())):
            if text:
                cell["outputs"].append({"output_type": "stream", "name": name,
                                        "text": text.splitlines(keepends=True)})
        if error is not None:
            cell["outputs"].append({"output_type": "error", "ename": type(error).__name__,
                                    "evalue": str(error), "traceback": tb})
            raise RuntimeError(f"notebook cell {cell['id']} failed: {error}") from error
    book["metadata"].setdefault("language_info", {})["version"] = platform.python_version()
    book["metadata"]["execution_provenance"] = {
        "method": "Python standard-library exec, shared namespace, explicit stdout/stderr capture",
        "jupyter_kernel_used": False,
        "python_version": platform.python_version(),
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "code_cells_executed": count,
        "limitation": "No IPython rich display, magics, kernel protocol or full nbformat schema validation",
    }
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="reexecute and compare outputs without rewriting")
    args = parser.parse_args()
    notebook = ROOT / "tutorial.ipynb"
    book = json.loads(notebook.read_text(encoding="utf-8"))
    old = [c["outputs"] for c in book["cells"] if c["cell_type"] == "code"]
    previous = Path.cwd()
    try:
        os.chdir(ROOT)
        if str(ROOT) not in sys.path:
            sys.path.insert(0, str(ROOT))
        count = execute(book, notebook)
    finally:
        os.chdir(previous)
    outputs = [c["outputs"] for c in book["cells"] if c["cell_type"] == "code"]
    if args.check:
        if outputs != old:
            raise SystemExit("FAIL: rerun outputs differ; use ordinary execution to refresh after inspecting changes")
        print(f"PASS: {count} code cells rerun; saved outputs exactly match (stdlib exec, no Jupyter kernel)")
    else:
        notebook.write_text(json.dumps(book, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"PASS: {count} code cells executed and outputs saved (stdlib exec, no Jupyter kernel)")


if __name__ == "__main__":
    main()
