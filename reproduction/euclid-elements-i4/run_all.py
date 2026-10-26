"""Rebuild public evidence with actual subprocess runs and path-safe logs."""

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


def main():
    root = Path(__file__).resolve().parent
    os.chdir(root)
    Path("logs").mkdir(exist_ok=True)
    Path("results").mkdir(exist_ok=True)
    environment = {
        "python": platform.python_version(), "implementation": platform.python_implementation(),
        "os": platform.system(), "architecture": platform.machine(),
        "third_party_dependencies_required": [],
        "optional_modules_available": {name: importlib.util.find_spec(name) is not None
                                       for name in ("jupyter", "nbformat", "nbclient", "ipykernel")},
        "notebook_execution_method": "standard-library compile/exec, not Jupyter kernel",
        "clock_utc_reported_by_runtime": datetime.now(timezone.utc).isoformat(),
        "commands_relative_to": "reproduction/euclid-elements-i4/",
    }
    Path("results/environment.json").write_text(json.dumps(environment, indent=2) + "\n", encoding="utf-8")
    jobs = [
        ("tests-normal", ["-B", "-m", "unittest", "-v"]),
        ("tests-O", ["-B", "-O", "-m", "unittest", "-v"]),
        ("tests-OO", ["-B", "-OO", "-m", "unittest", "-v"]),
        ("enumeration-normal", ["-B", "enumerate_cases.py"]),
        ("enumeration-O", ["-B", "-O", "enumerate_cases.py"]),
        ("enumeration-OO", ["-B", "-OO", "enumerate_cases.py"]),
        ("notebook-build", ["-B", "build_notebook.py"]),
        ("notebook-stdlib", ["-B", "execute_notebook.py"]),
    ]
    status, enumeration_hashes = [], []
    for name, arguments in jobs:
        command = "python3 " + " ".join(arguments)
        result = subprocess.run([sys.executable, *arguments], text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        output = result.stdout.replace(str(root), ".").replace(sys.executable, "python3")
        log = f"$ {command}\n{output}\nExit code: {result.returncode}\n"
        Path(f"logs/{name}.log").write_text(log, encoding="utf-8")
        status.append({"name": name, "command": command, "exit_code": result.returncode,
                       "log": f"logs/{name}.log"})
        print(f"{name}: {'PASS' if result.returncode == 0 else 'FAIL'}")
        if result.returncode != 0:
            print(output)
            raise SystemExit(result.returncode)
        if name.startswith("enumeration-"):
            enumeration_hashes.append(hashlib.sha256(Path("results/enumeration.json").read_bytes()).hexdigest())
    if len(set(enumeration_hashes)) != 1:
        raise RuntimeError("Enumeration results differ across normal/-O/-OO")
    test_counts = [int(re.search(r"Ran (\d+) tests", Path(f"logs/tests-{mode}.log").read_text()).group(1))
                   for mode in ("normal", "O", "OO")]
    if len(set(test_counts)) != 1:
        raise RuntimeError("Unit-test counts differ between optimization modes")
    notebook = json.loads(Path("euclid_i4_tutorial.ipynb").read_text(encoding="utf-8"))
    cell_count = notebook["metadata"]["reproduction"]["executed_code_cells"]
    report = {"jobs": status, "all_passed": True,
              "enumeration_sha256_by_mode": dict(zip(("normal", "O", "OO"), enumeration_hashes)),
              "enumeration_identical_across_optimization_modes": True,
              "unit_test_methods_per_mode": test_counts[0],
              "notebook_execution": f"{cell_count} Python code cells, stdlib compile/exec; not a Jupyter kernel"}
    Path("results/verification.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    # The independent reviewer owns that subtree and its separate evidence.
    # Never bind a partially written reviewer file into this generated manifest.
    files = sorted(path for path in Path(".").rglob("*") if path.is_file()
                   and "__pycache__" not in path.parts and "independent-review" not in path.parts
                   and path.name != "SHA256SUMS.txt")
    Path("SHA256SUMS.txt").write_text("".join(
        hashlib.sha256(path.read_bytes()).hexdigest() + "  " + path.as_posix() + "\n"
        for path in files), encoding="utf-8")
    print("All commands passed; enumeration JSON identical across three optimization modes.")


if __name__ == "__main__":
    main()
