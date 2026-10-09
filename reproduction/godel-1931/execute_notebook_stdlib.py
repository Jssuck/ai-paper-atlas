"""Execute this pack's ordinary Python notebook cells without Jupyter.

This is NOT an IPython/Jupyter kernel test. It supports only plain Python,
as used by godel1931_toy.ipynb. It saves real stdout and execution counts.
"""

import contextlib
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import sys


def main():
    folder = Path(__file__).resolve().parent
    path = folder / "godel1931_toy.ipynb"
    notebook = json.loads(path.read_text(encoding="utf-8"))
    assert notebook["nbformat"] == 4 and notebook["nbformat_minor"] == 5
    assert notebook["metadata"]["kernelspec"]["name"] == "python3"
    ids = [cell["id"] for cell in notebook["cells"]]
    assert len(ids) == len(set(ids))
    print(f"UTC: {datetime.now(timezone.utc).isoformat()}")
    print(f"Python: {sys.version.split()[0]}")
    print("Verification mode: plain Python cells via stdlib compile/exec; NOT a Jupyter kernel.")
    namespace = {"__name__": "godel_teaching_notebook"}
    os.chdir(folder)
    count = 0
    for index, cell in enumerate(notebook["cells"]):
        assert cell["cell_type"] in ("markdown", "code")
        source = "".join(cell["source"])
        assert isinstance(source, str)
        if cell["cell_type"] != "code":
            continue
        count += 1
        digest = hashlib.sha256(source.encode("utf-8")).hexdigest()[:16]
        print(f"\nCell {index + 1}, execution {count}, source SHA256 prefix {digest}")
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
            exec(compile(source, f"{path.name}:cell-{index + 1}", "exec"), namespace)
        output = stream.getvalue()
        cell["execution_count"] = count
        cell["outputs"] = ([{"output_type": "stream", "name": "stdout",
                             "text": output.splitlines(keepends=True)}] if output else [])
        print(output, end="" if output.endswith("\n") or not output else "\n")
    notebook["metadata"]["verification"] = {
        "method": "stdlib compile/exec, shared namespace, top-to-bottom",
        "jupyter_kernel_tested": False,
        "executed_code_cells": count,
        "python_version": sys.version.split()[0],
    }
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"\nPASS: {count} code cells completed; outputs saved to {path.name}.")


if __name__ == "__main__":
    main()
