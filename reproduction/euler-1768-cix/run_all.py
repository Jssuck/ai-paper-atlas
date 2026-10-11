#!/usr/bin/env python3
"""Regenerate actual execution logs and deterministic artifacts, offline."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shlex
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent


def main():
    if sys.version_info < (3, 10):
        raise SystemExit("Python 3.10 or newer is required")
    (ROOT / "logs").mkdir(exist_ok=True)
    (ROOT / "outputs").mkdir(exist_ok=True)
    records = []
    environment = {
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "executable": Path(sys.executable).name,
        "dependencies": "Python standard library only",
        "network_required": False,
        "randomness": "none",
        "working_directory": ".",
        "path_note": "Absolute interpreter and working-directory paths are normalized for portability; commands execute with the active interpreter in this reproduction directory.",
    }
    (ROOT / "logs/environment.json").write_text(json.dumps(environment, indent=2) + "\n", encoding="utf-8")
    commands = [
        ("tests", [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]),
        ("demo", [sys.executable, "memory_model.py", "--demo", "--output", "outputs/demo.json"]),
        ("exhaustive", [sys.executable, "memory_model.py", "--check", "--output", "outputs/exhaustive.json"]),
    ]
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0"}
    for label, command in commands:
        start_utc = datetime.now(timezone.utc).isoformat()
        start = time.perf_counter()
        result = subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True)
        duration = time.perf_counter() - start
        recorded_command = [Path(command[0]).name, *command[1:]]
        log = (f"Command: {shlex.join(recorded_command)}\nStarted UTC: {start_utc}\n"
               f"Exit code: {result.returncode}\nElapsed seconds: {duration:.6f}\n"
               f"\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
        (ROOT / "logs" / f"{label}.log").write_text(log, encoding="utf-8")
        records.append({"name": label, "argv": recorded_command, "exit_code": result.returncode,
                        "elapsed_seconds": duration, "log": f"logs/{label}.log"})
        print(f"{label}: exit={result.returncode}, elapsed={duration:.3f}s")
        if result.returncode:
            (ROOT / "logs/run.json").write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
            print(result.stdout, result.stderr)
            raise SystemExit(result.returncode)
    hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in [ROOT / "memory_model.py", ROOT / "tests/test_memory_model.py", ROOT / "run_all.py",
                           ROOT / "outputs/demo.json", ROOT / "outputs/exhaustive.json"]}
    (ROOT / "logs/run.json").write_text(json.dumps({"commands": records, "sha256": hashes}, indent=2) + "\n", encoding="utf-8")
    print("PASS: tests, examples, and exhaustive model checks; see logs/ and outputs/.")


if __name__ == "__main__":
    main()
