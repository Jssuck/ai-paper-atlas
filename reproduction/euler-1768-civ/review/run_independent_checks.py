#!/usr/bin/env python3
"""Capture the independent review's actual subprocess checks (stdlib only)."""
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    records, log = [], []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0")

    def run(arguments, expected=0, display=None):
        command = [sys.executable, *arguments]
        completed = subprocess.run(command, cwd=ROOT, env=env, text=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
        shown = "python3 " + " ".join(display or arguments)
        # Temporary path names are never needed in the public evidence log.
        output = completed.stdout
        log.extend(["$ " + shown, output.rstrip(), f"Exit status: {completed.returncode}; expected: {expected}", ""])
        records.append({"command": shown, "exit_status": completed.returncode,
                        "expected_exit_status": expected, "passed": completed.returncode == expected})
        if completed.returncode != expected:
            raise RuntimeError("Command failed: " + shown)
        return completed

    status = "PASS"
    try:
        run(["report.py", "--check", "outputs/report.json"])
        run(["-m", "unittest", "discover", "-s", "tests", "-v"])
        run(["run_checks.py"])
        # Execute all three Python examples published in the teaching guide.
        teaching = (ROOT / "TEACHING.md").read_text(encoding="utf-8")
        marker = "python3 - <<'PY'\n"
        snippets = [part.split("\nPY", 1)[0] for part in teaching.split(marker)[1:]]
        if len(snippets) != 3:
            raise RuntimeError("Expected exactly three teaching Python examples")
        for number, source in enumerate(snippets, 1):
            run(["-c", source], display=["-c", f"<TEACHING.md-example-{number}>"])
        run(["review/independent_oracle.py"])
        # Verify fresh generation and the check command's failure behavior,
        # without replacing the checked-in report or touching the main code.
        with tempfile.TemporaryDirectory(prefix="euler-civ-review-") as directory:
            fresh = Path(directory) / "report.json"
            run(["report.py", "--output", str(fresh)], display=["report.py", "--output", "<temporary-report.json>"])
            matches = fresh.read_bytes() == (ROOT / "outputs/report.json").read_bytes()
            records.append({"check": "fresh report byte identity", "passed": matches})
            log.extend(["Fresh report byte-identical to outputs/report.json: " + str(matches), ""])
            if not matches:
                raise RuntimeError("Fresh report differs")
            fresh.write_bytes(fresh.read_bytes() + b" ")
            run(["report.py", "--check", str(fresh)], expected=1,
                display=["report.py", "--check", "<deliberately-corrupted-report.json>"])
    except Exception as exc:
        status = "FAIL"
        log.append(type(exc).__name__ + ": " + str(exc))
    paths = ("euler_civ.py", "report.py", "run_checks.py", "tests/test_euler_civ.py", "README.md", "TEACHING.md",
             "outputs/report.json", "outputs/environment.json",
             "review/independent_oracle.py", "review/run_independent_checks.py", "review/independent-results.json")
    metadata = {"status": status, "python_version": platform.python_version(),
                "python_implementation": platform.python_implementation(),
                "platform": platform.platform(), "machine": platform.machine(),
                "dependencies": "Python standard library only; no installation or network", "checks": records,
                "environment": {"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0"},
                "sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths}}
    (ROOT / "review/run.log").write_text("\n".join(log) + "\n", encoding="utf-8")
    (ROOT / "review/validation.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("\n".join(log))
    print("Independent review status: " + status)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
