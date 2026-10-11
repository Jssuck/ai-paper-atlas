"""Curated semantic mutation checks, with separate infrastructure-error accounting.

Each mutant is an exact one-site edit to a temporary copy. No source or tests are
changed in the release. A behavior kill requires the full expected test-ID set,
40 completed methods, assertion failures, ZERO test errors and ZERO skips.
Syntax/import failures, timeouts, missing markers, and unexpected suite sizes do
not earn credit. Self-check controls exercise those non-kill classifications.
"""
import argparse
import ast
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
EXPECTED_TESTS = 40
MODES = {"normal": [], "O": ["-O"], "OO": ["-OO"]}
MUTATIONS = {
    "reinforcement_ignores_amount": ('self._weights.get(edge, 0) + amount', 'self._weights.get(edge, 0) + 1'),
    "ties_choose_first": ('if len(winners) != 1:', 'if False:'),
    "weakest_wins_recall": ('maximum = max(weight for _, weight in row)', 'maximum = min(weight for _, weight in row)'),
    "forgetting_disabled": ('remaining = max(0, self._weights[edge] - steps)', 'remaining = self._weights[edge]'),
    "evict_newest_tie": ('(self._weights[e], self._born[e])', '(self._weights[e], -self._born[e])'),
    "capacity_off_by_one": ('len(self._weights) > self.capacity:', 'len(self._weights) > self.capacity + 1:'),
    "context_ignored_on_recall": ('self.habits.choose((context, output[-1]))', 'self.habits.choose(("", output[-1]))'),
    "terminal_becomes_self_loop": ('successors = tokens[1:] + (None,)', 'successors = tokens[1:] + tokens[-1:]'),
    "replay_labeled_external": ('self.active = IdeaEvent(token, "replay")', 'self.active = IdeaEvent(token, "external")'),
    "feedback_labeled_external": ('return self._receive(body.signal, context, "feedback")', 'return self._receive(body.signal, context, "external")'),
    "clear_erases_dispositions": ('def clear_active(self) -> None:\n        self.active = None', 'def clear_active(self) -> None:\n        self.active = None\n        self.brain.habits.forget(10**9)'),
    "incoming_gate_ignored": ('if not self.afferent_enabled:', 'if False:'),
    "outgoing_gate_ignored": ('if self.active is None or not self.efferent_enabled:', 'if self.active is None:'),
    "peripheral_forgetting_ignored": ('for table in (self.brain.habits, self.incoming, self.outgoing):', 'for table in (self.brain.habits,):'),
    "budget_off_by_one": ('for _ in range(max_transitions):', 'for _ in range(max_transitions + 1):'),
}
RUNNER = r'''
import io, json, sys, traceback, unittest
try:
    import test_model
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_model)
    if "--empty-suite" in sys.argv:
        suite = unittest.TestSuite()
    def ids(node):
        out = []
        for item in node:
            out.extend(ids(item) if isinstance(item, unittest.TestSuite) else [item.id()])
        return out
    names = ids(suite)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    print(stream.getvalue())
    summary = {"stage": "complete", "tests": result.testsRun, "ids": names,
               "failures": len(result.failures), "errors": len(result.errors),
               "skipped": len(result.skipped), "optimized": sys.flags.optimize}
    print("RESULT_JSON=" + json.dumps(summary, sort_keys=True))
    sys.exit(0 if result.wasSuccessful() else 1)
except Exception:
    traceback.print_exc()
    print("RESULT_JSON=" + json.dumps({"stage": "bootstrap_error"}))
    sys.exit(2)
'''


def classify(returncode, summary, expected_ids):
    if summary is None:
        return "harness_error"
    if summary.get("stage") != "complete":
        return "harness_error"
    if summary.get("tests") != EXPECTED_TESTS or summary.get("ids") != expected_ids:
        return "suite_mismatch"
    if summary.get("errors", 0):
        return "test_error"
    if summary.get("skipped", 0):
        return "suite_mismatch"
    failures = summary.get("failures", 0)
    if returncode == 1 and failures > 0:
        return "behavioral_kill"
    if returncode == 0 and failures == 0:
        return "pass"
    return "harness_error"


def run_copy(source, flags, output, name, expected_ids, extra=()):
    with tempfile.TemporaryDirectory(prefix=".mutation-", dir=ROOT) as directory:
        target = Path(directory)
        (target / "model.py").write_text(source, encoding="utf-8")
        for filename in ("test_model.py", "demo.py"):
            shutil.copyfile(ROOT / filename, target / filename)
        (target / "_runner.py").write_text(RUNNER, encoding="utf-8")
        command = [sys.executable, *flags, "-B", "_runner.py", *extra]
        try:
            proc = subprocess.run(command, cwd=target, text=True, capture_output=True, timeout=20)
        except subprocess.TimeoutExpired as error:
            (output / f"{name}.log").write_text("Timed out after 20 seconds in isolated test copy.\n", encoding="utf-8")
            return {"name": name, "classification": "timeout", "summary": None}
        raw = (proc.stdout + proc.stderr).replace(str(target), "ISOLATED_TEST_COPY")
        (output / f"{name}.log").write_text(raw, encoding="utf-8")
        matches = [line[len("RESULT_JSON="):] for line in proc.stdout.splitlines()
                   if line.startswith("RESULT_JSON=")]
        try:
            summary = json.loads(matches[-1]) if len(matches) == 1 else None
        except json.JSONDecodeError:
            summary = None
        ids = expected_ids if expected_ids is not None else (summary or {}).get("ids")
        return {"name": name, "classification": classify(proc.returncode, summary, ids),
                "returncode": proc.returncode, "summary": summary}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="logs/mutation")
    args = parser.parse_args()
    output = ROOT / args.output
    output.mkdir(parents=True, exist_ok=True)
    source = (ROOT / "model.py").read_text(encoding="utf-8")
    test_tree = ast.parse((ROOT / "test_model.py").read_text(encoding="utf-8"))
    bare_asserts = sum(isinstance(node, ast.Assert) for node in ast.walk(test_tree))
    if bare_asserts:
        raise RuntimeError("Bare assert statements would disappear in optimized tests")
    report = {"expected_tests_per_run": EXPECTED_TESTS, "bare_asserts_in_tests": bare_asserts,
              "curated_mutants_per_mode": len(MUTATIONS), "modes": {}}
    all_ok = True
    expected_ids = None
    for mode, flags in MODES.items():
        directory = output / mode
        directory.mkdir(exist_ok=True)
        baseline = run_copy(source, flags, directory, "baseline", expected_ids)
        if baseline["classification"] != "pass":
            report["modes"][mode] = {"baseline": baseline}
            all_ok = False
            continue
        expected_ids = baseline["summary"]["ids"]
        mutants = []
        for name, (old, new) in MUTATIONS.items():
            if source.count(old) != 1:
                raise RuntimeError(f"Mutation {name} must match exactly one source site")
            mutants.append(run_copy(source.replace(old, new), flags, directory, name, expected_ids))
        controls = [
            run_copy(source + "\ndef broken(:\n", flags, directory, "control_syntax", expected_ids),
            run_copy('raise ImportError("intentional control")\n' + source, flags, directory,
                     "control_import", expected_ids),
            run_copy(source, flags, directory, "control_empty_suite", expected_ids, ("--empty-suite",)),
            run_copy(source.replace('row = [(value, weight)',
                                    'raise RuntimeError("intentional test error")\n        row = [(value, weight)'),
                     flags, directory, "control_runtime_error", expected_ids),
        ]
        expected_controls = ["harness_error", "harness_error", "suite_mismatch", "test_error"]
        controls_ok = [r["classification"] for r in controls] == expected_controls
        kills = sum(r["classification"] == "behavioral_kill" for r in mutants)
        all_ok = all_ok and kills == len(MUTATIONS) and controls_ok
        report["modes"][mode] = {"baseline": baseline, "behavioral_kills": kills,
                                  "mutants": mutants, "controls": controls,
                                  "control_checks_passed": controls_ok}
    report["success"] = all_ok
    (output / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    compact = {"success": all_ok, "bare_asserts_in_tests": bare_asserts,
               "modes": {mode: {"baseline_tests": data["baseline"].get("summary", {}).get("tests"),
                                 "behavioral_kills": data.get("behavioral_kills", 0),
                                 "control_checks_passed": data.get("control_checks_passed", False)}
                         for mode, data in report["modes"].items()}}
    print(json.dumps(compact, indent=2))
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
