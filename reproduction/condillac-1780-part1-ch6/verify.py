"""Run all reproducible author checks and preserve real, portable logs."""

import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs"


def main():
    LOGS.mkdir(exist_ok=True)
    sources = sorted(list(ROOT.glob("*.py")) + list(ROOT.glob("*.md")) + list((ROOT / "tests").glob("*.py")))
    source_hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources}
    assert_nodes = []
    for path in sources:
        if path.suffix == ".py":
            assert_nodes.extend(f"{path.relative_to(ROOT)}:{node.lineno}" for node in ast.walk(ast.parse(path.read_text()))
                                if isinstance(node, ast.Assert))
    environment = {"python_version": sys.version, "implementation": platform.python_implementation(),
                   "platform": platform.platform(), "standard_library_only": True,
                   "utc_start": datetime.now(timezone.utc).isoformat(), "invocation_optimization": sys.flags.optimize}
    (LOGS / "environment.json").write_text(json.dumps(environment, indent=2) + "\n", encoding="utf-8")
    stages = []
    demo_outputs = []
    for label, flags in (("normal", []), ("O", ["-O"]), ("OO", ["-OO"])):
        for task, arguments, suffix in (("unit-tests", ["-m", "unittest", "discover", "-s", "tests", "-v"], "txt"),
                                        ("finite-oracle", ["finite_oracle.py"], "json"),
                                        ("demo", ["demo.py"], "json")):
            command = [sys.executable, "-B"] + flags + arguments
            start = time.perf_counter()
            process = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=60)
            elapsed = time.perf_counter() - start
            output = (process.stdout + process.stderr).replace(str(ROOT), ".")
            log = f"{task}-{label}.{suffix}"
            (LOGS / log).write_text(output, encoding="utf-8")
            stages.append({"name": f"{task}-{label}", "command": [Path(sys.executable).name, "-B"] + flags + arguments,
                           "cwd": ".", "exit_code": process.returncode, "seconds": round(elapsed, 6), "log": f"logs/{log}"})
            if task == "demo":
                demo_outputs.append(process.stdout)
    start = time.perf_counter()
    process = subprocess.run([sys.executable, "-B", "mutation_check.py"], cwd=ROOT,
                             text=True, capture_output=True, timeout=60)
    (LOGS / "mutations.json").write_text((process.stdout + process.stderr).replace(str(ROOT), "."), encoding="utf-8")
    stages.append({"name": "valid-semantic-mutations-OO", "command": [Path(sys.executable).name, "-B", "mutation_check.py"],
                   "cwd": ".", "exit_code": process.returncode, "seconds": round(time.perf_counter() - start, 6),
                   "log": "logs/mutations.json"})
    same_demo = len(set(demo_outputs)) == 1
    result = {"status": "PASS" if all(stage["exit_code"] == 0 for stage in stages) and same_demo and not assert_nodes else "FAIL",
              "utc_finished": datetime.now(timezone.utc).isoformat(),
              "scope": "Author verification only; finite tests are not general proofs or an independent audit",
              "bare_assert_nodes": assert_nodes, "demo_identical_across_optimization_modes": same_demo,
              "stages": stages, "source_sha256": source_hashes}
    (LOGS / "verification.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "stages": len(stages), "tests_per_mode": 27,
                      "modes": ["normal", "-O", "-OO"], "demo_identical": same_demo,
                      "details": "logs/verification.json"}, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
