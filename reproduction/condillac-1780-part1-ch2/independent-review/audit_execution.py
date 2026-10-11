"""Run the final production entry point in isolated temporary copies.

This avoids altering author evidence. Both invocations start outside the package
root. Only output path spellings are normalized, not values or exit codes.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
LOGS = Path(__file__).resolve().parent / "logs"
FILES = ("model.py", "walkthrough.py", "exhaustive.py", "run_all.py", "tests/test_model.py")


def require(condition, description):
    if not condition:
        raise AssertionError(description)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(value, paths):
    if isinstance(value, str):
        for original, replacement in paths:
            value = value.replace(original, replacement)
        return value
    if isinstance(value, dict):
        return {key: normalize(val, paths) for key, val in value.items()}
    if isinstance(value, list):
        return [normalize(val, paths) for val in value]
    return value


def main():
    source_hashes = {name: sha(ROOT / name) for name in FILES}
    modes = []
    for flag in (None, "-O"):
        with tempfile.TemporaryDirectory(prefix="condillac-independent-") as temporary:
            base = Path(temporary)
            package = base / "package"
            outside = base / "unrelated-working-directory"
            (package / "tests").mkdir(parents=True)
            outside.mkdir()
            for name in FILES:
                shutil.copy2(ROOT / name, package / name)
                require(sha(package / name) == source_hashes[name], "copy mismatch: " + name)
            command = [sys.executable] + ([flag] if flag else []) + [str(package / "run_all.py")]
            run = subprocess.run(command, cwd=outside, capture_output=True, text=True,
                                 env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
            mode = "optimized" if flag else "normal"
            paths = [(str(package), "<isolated-package-copy>"),
                     (str(base), "<temporary-audit-directory>"),
                     (sys.executable, "python3")]
            require(run.returncode == 0, normalize(run.stdout + run.stderr, paths))
            suffix = "optimized" if flag else ""
            logdir, outdir = package / "logs" / suffix, package / "outputs" / suffix
            commands = json.loads((logdir / "commands.json").read_text())
            environment = json.loads((logdir / "environment.json").read_text())
            require(environment["optimization_level"] == (1 if flag else 0), "optimization not active")
            for child in commands:
                require(child["exit_code"] == 0, "child failed")
                require((" -O " in child["command"]) == bool(flag), "optimization not propagated")
            exhaustive = json.loads((outdir / "exhaustive.json").read_text())
            walkthrough = json.loads((outdir / "walkthrough.json").read_text())
            # Closed-form independent count: a complete triangle is consistent
            # exactly when d_AC = d_AB + d_BC, coordinate by coordinate.
            cycle_1d = sum(-2 <= a + b <= 2 for a in range(-2, 3) for b in range(-2, 3))
            cycle_2d_axis = sum(-1 <= a + b <= 1 for a in range(-1, 2) for b in range(-1, 2))
            consistent_1d = 1 + 3 * 5 + 3 * 5 ** 2 + cycle_1d
            consistent_2d = 1 + 3 * 9 + 3 * 9 ** 2 + cycle_2d_axis ** 2
            expected_totals = {"graph_cases": 6 ** 3 + 10 ** 3,
                               "consistent_graphs": consistent_1d + consistent_2d,
                               "inconsistent_graphs": 6 ** 3 + 10 ** 3 - consistent_1d - consistent_2d,
                               "brute_force_assignments": 6 ** 3 * 9 ** 2 + 10 ** 3 * 25 ** 2,
                               "pair_queries": 3 * (consistent_1d + consistent_2d),
                               "reversed_graph_checks": 6 ** 3 + 10 ** 3}
            require(exhaustive["totals"] == expected_totals, "published counts mismatch")
            require(walkthrough["order_permutations"]["permutations"] == 24, "permutation count")
            require(walkthrough["order_permutations"]["toy_prefix_sum_values"] == [6, 7, 8, 9, 10, 11],
                    "prefix score range")
            require(walkthrough["order_permutations"]["inconsistent_triangle_orders_rejected"] == 6,
                    "inconsistent permutation count")
            unit_text = normalize((logdir / "unit-tests.txt").read_text(), paths)
            (LOGS / ("unit-tests-" + mode + ".txt")).write_text(unit_text)
            modes.append({"mode": mode, "command": "python3 " + ((flag + " ") if flag else "") +
                          "<isolated-package-copy>/run_all.py",
                          "initial_working_directory": "unrelated directory outside isolated package copy",
                          "exit_code": run.returncode, "stdout": normalize(run.stdout, paths),
                          "stderr": normalize(run.stderr, paths),
                          "children": normalize(commands, paths),
                          "environment": normalize(environment, paths),
                          "exhaustive": exhaustive})
    require(source_hashes == {name: sha(ROOT / name) for name in FILES}, "source changed during audit")
    output = {"status": "PASS", "normalization": "Only known local absolute paths replaced with portable placeholders.",
              "source_sha256": source_hashes, "modes": modes}
    (LOGS / "audited-code-sha256.json").write_text(json.dumps(source_hashes, indent=2) + "\n")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
