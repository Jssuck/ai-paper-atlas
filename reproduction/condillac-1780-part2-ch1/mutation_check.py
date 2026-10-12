"""Curated semantic mutations and deliberately separate harness controls.

No mutation changes release source. Each isolated subprocess must finish exactly
all 40 expected tests at the requested optimization level. A semantic kill is
assertion failure with zero test errors, skips, or other abnormal outcomes.
"""
import ast
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
MODES = {"normal": [], "O": ["-O"], "OO": ["-OO"]}
MUTATIONS = {
    "evidence_union": ("current = current & compatible", "current = current | compatible"),
    "evidence_forgets_previous": ("current = current & compatible", "current = compatible"),
    "initial_coverage_ignored": (
        'current = universe if initial is None else _subset(initial, universe, "initial")',
        'current = universe if initial is None else (_subset(initial, universe, "initial") | universe)'),
    "foreign_labels_allowed": ("if not result <= universe:", "if False:"),
    "empty_rule_body_allowed": ("if not body:", "if False:"),
    "conjunction_becomes_disjunction": ("if rule.body <= state", "if bool(rule.body & state)"),
    "conjunctive_rules_ignored": ("if rule.body <= state", "if rule.body <= state and len(rule.body) == 1"),
    "anchors_ignored": ("return (anchors | derived) - withdrawn", "return frozenset(derived) - withdrawn"),
    "withdrawal_ignored": ("return anchors, withdrawn", "return anchors, frozenset()"),
    "old_state_is_own_support": ("return (anchors | derived) - withdrawn", "return (state | anchors | derived) - withdrawn"),
    "least_starts_at_top": (
        'current = frozenset() if kind == "least" else self.claims - withdrawn',
        'current = self.claims - withdrawn'),
    "greatest_starts_at_bottom": (
        'current = frozenset() if kind == "least" else self.claims - withdrawn',
        'current = frozenset()'),
    "iteration_stops_early": ("if following == current:", "if following == current or len(states) > 1:"),
}
RUNNER = r'''
import io, json, sys, traceback, unittest
try:
    import test_model
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_model)
    if "--empty" in sys.argv:
        suite = unittest.TestSuite()
    class TrackedResult(unittest.TextTestResult):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.started = []
            self.completed = []
        def startTest(self, test):
            self.started.append(test.id())
            super().startTest(test)
        def stopTest(self, test):
            self.completed.append(test.id())
            super().stopTest(test)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2, resultclass=TrackedResult).run(suite)
    print(stream.getvalue())
    payload = {"stage": "complete", "tests": result.testsRun,
               "started": result.started, "completed": result.completed,
               "failures": len(result.failures), "errors": len(result.errors),
               "skips": len(result.skipped), "expected_failures": len(result.expectedFailures),
               "unexpected_successes": len(result.unexpectedSuccesses),
               "optimization": sys.flags.optimize}
    print("RESULT_JSON=" + json.dumps(payload, sort_keys=True))
    if "--duplicate" in sys.argv:
        print("RESULT_JSON=" + json.dumps(payload, sort_keys=True))
    sys.exit(0 if result.wasSuccessful() else 1)
except Exception:
    traceback.print_exc()
    print('RESULT_JSON={"stage":"bootstrap_error"}')
    sys.exit(2)
'''


def expected_test_ids():
    tree = ast.parse((ROOT / "test_model.py").read_text(encoding="utf-8"))
    if any(isinstance(node, ast.Assert) for node in ast.walk(tree)):
        raise RuntimeError("Bare assert in tests would disappear under optimization")
    names = sorted(f"test_model.{group.name}.{method.name}"
                   for group in tree.body if isinstance(group, ast.ClassDef)
                   for method in group.body if isinstance(method, ast.FunctionDef)
                   and method.name.startswith("test_"))
    if len(names) != 40 or len(set(names)) != len(names):
        raise RuntimeError("Expected exactly 40 distinct author test methods")
    return names


def classify(returncode, stdout, expected_ids, optimization):
    markers = [line[len("RESULT_JSON="):] for line in stdout.splitlines()
               if line.startswith("RESULT_JSON=")]
    if len(markers) != 1:
        return "harness_error", None
    try:
        summary = json.loads(markers[0])
    except json.JSONDecodeError:
        return "harness_error", None
    if not isinstance(summary, dict) or summary.get("stage") != "complete":
        return "harness_error", summary
    numeric = ("tests", "failures", "errors", "skips", "expected_failures",
               "unexpected_successes", "optimization")
    if any(type(summary.get(key)) is not int or summary[key] < 0 for key in numeric):
        return "harness_error", summary
    if summary["optimization"] != optimization:
        return "harness_error", summary
    if (summary["tests"] != len(expected_ids) or summary.get("started") != expected_ids
            or summary.get("completed") != expected_ids):
        return "suite_mismatch", summary
    if summary["errors"]:
        return "test_error", summary
    if any(summary[key] for key in ("skips", "expected_failures", "unexpected_successes")):
        return "suite_mismatch", summary
    if returncode == 1 and summary["failures"] > 0:
        return "behavioral_kill", summary
    if returncode == 0 and summary["failures"] == 0:
        return "pass", summary
    return "harness_error", summary


def run_case(source, flags, name, directory, expected_ids, extra=(), timeout=10):
    with tempfile.TemporaryDirectory(prefix=".mutation-", dir=ROOT) as temp:
        target = Path(temp)
        (target / "model.py").write_text(source, encoding="utf-8")
        for filename in ("demo.py", "test_model.py"):
            shutil.copyfile(ROOT / filename, target / filename)
        (target / "_runner.py").write_text(RUNNER, encoding="utf-8")
        command = [sys.executable, *flags, "-B", "_runner.py", *extra]
        try:
            process = subprocess.run(command, cwd=target, text=True, capture_output=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            (directory / f"{name}.log").write_text(f"Actual subprocess timeout after {timeout} seconds.\n", encoding="utf-8")
            return {"name": name, "classification": "timeout", "returncode": None, "summary": None}
        stdout = process.stdout.replace(str(target), "ISOLATED_TEST_COPY")
        stderr = process.stderr.replace(str(target), "ISOLATED_TEST_COPY")
        (directory / f"{name}.log").write_text(stdout + stderr, encoding="utf-8")
        classification, summary = classify(process.returncode, stdout, expected_ids,
                                           0 if not flags else len(flags[0]) - 1)
        return {"name": name, "classification": classification,
                "returncode": process.returncode, "summary": summary}


def main():
    source = (ROOT / "model.py").read_text(encoding="utf-8")
    ids = expected_test_ids()
    output = ROOT / "logs" / "mutation"
    output.mkdir(parents=True, exist_ok=True)
    report = {"author_check": True, "expected_tests": len(ids), "bare_asserts_in_tests": 0,
              "mutants_per_mode": len(MUTATIONS), "modes": {}}
    success = True
    for mode, flags in MODES.items():
        directory = output / mode
        directory.mkdir(exist_ok=True)
        baseline = run_case(source, flags, "baseline", directory, ids)
        if baseline["classification"] != "pass":
            success = False
            report["modes"][mode] = {"baseline": baseline}
            continue
        mutants = []
        for name, (before, after) in MUTATIONS.items():
            if source.count(before) != 1:
                raise RuntimeError(f"Mutation {name}: expected exactly one source location")
            mutants.append(run_case(source.replace(before, after), flags, name, directory, ids))
        controls = [
            ("syntax_error", source + "\ndef broken(:\n", (), 10, "harness_error"),
            ("import_error", 'raise ImportError("intentional control")\n' + source, (), 10, "harness_error"),
            ("early_exit", 'raise SystemExit(0)\n' + source, (), 10, "harness_error"),
            ("empty_suite", source, ("--empty",), 10, "suite_mismatch"),
            ("duplicate_marker", source, ("--duplicate",), 10, "harness_error"),
            ("runtime_error", source.replace("derived = {rule.head", 'raise RuntimeError("intentional control")\n        derived = {rule.head'), (), 10, "test_error"),
            ("actual_timeout", 'import time\ntime.sleep(3)\n' + source, (), 0.25, "timeout"),
        ]
        control_results = []
        for name, changed, extra, timeout, expected in controls:
            result = run_case(changed, flags, name, directory, ids, extra, timeout)
            result["expected_classification"] = expected
            result["correctly_classified"] = result["classification"] == expected
            control_results.append(result)
        kills = sum(item["classification"] == "behavioral_kill" for item in mutants)
        controls_ok = all(item["correctly_classified"] for item in control_results)
        success = success and kills == len(MUTATIONS) and controls_ok
        report["modes"][mode] = {"baseline": baseline, "behavioral_kills": kills,
                                  "mutants": mutants, "controls": control_results,
                                  "control_checks_passed": controls_ok}
    report["success"] = success
    (output / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"success": success, "mutants_per_mode": len(MUTATIONS),
                      "expected_tests": len(ids), "modes": {
                          mode: {"baseline": record["baseline"]["classification"],
                                 "behavioral_kills": record.get("behavioral_kills", 0),
                                 "controls_ok": record.get("control_checks_passed", False)}
                          for mode, record in report["modes"].items()}}, indent=2))
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
