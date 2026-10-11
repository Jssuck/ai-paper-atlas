"""Eight explicit semantic mutations; each must cause a unittest failure.

A crash, syntax error, timeout or an unexecuted test does not count as a kill.
Temporary copies stay under this reproduction folder and are removed afterward.
"""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
MUTANTS = (
    ("unknown_as_equal", 'return "unknown"', 'return "equal"'),
    ("ignore_selected_features", 'indices = tuple(catalog.features.index(f) for f in features)',
     'indices = tuple(range(len(catalog.features)))'),
    ("invent_catalog_witnesses", 'if all(actual[catalog.features.index(f)] == v for f, v in attributes)',
     'if True'),
    ("disjunction_instead_of_conjunction", 'all(p in known for p in rule.premises)',
     'any(p in known for p in rule.premises)'),
    ("unfounded_initial_proof", 'steps = [Step(atom) for atom in theory.facts]',
     'steps = [Step(atom) for atom in theory.atoms]'),
    ("skip_certificate_dependencies", 'if not set(rule.premises).issubset(known):',
     'if False:'),
    ("ignore_certificate_conclusion", 'if rule is None or rule.conclusion != step.atom:',
     'if rule is None:'),
    ("reverse_semantic_implication", 'if antecedent and not valuation[rule.conclusion]:',
     'if valuation[rule.conclusion] and not antecedent:'),
)


def main():
    source = (ROOT / "model.py").read_text(encoding="utf-8")
    tests = (ROOT / "test_model.py").read_text(encoding="utf-8")
    baseline = subprocess.run([sys.executable, "test_model.py"], cwd=ROOT,
                              text=True, capture_output=True, timeout=60)
    if baseline.returncode != 0 or "Ran 18 tests" not in baseline.stderr:
        raise RuntimeError("baseline did not pass all 18 tests")
    results = []
    for name, before, after in MUTANTS:
        if source.count(before) != 1:
            raise RuntimeError(f"mutation target must occur exactly once: {name}")
        with tempfile.TemporaryDirectory(prefix=".mutation-", dir=ROOT) as folder:
            work = Path(folder)
            (work / "model.py").write_text(source.replace(before, after), encoding="utf-8")
            (work / "test_model.py").write_text(tests, encoding="utf-8")
            run = subprocess.run([sys.executable, "test_model.py"], cwd=work,
                                 text=True, capture_output=True, timeout=60)
            failures = [line for line in run.stderr.splitlines() if line.startswith("FAIL:")]
            killed = (run.returncode == 1 and bool(failures)
                      and "Ran 18 tests" in run.stderr and "ERROR:" not in run.stderr)
            results.append({"mutation": name, "killed_by_behavioral_failure": killed,
                            "exit_code": run.returncode, "failing_tests": failures})
    print(json.dumps({"baseline": "18 tests passed", "mutations": results,
                      "killed": sum(row["killed_by_behavioral_failure"] for row in results),
                      "total": len(results)}, indent=2))
    if not all(row["killed_by_behavioral_failure"] for row in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
