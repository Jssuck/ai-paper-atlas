"""Semantic mutation checks, with harness failures distinguished from detection.

Only a completed suite with behavioral failures and no errors is detected.
An actual syntax-error control must be classified as a harness failure.
"""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
EXPECTED_TESTS = 27
MUTANTS = (
    ("lack_is_need", 'return self.lacking and self.known and (self.habitual_enjoyment or self.habitual_imagination)',
     'return self.lacking'),
    ("past_enjoyment_required", 'return self.lacking and self.known and (self.habitual_enjoyment or self.habitual_imagination)',
     'return self.lacking and self.known and self.habitual_enjoyment'),
    ("ignore_direction", 'return self.need and self.faculties_directed', 'return self.need'),
    ("erase_suspended_passion", 'return self.desire_habit', 'return self.desire_habit and self.desire'),
    ("allow_empty_support", 'if not self.support:', 'if False:'),
    ("existential_judgment", 'return all(getattr(w, predicate) for w in self.worlds if w.name in self.support)',
     'return any(getattr(w, predicate) for w in self.worlds if w.name in self.support)'),
    ("assume_actual_in_support", 'return all(getattr(w, predicate) for w in self.worlds if w.name in self.support)',
     'return all(getattr(w, predicate) for w in self.worlds if w.name in self.support or w.name == self.actual)'),
    ("ignore_experience_origin", 'return self.established and self.from_experience', 'return self.established'),
    ("ignore_established_habit", 'return self.established and self.from_experience', 'return self.from_experience'),
    ("equate_obtaining_and_no_obstacle", 'obstacle_judgment = beliefs.judges("obstacle_free")',
     'obstacle_judgment = beliefs.judges("obtains")'),
    ("reverse_bridge", 'return all((not w.obstacle_free) or w.obtains for w in self.worlds if w.name in self.support)',
     'return all((not w.obtains) or w.obstacle_free for w in self.worlds if w.name in self.support)'),
)


def classify(returncode, report):
    if not isinstance(report, dict):
        return "harness_failure"
    if (report.get("tests_run") != EXPECTED_TESTS or report.get("errors") != 0
            or report.get("skipped") != 0 or report.get("optimization") != sys.flags.optimize):
        return "harness_failure"
    if returncode == 0 and report.get("failures") == 0 and report.get("successful") is True:
        return "survived"
    if returncode == 1 and type(report.get("failures")) is int and report["failures"] > 0 and report.get("successful") is False:
        return "detected_by_behavior"
    return "harness_failure"


def run_suite(work):
    flags = ["-" + "O" * sys.flags.optimize] if sys.flags.optimize else []
    command = [sys.executable, *flags, "-B", "test_model.py"]
    try:
        run = subprocess.run(command, cwd=work, text=True, capture_output=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"status": "harness_failure", "exception": type(error).__name__}
    try:
        report = json.loads(run.stdout)
    except (ValueError, TypeError):
        report = None
    diagnostic = run.stderr.replace(str(work), "BASELINE_DIR" if work == ROOT else "MUTATION_WORKDIR")
    return {"status": classify(run.returncode, report), "exit_code": run.returncode,
            "test_report": report,
            "behavioral_failures": [line for line in diagnostic.splitlines() if line.startswith("FAIL:")],
            "errors": [line for line in diagnostic.splitlines() if line.startswith("ERROR:")],
            "stderr": diagnostic}


def main():
    source = (ROOT / "model.py").read_text(encoding="utf-8")
    tests = (ROOT / "test_model.py").read_text(encoding="utf-8")
    baseline = run_suite(ROOT)
    if baseline["status"] != "survived":
        print(json.dumps({"baseline": baseline, "all_semantic_mutations_detected": False}, indent=2))
        return 1
    results = []
    for name, before, after in MUTANTS:
        if source.count(before) != 1:
            results.append({"mutation": name, "status": "harness_failure",
                            "reason": "mutation target must occur exactly once"})
            continue
        with tempfile.TemporaryDirectory(prefix=".mutation-", dir=ROOT) as folder:
            work = Path(folder)
            (work / "model.py").write_text(source.replace(before, after), encoding="utf-8")
            (work / "test_model.py").write_text(tests, encoding="utf-8")
            results.append({"mutation": name, **run_suite(work)})
    with tempfile.TemporaryDirectory(prefix=".harness-control-", dir=ROOT) as folder:
        work = Path(folder)
        (work / "model.py").write_text("def broken(:\n", encoding="utf-8")
        (work / "test_model.py").write_text(tests, encoding="utf-8")
        control = run_suite(work)
    detected = sum(row["status"] == "detected_by_behavior" for row in results)
    success = detected == len(MUTANTS) and control["status"] == "harness_failure"
    report = {"optimization": sys.flags.optimize,
              "diagnostic_path_normalization": "Only execution-directory paths in stderr are replaced by BASELINE_DIR or MUTATION_WORKDIR; outcomes and diagnostic content are otherwise unchanged.",
              "baseline": baseline,
              "semantic_mutations": results, "detected": detected, "total": len(MUTANTS),
              "syntax_error_control": control,
              "control_correctly_rejected": control["status"] == "harness_failure",
              "all_semantic_mutations_detected": success}
    print(json.dumps(report, indent=2))
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
