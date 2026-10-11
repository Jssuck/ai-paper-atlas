"""Run real, isolated semantic mutants against unchanged unit tests.

Only a completed run with assertion failures (and no test errors) kills a mutant.
A syntax/import failure is a broken experiment, not a successful mutation kill.
"""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
MUTATIONS = (
    ("any_answer_means_identified", "finite_model.py",
     'status = "identified" if len(values) == 1 else "ambiguous"',
     'status = "identified" if len(values) >= 1 else "ambiguous"'),
    ("empty_fiber_means_identified", "finite_model.py",
     'return Answer("inconsistent", (), ())', 'return Answer("identified", (), ())'),
    ("names_become_observations", "finite_model.py",
     'return FiniteModel(self.columns, self.states, self.signatures,\n                           tuple(labels[state] for state in self.states))',
     'return FiniteModel(self.columns, self.states,\n                           tuple(tuple(i for _ in self.columns) for i in range(len(self.states))),\n                           tuple(labels[state] for state in self.states))'),
    ("new_probe_erases_old_data", "finite_model.py",
     'rows = tuple(row + (values[state],)', 'rows = tuple((0,) * len(row) + (values[state],)'),
    ("ignore_known_gain", "ratios.py", 'return result.product / gain', 'return result.product / Fraction(1)'),
    ("break_parameter_symmetry", "ratios.py", 'return coefficient * scale, gain / scale', 'return coefficient * scale, gain * scale'),
    ("zero_inputs_identify_product", "ratios.py",
     'return ProductInference("uninformative", None)', 'return ProductInference("identified", Fraction(1))'),
    ("ignore_conflicting_measurements", "ratios.py",
     'if len(ratios) != 1 or next(iter(ratios)) <= 0:', 'if next(iter(ratios)) <= 0:'),
    ("invert_relative_measurement", "ratios.py", 'return a.product / b.product', 'return b.product / a.product'),
)


def tests_in(path):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0")
    return subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
                          cwd=path, env=env, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, timeout=60)


def run():
    baseline = tests_in(ROOT)
    if baseline.returncode:
        raise RuntimeError("baseline unit tests failed; no mutation result is valid\n" + baseline.stdout)
    results = []
    details = ["BASELINE\n" + baseline.stdout]
    for name, filename, old, new in MUTATIONS:
        with tempfile.TemporaryDirectory(prefix=".mutation-", dir=ROOT) as folder:
            temp = Path(folder)
            for source in ("finite_model.py", "ratios.py", "demo.py"):
                shutil.copyfile(ROOT / source, temp / source)
            shutil.copytree(ROOT / "tests", temp / "tests", ignore=shutil.ignore_patterns("__pycache__"))
            path = temp / filename
            source = path.read_text(encoding="utf-8")
            if source.count(old) != 1:
                raise RuntimeError(f"mutation anchor is not unique: {name}")
            path.write_text(source.replace(old, new), encoding="utf-8")
            compile(path.read_text(encoding="utf-8"), filename, "exec")
            result = tests_in(temp)
            failures = len(re.findall(r"^FAIL:", result.stdout, re.MULTILINE))
            errors = len(re.findall(r"^ERROR:", result.stdout, re.MULTILINE))
            killed = result.returncode == 1 and failures > 0 and errors == 0
            results.append({"mutation": name, "exit_code": result.returncode,
                            "assertion_failures": failures, "test_errors": errors,
                            "result": "KILLED" if killed else "NOT_KILLED"})
            details.append(f"\nMUTANT {name}\n" + result.stdout)
    logs = ROOT / "logs"
    logs.mkdir(exist_ok=True)
    (logs / "mutation-details.txt").write_text("\n".join(details).replace(str(ROOT), "."), encoding="utf-8")
    summary = {"baseline": "PASS", "mutants": results,
               "result": "PASS" if all(r["result"] == "KILLED" for r in results) else "FAIL"}
    print(json.dumps(summary, indent=2))
    return summary["result"] == "PASS"


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
