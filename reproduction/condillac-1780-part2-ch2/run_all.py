"""Run and retain complete author-verification logs in all optimization modes."""
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import shlex
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent


def main():
    logs = ROOT / "logs"
    logs.mkdir(exist_ok=True)
    scripts = sorted(ROOT.glob("*.py"))
    for path in scripts:
        if any(isinstance(node, ast.Assert) for node in ast.walk(ast.parse(path.read_text(encoding="utf-8")))):
            raise RuntimeError(f"bare assert forbidden: {path.name}")
    started = time.perf_counter()
    summary = {"verified_at_utc": datetime.now(timezone.utc).isoformat(), "python": sys.version,
               "implementation": platform.python_implementation(), "platform": platform.platform(),
               "dependency_policy": "Python standard library only; nothing installed; no network used",
               "scope": "Author checks, not independent audit or psychological validation",
               "log_normalization": "Only temp workdir prefixes and command interpreter paths are replaced; no output lines removed",
               "files_sha256": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in scripts},
               "bare_assert_count": 0, "modes": {}}
    with (logs / "verification.log").open("w", encoding="utf-8") as log:
        log.write("PATH NORMALIZATION ONLY: ${PYTHON_EXECUTABLE} = current sys.executable; ${MUTATION_DIR} = each child temporary directory. No stdout/stderr lines removed.\n")
        for mode, flags in (("normal", []), ("O", ["-O"]), ("OO", ["-OO"])):
            records = []
            for label, tail in (("tests", ["-m", "unittest", "-v"]),
                                ("mutations", ["mutation_check.py", "--mode", mode])):
                command = [sys.executable, *flags, "-B", *tail]
                result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
                log.write(f"\n=== {mode}: {label} ===\n$ {shlex.join(['${PYTHON_EXECUTABLE}', *command[1:]])}\n")
                log.write("--- stdout ---\n" + result.stdout + "--- stderr ---\n" + result.stderr)
                log.write(f"--- exit code: {result.returncode} ---\n")
                log.flush()
                record = {"stage": label, "exit_code": result.returncode}
                if label == "tests":
                    record["expected_test_methods"] = 28
                    record["completion_verified"] = "Ran 28 tests in " in result.stderr and result.stderr.rstrip().endswith("OK")
                else:
                    parsed = json.loads(result.stdout)
                    record.update({key: parsed[key] for key in ("mutation_count", "baseline_count", "control_count", "passed")})
                    record["outcomes"] = [{"name": case["name"], "kind": case["kind"], "outcome": case["outcome"]}
                                          for case in parsed["cases"]]
                records.append(record)
                if result.returncode != 0 or record.get("completion_verified") is False or record.get("passed") is False:
                    raise RuntimeError(f"verification failed in {mode}/{label}; inspect verification.log")
            summary["modes"][mode] = records
        command = [sys.executable, "-B", "demo.py"]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=30)
        log.write(f"\n=== demo ===\n$ {shlex.join(['${PYTHON_EXECUTABLE}', *command[1:]])}\n--- stdout ---\n{result.stdout}--- stderr ---\n{result.stderr}--- exit code: {result.returncode} ---\n")
        if result.returncode != 0:
            raise RuntimeError("demo failed")
        json.loads(result.stdout)
        (logs / "results.json").write_text(result.stdout, encoding="utf-8")
    summary["elapsed_seconds"] = round(time.perf_counter() - started, 6)
    summary["passed"] = True
    (logs / "verification-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": True, "test_methods_per_mode": 28, "modes": list(summary["modes"]),
                      "behavior_mutations_per_mode": 8, "classification_controls_per_mode": 5,
                      "logs": ["logs/verification.log", "logs/verification-summary.json", "logs/results.json"]}, indent=2))


if __name__ == "__main__":
    main()
