#!/usr/bin/env python3
"""Rebuild reports and preserve genuine test output in three Python modes."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shlex
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def portable_command(command):
    """Publish a portable spelling, not local installation/workspace paths."""
    return ["python3"] + [str(arg) for arg in command[1:]]


def run_logged(command, logfile, env):
    start = utc_now()
    before = time.perf_counter()
    proc = subprocess.run(command, cwd=ROOT, env=env, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, text=True)
    elapsed = time.perf_counter() - before
    logfile.write_text(
        f"Started UTC: {start}\nPortable command: {shlex.join(portable_command(command))}\n"
        f"Working directory: . (package directory)\n"
        f"Execution note: current sys.executable used; local paths omitted.\n\n{proc.stdout}\n"
        f"Exit code: {proc.returncode}\nElapsed seconds: {elapsed:.6f}\n",
        encoding="utf-8")
    return proc, elapsed


def main():
    logs = ROOT / "logs"
    logs.mkdir(exist_ok=True)
    env = os.environ.copy()
    # Ensure the no-flag run really is normal, independent of caller settings.
    env.pop("PYTHONOPTIMIZE", None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    environment = {
        "captured_utc": utc_now(), "portable_python_command": "python3",
        "execution_note": "Current sys.executable used internally; local installation paths omitted.",
        "python_version": sys.version, "implementation": platform.python_implementation(),
        "platform": platform.platform(), "machine": platform.machine(),
        "working_directory": ". (package directory)", "dependencies": "Python standard library only",
        "network_access_required": False,
        "test_environment_overrides": {"PYTHONOPTIMIZE": "removed", "PYTHONDONTWRITEBYTECODE": "1"},
    }
    (logs / "environment.json").write_text(json.dumps(environment, indent=2) + "\n", encoding="utf-8")
    build, build_elapsed = run_logged(
        [sys.executable, "second_figure.py", "--json", "report.json", "--markdown", "REPORT.md"],
        logs / "report-build.log", env)
    results = []
    for label, flags, expected_optimize in (("normal", [], 0), ("optimized", ["-O"], 1),
                                           ("double-optimized", ["-OO"], 2)):
        command = [sys.executable] + flags + ["-m", "unittest", "-v", "test_second_figure"]
        probe = subprocess.run([sys.executable] + flags + ["-c", "import sys; print(sys.flags.optimize)"],
                               cwd=ROOT, env=env, capture_output=True, text=True)
        proc, elapsed = run_logged(command, logs / f"tests-{label}.log", env)
        match = re.search(r"Ran (\d+) tests? in ([0-9.]+)s", proc.stdout)
        observed = int(probe.stdout.strip()) if probe.returncode == 0 else None
        results.append({"mode": label, "portable_command": portable_command(command), "exit_code": proc.returncode,
                        "expected_optimize": expected_optimize, "observed_optimize": observed,
                        "tests_run": int(match.group(1)) if match else None,
                        "unittest_seconds": float(match.group(2)) if match else None,
                        "process_seconds": elapsed, "log": f"logs/tests-{label}.log",
                        "passed": proc.returncode == 0 and observed == expected_optimize and match is not None})
    hashes = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
              for name in ("second_figure.py", "test_second_figure.py", "run_verification.py",
                           "README.md", "WALKTHROUGH.md", "report.json", "REPORT.md")}
    passed = build.returncode == 0 and all(row["passed"] for row in results)
    verification = {"completed_utc": utc_now(), "report_build_exit_code": build.returncode,
                    "report_build_seconds": build_elapsed, "passed": passed,
                    "test_runs": results, "sha256": hashes}
    (logs / "verification.json").write_text(json.dumps(verification, indent=2) + "\n", encoding="utf-8")
    lines = ["# Verification record", "", f"Completed (UTC): {verification['completed_utc']}", "",
             "These are actual subprocess runs, not inferred results. Full stdout/stderr, commands, "
             "exit codes and timings are retained in `logs/`. Commands use portable `python3` spellings "
             "and relative working directories instead of private local paths. Environment and file hashes are recorded "
             "in `logs/environment.json` and `logs/verification.json`.", "",
             f"Report generation exit code: **{build.returncode}**.", "",
             "| Mode | Observed optimization | Tests | Exit | Result |",
             "|---|---:|---:|---:|---|"]
    for row in results:
        lines.append(f"| {row['mode']} | {row['observed_optimize']} | {row['tests_run']} | "
                     f"{row['exit_code']} | {'PASS' if row['passed'] else 'FAIL'} |")
    lines.extend(["", "## Coverage and limits", "",
                  "The suite independently checks all 192 mood-policy cases, all 176 invalid-case "
                  "witnesses and their cardinality minimality, all 9,180 atomic clause evaluations, "
                  "all 255 support realizations, and compression for all 584 labeled models with "
                  "domain sizes one through three. It also checks reversal, vacuity, strict input "
                  "validation, deterministic reports and CLI behavior.", "",
                  "Passing finite tests is not by itself a proof over arbitrary universes, nor a "
                  "historical validation. The support-preservation argument is given separately "
                  "in WALKTHROUGH.md. The three modes run the same test suite, not three "
                  "independent implementations. The set-based oracle is independent of the "
                  "production atom evaluator but belongs to the same authored package.", ""])
    (ROOT / "VERIFICATION.md").write_text("\n".join(lines), encoding="utf-8")
    for row in results:
        print(f"{row['mode']}: {row['tests_run']} tests; optimize={row['observed_optimize']}; "
              f"exit={row['exit_code']}; {'PASS' if row['passed'] else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
