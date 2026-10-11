"""Recreate all result files without network access or third-party packages."""
import json
import platform
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"


def main():
    RESULTS.mkdir(exist_ok=True)
    environment = {"python_version": platform.python_version(),
                   "implementation": platform.python_implementation(),
                   "platform": platform.system(), "machine": platform.machine(),
                   "third_party_dependencies": [],
                   "execution": "local CPU; no network; no install step"}
    (RESULTS / "environment.json").write_text(json.dumps(environment, indent=2) + "\n", encoding="utf-8")
    cases = [("tests-normal.log", ["test_model.py"]),
             ("tests-O.log", ["-O", "test_model.py"]),
             ("tests-OO.log", ["-OO", "test_model.py"]),
             ("demo.json", ["demo.py"]),
             ("mutations.json", ["mutation_check.py"])]
    records = []
    for filename, arguments in cases:
        run = subprocess.run([sys.executable, *arguments], cwd=ROOT,
                             text=True, capture_output=True, timeout=120)
        if filename.endswith(".json"):
            output = run.stdout
            if run.returncode == 0:
                json.loads(output)
            if run.stderr:
                (RESULTS / (filename + ".stderr.log")).write_text(run.stderr, encoding="utf-8")
        else:
            output = run.stdout + run.stderr
        (RESULTS / filename).write_text(output, encoding="utf-8")
        records.append({"command": "python " + " ".join(arguments),
                        "result_file": "results/" + filename, "exit_code": run.returncode})
        print(f"{'PASS' if run.returncode == 0 else 'FAIL'} python {' '.join(arguments)} -> results/{filename}")
    summary = {"runs": records, "all_passed": all(row["exit_code"] == 0 for row in records)}
    (RESULTS / "run-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    if not summary["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
