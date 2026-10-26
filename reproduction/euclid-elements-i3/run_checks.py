"""Regenerate real test logs, environment, notebook outputs and metrics."""
import ast
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import time
from fractions import Fraction as F

from euclid_i3 import Point, Certificate, analytic_witness, verify
from experiments import mutations, run_families

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence"


def write_json(name, obj):
    (EVIDENCE/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")


def run(label, args):
    started = time.perf_counter()
    result = subprocess.run([sys.executable, *args], cwd=ROOT,
                            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    elapsed = time.perf_counter()-started
    public_command = "python " + " ".join(args)
    (EVIDENCE/(label+".log")).write_text(
        "$ "+public_command+"\n"+result.stdout+f"\nexit_code: {result.returncode}\n",
        encoding="utf-8")
    match = re.search(r"Ran (\d+) tests? in", result.stdout)
    return {"command": public_command, "exit_code": result.returncode,
            "tests_run": int(match.group(1)) if match else None,
            "wall_seconds": round(elapsed, 6), "log": "evidence/"+label+".log"}


def main():
    EVIDENCE.mkdir(exist_ok=True)
    environment = {
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "os": platform.system(), "architecture": platform.machine(),
        "dependencies": "Python standard library only",
        "packages_installed_for_this_run": [],
        "jupyter_kernel_available": importlib.util.find_spec("ipykernel") is not None,
        "notebook_execution": "stdlib compile/exec, not Jupyter kernel execution",
        "notebook_structure": "self-contained nbformat-4 JSON; ordinary Python cells only",
        "notebook_validation_scope": "sequential code execution and captured stdout; no Jupyter kernel or full schema validation",
        "private_paths_recorded": False,
    }
    write_json("environment.json", environment)
    runs = {label: run(label, flags+["-m", "unittest", "-v", "test_euclid_i3"])
            for label, flags in (("normal", []), ("optimized", ["-O"]),
                                 ("double_optimized", ["-OO"]))}
    notebook_run = run("notebook", ["execute_notebook.py"])
    a, b, c = Point(0, 0), Point(5, 0), F(4)
    cert = analytic_witness(a, b, c)
    cases = {"positive_strict_cut": verify(a, b, c, cert).as_dict()}
    cases.update({name: verify(a, b, c, obj).as_dict()
                  for name, obj in mutations(a, b, cert).items()})
    cases.update({
        "equal_target": verify(a, b, 25, Certificate(Point(0, 5), b)).as_dict(),
        "longer_target": verify(a, b, 36, Certificate(Point(0, 6), Point(6, 0))).as_dict(),
        "zero_target": verify(a, b, 0, Certificate(a, a)).as_dict(),
        "negative_squared_length": verify(a, b, -1, cert).as_dict(),
        "degenerate_segment": verify(a, a, c, cert).as_dict(),
        "degenerate_all_zero": verify(a, a, 0, Certificate(a, a)).as_dict(),
    })
    source_files = ("euclid_i3.py", "experiments.py", "test_euclid_i3.py",
                    "execute_notebook.py", "run_checks.py", "tutorial.ipynb", "README.md")
    hashes = {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in source_files}
    assert_counts = {name: sum(isinstance(n, ast.Assert) for n in ast.walk(
                     ast.parse((ROOT/name).read_text(encoding="utf-8"))))
                     for name in source_files if name.endswith(".py")}
    results = {
        "scope": "original exact-rational analytic teaching reproduction; not a ruler/compass engine",
        "target_notation": "C is squared length, not length",
        "test_runs": runs,
        "unique_unittest_methods": runs["normal"]["tests_run"],
        "family_metrics": run_families(),
        "counterexample_results": cases,
        "notebook": {**notebook_run, "total_cells": 5, "executed_code_cells": 3,
                     "execution_method": "stdlib compile/exec", "jupyter_kernel_used": False},
        "python_assert_statements_by_file": assert_counts,
        "source_sha256": hashes,
        "limits": ["Finite tests do not prove a universal theorem.",
                   "AD distance equality does not prove the I.2 construction or its provenance.",
                   "The witness builder requires rational AB length and rational target length.",
                   "The verifier handles rational point certificates only, not general algebraic coordinates.",
                   "No actual straightedge/compass operation sequence is produced or checked."],
    }
    write_json("results.json", results)
    failed = [name for name, item in {**runs, "notebook": notebook_run}.items() if item["exit_code"]]
    if failed:
        raise SystemExit("FAILED: " + ", ".join(failed))
    print(json.dumps({"tests_each_mode": results["unique_unittest_methods"],
                      "modes_passed": list(runs), **results["family_metrics"],
                      "notebook_code_cells_executed": 3}, indent=2))


if __name__ == "__main__":
    main()
