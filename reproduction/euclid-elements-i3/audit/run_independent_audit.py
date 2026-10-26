"""Re-run original tests plus independent oracle without changing source/evidence.

All output written under audit/. Notebook execution occurs on disposable copies.
Published logs contain relative commands, no private paths.
"""
import ast
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audit"
PUBLISH = ROOT.parents[1]
ARTICLE = PUBLISH / "papers/ancient/euclid-elements-i3.zh-CN.md"


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(label, args, cwd=ROOT):
    command = "python " + " ".join(args)
    start = time.perf_counter()
    process = subprocess.run([sys.executable, *args], cwd=cwd,
                             env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                             text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (AUDIT / (label + ".log")).write_text(
        "$ " + command + "\n" + process.stdout + "\nexit_code: " + str(process.returncode) + "\n",
        encoding="utf-8")
    require(process.returncode == 0, "audit subprocess failed: " + label)
    return {"command": command, "exit_code": process.returncode,
            "wall_seconds": round(time.perf_counter() - start, 6),
            "log": "audit/" + label + ".log"}, process.stdout


def main():
    source_names = ("euclid_i3.py", "experiments.py", "test_euclid_i3.py", "execute_notebook.py",
                    "run_checks.py", "tutorial.ipynb", "README.md")
    selected = [ARTICLE] + [ROOT / x for x in source_names]
    selected += [AUDIT / "independent_oracle.py", Path(__file__).resolve()]
    before = {str(path.relative_to(PUBLISH)): sha(path) for path in selected}
    test_runs, oracle_runs, oracle_results, methods = {}, {}, {}, {}
    for mode, flags in (("normal", []), ("optimized", ["-O"]), ("double_optimized", ["-OO"])):
        record, output = run("original_" + mode, flags + ["-m", "unittest", "-v", "test_euclid_i3"])
        match = re.search(r"Ran (\d+) tests? in", output)
        require(match is not None, "test count absent: " + mode)
        record["tests_run"] = int(match.group(1))
        methods[mode] = re.findall(r"^(test_\S+) .*\.\.\. ok$", output, re.MULTILINE)
        require(len(methods[mode]) == record["tests_run"], "not all methods individually successful")
        test_runs[mode] = record
        record, output = run("oracle_" + mode, flags + ["audit/independent_oracle.py"])
        oracle_results[mode] = json.loads(output)
        require(oracle_results[mode]["status"] == "PASS", "oracle did not pass: " + mode)
        oracle_runs[mode] = record
    require(len({tuple(x) for x in methods.values()}) == 1, "test method coverage differs by optimization mode")
    require(oracle_results["normal"] == oracle_results["optimized"] == oracle_results["double_optimized"],
            "oracle result differs by optimization mode")
    original = json.loads((ROOT / "evidence/results.json").read_text(encoding="utf-8"))
    require(all(original["source_sha256"][name] == sha(ROOT / name) for name in source_names),
            "published evidence source hashes are stale")
    require(all(r["tests_run"] == original["unique_unittest_methods"] for r in test_runs.values()),
            "recorded test counts disagree")
    experiment_run, experiment_output = run("independent_experiments", ["experiments.py"])
    require(json.loads(experiment_output) == original["family_metrics"], "recorded experiment counts disagree")

    # The exercise's executor is re-run, but only on copies. Compare outputs
    # against published outputs, not merely successful exit status.
    with tempfile.TemporaryDirectory(prefix="euclid-i3-audit-") as temp:
        temp_path = Path(temp)
        for name in ("euclid_i3.py", "experiments.py", "execute_notebook.py", "tutorial.ipynb"):
            shutil.copyfile(ROOT / name, temp_path / name)
        notebook_run, _ = run("independent_notebook", ["execute_notebook.py"], temp_path)
        replay = json.loads((temp_path / "tutorial.ipynb").read_text(encoding="utf-8"))
    published = json.loads((ROOT / "tutorial.ipynb").read_text(encoding="utf-8"))
    require(replay == published, "notebook replay differs from published JSON")
    code_cells = [cell for cell in replay["cells"] if cell["cell_type"] == "code"]
    require(len(replay["cells"]) == 5 and len(code_cells) == 3, "notebook cell counts incorrect")
    require([c["execution_count"] for c in code_cells] == [1, 2, 3], "notebook order incorrect")
    after = {str(path.relative_to(PUBLISH)): sha(path) for path in selected}
    require(before == after, "audited source changed during audit")
    python_files = [ROOT / name for name in source_names if name.endswith(".py")]
    python_files += [AUDIT / "independent_oracle.py", Path(__file__).resolve()]
    assert_counts = {str(path.relative_to(PUBLISH)): sum(isinstance(n, ast.Assert)
                     for n in ast.walk(ast.parse(path.read_text(encoding="utf-8")))) for path in python_files}
    require(not any(assert_counts.values()), "assert statement found")
    report = {
        "status": "PASS", "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {"python_implementation": platform.python_implementation(),
                        "python_version": platform.python_version(), "os": platform.system(),
                        "architecture": platform.machine(), "dependencies_installed": [],
                        "notebook_related_modules_available": {
                            name: importlib.util.find_spec(name) is not None
                            for name in ("ipykernel", "nbclient", "nbformat")}},
        "original_tests_independently_rerun": test_runs,
        "original_test_method_names_identical_across_modes": True,
        "oracle_runs": oracle_runs, "oracle_results_identical_across_modes": True,
        "oracle_result": oracle_results["normal"],
        "recorded_evidence_source_hashes_match": True,
        "recorded_test_and_family_metrics_match": True,
        "experiment_run": experiment_run,
        "notebook_replay": {**notebook_run, "published_json_matches_replay": True,
                             "total_cells": 5, "code_cells": 3,
                             "execution_method": "stdlib compile/exec; not Jupyter kernel"},
        "python_assert_statements": assert_counts,
        "bound_sha256": after,
        "evidence_sha256": {str(path.relative_to(ROOT)): sha(path)
                            for path in sorted((ROOT / "evidence").glob("*"))
                            if path.is_file()} | {str(path.relative_to(ROOT)): sha(path)
                                                  for path in sorted(AUDIT.glob("*.log"))},
        "scope": "Independent mathematics/code review, finite tests, and evidence consistency; no historical source audit or formal proof certification."
    }
    (AUDIT / "results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "original_tests_each_mode": test_runs["normal"]["tests_run"],
                      "oracle_counts_each_mode": report["oracle_result"]["counts"],
                      "oracle_results_identical_across_modes": True,
                      "published_notebook_equals_replay": True,
                      "source_hash_bindings": len(after)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
