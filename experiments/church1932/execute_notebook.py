"""Run this plain-Python notebook without installing Jupyter dependencies.

This is a deliberately limited runner, not a Jupyter kernel: it supports exec-
compatible Python cells and stdout/stderr, not IPython magic, rich display or
automatic display of a cell's final expression. All notebook cells explicitly
print their results. Run only notebooks you trust: their cells execute code.
"""

import argparse
from contextlib import redirect_stderr, redirect_stdout
import io
import json
import os
from pathlib import Path
import platform
import sys
import traceback


def execute(path: Path) -> None:
    path = path.resolve()
    notebook = json.loads(path.read_text(encoding="utf-8"))
    if notebook.get("nbformat") != 4:
        raise ValueError("Only nbformat 4 is supported")
    original_cwd = Path.cwd()
    original_path = sys.path.copy()
    sys.dont_write_bytecode = True
    namespace = {"__name__": "__main__", "__builtins__": __builtins__}
    count = 0
    try:
        os.chdir(path.parent)
        sys.path.insert(0, str(path.parent))
        for index, cell in enumerate(notebook["cells"]):
            if cell["cell_type"] != "code":
                continue
            count += 1
            source = cell["source"]
            source = source if isinstance(source, str) else "".join(source)
            cell["execution_count"] = count
            cell["outputs"] = []
            stdout, stderr = io.StringIO(), io.StringIO()
            try:
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    exec(compile(source, f"{path.name}:cell-{index + 1}", "exec"), namespace)
            except Exception as exc:
                cell["outputs"].append({"output_type": "error", "ename": type(exc).__name__,
                                        "evalue": str(exc),
                                        "traceback": traceback.format_exc().splitlines()})
                notebook["metadata"]["stdlib_execution"] = {"status": "failed", "code_cells": count}
                path.write_text(json.dumps(notebook, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                raise
            for name, stream in (("stdout", stdout), ("stderr", stderr)):
                if stream.getvalue():
                    cell["outputs"].append({"output_type": "stream", "name": name,
                                            "text": stream.getvalue().splitlines(keepends=True)})
            print(f"Cell {count}: PASS ({len(source.splitlines())} lines)")
        notebook["metadata"]["language_info"]["version"] = platform.python_version()
        notebook["metadata"]["stdlib_execution"] = {
            "status": "passed", "code_cells": count,
            "executor": "execute_notebook.py; sequential Python exec; not a Jupyter kernel",
            "python_version": platform.python_version(),
        }
        path.write_text(json.dumps(notebook, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    finally:
        os.chdir(original_cwd)
        sys.path[:] = original_path
    print(f"Executed {count} code cells top-to-bottom; actual outputs saved to {path.name}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("notebook", type=Path, nargs="?",
                        default=Path(__file__).with_name("church1932.ipynb"))
    execute(parser.parse_args().notebook)
