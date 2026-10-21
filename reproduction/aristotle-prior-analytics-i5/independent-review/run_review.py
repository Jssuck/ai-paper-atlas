#!/usr/bin/env python3
"""Re-run independent review and author tests, keeping public, relative logs."""
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

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "independent-review"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command, label, env):
    started = datetime.now(timezone.utc).isoformat()
    before = time.perf_counter()
    p = subprocess.run(command, cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    elapsed = time.perf_counter() - before
    content = (f"Started UTC: {started}\nCommand: {shlex.join(command)}\n"
               "Working directory: . (reproduction root)\n"
               "Environment overrides: PYTHONOPTIMIZE removed; PYTHONHASHSEED=0; PYTHONDONTWRITEBYTECODE=1\n\n"
               + p.stdout + f"\nExit code: {p.returncode}\nElapsed seconds: {elapsed:.6f}\n")
    (OUT / (label + ".log")).write_text(content, encoding="utf-8")
    return {"command": command, "exit_code": p.returncode, "elapsed_seconds": elapsed,
            "log": label + ".log"}, p.stdout


def main():
    env = os.environ.copy()
    env.pop("PYTHONOPTIMIZE", None)
    env.update(PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1")
    names = ("second_figure.py", "test_second_figure.py", "run_verification.py", "README.md",
             "WALKTHROUGH.md", "REPORT.md", "report.json")
    before = {name: digest(ROOT / name) for name in names}
    runs = []
    for mode, flags, expected in (("normal", [], 0), ("optimized", ["-O"], 1),
                                  ("double-optimized", ["-OO"], 2)):
        prefix = ["python3"] + flags
        probe = subprocess.run(prefix + ["-c", "import sys; print(sys.flags.optimize)"], env=env,
                               cwd=ROOT, text=True, capture_output=True, check=True)
        observed = int(probe.stdout)
        author, output = run(prefix + ["-m", "unittest", "-v", "test_second_figure"],
                             "author-" + mode, env)
        match = re.search(r"Ran (\d+) tests? in ([0-9.]+)s", output)
        author["tests_run"] = int(match.group(1)) if match else None
        audit, _ = run(prefix + ["independent-review/audit_second_figure.py", "--output",
                                 "independent-review/results-" + mode + ".json"],
                       "independent-" + mode, env)
        passed = (observed == expected and author["exit_code"] == 0 and author["tests_run"] == 41
                  and audit["exit_code"] == 0)
        runs.append({"mode": mode, "observed_optimize": observed, "expected_optimize": expected,
                     "author_suite": author, "independent_audit": audit, "passed": passed})
        print(f"{mode}: author {author['tests_run']} tests, exit {author['exit_code']}; "
              f"independent exit {audit['exit_code']}; optimize={observed}; {'PASS' if passed else 'FAIL'}", flush=True)
    after = {name: digest(ROOT / name) for name in names}
    same = before == after
    summary = {"status": "PASS" if same and all(r["passed"] for r in runs) else "FAIL",
               "completed_utc": datetime.now(timezone.utc).isoformat(),
               "environment": {"python": platform.python_version(), "implementation": platform.python_implementation(),
                               "platform": platform.platform(), "machine": platform.machine(),
                               "command_interpreter": "python3", "working_directory": ". (reproduction root)",
                               "dependencies": "Python standard library only", "network_required": False,
                               "overrides": {"PYTHONOPTIMIZE": "removed", "PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1"}},
               "reviewed_files_sha256": before, "reviewed_files_unchanged_during_run": same,
               "audit_script_sha256": digest(OUT / "audit_second_figure.py"),
               "runner_sha256": digest(OUT / "run_review.py"), "runs": runs}
    (OUT / "verification.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
