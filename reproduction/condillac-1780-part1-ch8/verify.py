"""Re-run every check, keeping genuine local logs and a source fingerprint."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"


def main():
    RESULTS.mkdir(exist_ok=True)
    environment = {
        "run_started_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform": platform.system(), "machine": platform.machine(),
        "third_party_dependencies": [],
        "execution": "local CPU; no network; no installation",
        "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                          for name in ("model.py", "test_model.py", "demo.py", "mutation_check.py", "verify.py",
                                       "independent-review/review_model.py", "independent-review/mutation_review.py")},
    }
    (RESULTS / "environment.json").write_text(json.dumps(environment, indent=2) + "\n", encoding="utf-8")
    runs = [
        ("tests-normal.log", ["test_model.py"]),
        ("tests-O.log", ["-O", "test_model.py"]),
        ("tests-OO.log", ["-OO", "test_model.py"]),
        ("demo.json", ["demo.py"]),
        ("mutations-normal.json", ["mutation_check.py"]),
        ("mutations-O.json", ["-O", "mutation_check.py"]),
        ("mutations-OO.json", ["-OO", "mutation_check.py"]),
    ]
    for label, flags in (("normal", []), ("O", ["-O"]), ("OO", ["-OO"])):
        runs.append(("independent-review-" + label + ".json", [*flags, "independent-review/review_model.py"]))
        runs.append(("independent-mutations-" + label + ".json", [*flags, "independent-review/mutation_review.py"]))
    records = []
    for filename, arguments in runs:
        try:
            run = subprocess.run([sys.executable, "-B", *arguments], cwd=ROOT,
                                 text=True, capture_output=True, timeout=600)
            code = run.returncode
            output = run.stdout + run.stderr if filename.endswith(".log") else run.stdout
            validation = None
            if filename.endswith(".json"):
                try:
                    parsed = json.loads(run.stdout)
                    if filename.startswith("independent-") and parsed.get("status") != "PASS":
                        validation = "independent audit did not report PASS"
                except ValueError:
                    validation = "invalid JSON output"
                if run.stderr:
                    (RESULTS / (filename + ".stderr.log")).write_text(run.stderr, encoding="utf-8")
            (RESULTS / filename).write_text(output, encoding="utf-8")
            record = {"command": "python " + " ".join(arguments), "exit_code": code,
                      "result_file": "results/" + filename, "output_validation_error": validation,
                      "passed": code == 0 and validation is None}
        except (OSError, subprocess.TimeoutExpired) as error:
            record = {"command": "python " + " ".join(arguments), "passed": False,
                      "exception": type(error).__name__}
        records.append(record)
        print(f"{'PASS' if record['passed'] else 'FAIL'} {record['command']} -> results/{filename}")
    summary = {"runs": records, "all_passed": all(row["passed"] for row in records)}
    (RESULTS / "run-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return 0 if summary["all_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
