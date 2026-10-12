"""Eight targeted behavior mutations plus five failure-classification controls.

Each mutant runs only its named sentinel test in an isolated temporary copy.
No mutant is counted as caught unless that test finishes with assertion failures
and no test errors. Syntax/import failures, early exit, and timeout are separate.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
MARKER = "__MUTATION_RECORD__="
HARNESS = r'''
import json, sys, traceback, unittest
MARKER = "__MUTATION_RECORD__="
try:
    import test_model
except BaseException as exc:
    traceback.print_exc()
    print(MARKER + json.dumps({"phase": "import", "type": type(exc).__name__}))
    sys.exit(3)
class Tracked(unittest.TextTestResult):
    started = 0
    finished = 0
    def startTest(self, test):
        self.started += 1
        super().startTest(test)
    def stopTest(self, test):
        self.finished += 1
        super().stopTest(test)
suite = unittest.defaultTestLoader.loadTestsFromName(sys.argv[1], test_model)
result = unittest.TextTestRunner(verbosity=2, resultclass=Tracked).run(suite)
print(MARKER + json.dumps({"phase": "done", "run": result.testsRun,
    "started": result.started, "finished": result.finished,
    "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped)}))
sys.exit(0 if result.wasSuccessful() else 1)
'''
MUTATIONS = (
    ("ignore_context_edges", "and all(a in prefix for a, b in frozen_edges if b == feature)", "and True",
     "test_context_order_set"),
    ("forget_last_observation", "[:len(observed)] == observed", "[:max(0, len(observed)-1)] == observed[:-1]",
     "test_prefix_counts"),
    ("erase_multiplicity", "Counter(self._message(message))", "Counter(set(self._message(message)))",
     "test_aggregate_keeps_multiplicity"),
    ("erase_feature_binding", "return frozenset(zip(self.labels, self._message(message)))",
     'return frozenset(("ignored", value) for value in self._message(message))', "test_unlabeled_collision"),
    ("claim_every_dictionary_injective", "return len({token for _, token in self.lexicon}) == len(self.lexicon)",
     "return True", "test_colliding_dictionary"),
    ("reverse_decoded_values", "return next(iter(compatible))", "return tuple(reversed(next(iter(compatible))))",
     "test_round_trip_alternate_order"),
    ("erase_frame_boundaries", '_strings(tokens, "tokens"), ensure_ascii=False',
     '"".join(_strings(tokens, "tokens")), ensure_ascii=False', "test_framing_distinguishes_boundaries"),
    ("accept_any_example", "if all(table[index] == value for index, value in observations)",
     "if any(table[index] == value for index, value in observations)", "test_all_analogy_examples_applied"),
)


def classify(returncode, stdout, timed_out=False):
    if timed_out:
        return "timeout"
    records = [line[len(MARKER):] for line in stdout.splitlines() if line.startswith(MARKER)]
    if len(records) != 1:
        return "harness_failure"
    try:
        record = json.loads(records[0])
    except (ValueError, TypeError):
        return "harness_failure"
    if record.get("phase") == "import":
        if returncode != 3:
            return "harness_failure"
        return "syntax_failure" if record.get("type") in ("SyntaxError", "IndentationError", "TabError") else "import_failure"
    if (record.get("phase") != "done" or any(record.get(key) != 1 for key in ("run", "started", "finished"))
            or record.get("skipped") != 0):
        return "harness_failure"
    if record.get("errors", 0):
        return "test_error" if returncode == 1 else "harness_failure"
    if record.get("failures", 0):
        return "behavior_caught" if returncode == 1 else "harness_failure"
    return "survived" if returncode == 0 else "harness_failure"


def run_case(source, test, flags, timeout=10):
    with tempfile.TemporaryDirectory(prefix="condillac-mutation-") as name:
        folder = Path(name)
        (folder / "model.py").write_text(source, encoding="utf-8")
        (folder / "test_model.py").write_text((ROOT / "test_model.py").read_text(encoding="utf-8"), encoding="utf-8")
        command = [sys.executable, *flags, "-B", "-c", HARNESS, "LanguageTests." + test]
        try:
            result = subprocess.run(command, cwd=folder, capture_output=True, text=True, timeout=timeout)
            return {"outcome": classify(result.returncode, result.stdout), "exit_code": result.returncode,
                    "stdout": result.stdout.replace(str(folder), "${MUTATION_DIR}"),
                    "stderr": result.stderr.replace(str(folder), "${MUTATION_DIR}")}
        except subprocess.TimeoutExpired as exc:
            def txt(value):
                return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else (value or "")
            return {"outcome": classify(None, "", True), "exit_code": None,
                    "stdout": txt(exc.stdout).replace(str(folder), "${MUTATION_DIR}"),
                    "stderr": txt(exc.stderr).replace(str(folder), "${MUTATION_DIR}")}


def verify(mode):
    flags = {"normal": [], "O": ["-O"], "OO": ["-OO"]}[mode]
    source = (ROOT / "model.py").read_text(encoding="utf-8")
    cases = []
    # One positive baseline for every targeted sentinel, not merely one smoke test.
    for name, old, new, test in MUTATIONS:
        if source.count(old) != 1:
            raise RuntimeError(f"mutation anchor {name} is not unique")
        for kind, text, expected in (("baseline", source, "survived"),
                                     ("mutation", source.replace(old, new), "behavior_caught")):
            cases.append({"name": name, "kind": kind, "test": test, "expected": expected,
                          **run_case(text, test, flags)})
    controls = (
        ("syntax", "def broken(:\n", "syntax_failure", 10),
        ("import", "import nonexistent_condillac_control_module\n", "import_failure", 10),
        ("early_exit", "import os; os._exit(0)\n", "harness_failure", 10),
        ("timeout", "import time; time.sleep(10)\n", "timeout", 0.2),
        ("test_runtime_error", source.replace('observed = _strings(prefix, "prefix")',
                                             'raise RuntimeError("intentional test-error control")'), "test_error", 10),
    )
    for name, changed, expected, timeout in controls:
        cases.append({"name": name, "kind": "control", "test": "test_prefix_counts", "expected": expected,
                      **run_case(changed, "test_prefix_counts", flags, timeout)})
    return {"mode": mode, "mutation_count": len(MUTATIONS), "baseline_count": len(MUTATIONS),
            "control_count": len(controls), "passed": all(case["outcome"] == case["expected"] for case in cases),
            "cases": cases}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("normal", "O", "OO"), default="normal")
    result = verify(parser.parse_args().mode)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result["passed"] else 1)
