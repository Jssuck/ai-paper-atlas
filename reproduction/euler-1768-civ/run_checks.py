#!/usr/bin/env python3
"""Run reproducible checks, preserving actual outputs and environment metadata."""
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"


def main():
    OUTPUTS.mkdir(exist_ok=True)
    commands = [
        [sys.executable, "report.py", "--check", "outputs/report.json"],
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
    ]
    logs = ["Commands display the interpreter as python3; subprocesses use the current sys.executable.", ""]
    results = []
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0")
    for command in commands:
        result = subprocess.run(command, cwd=ROOT, env=env, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
        display_command = ["python3", *command[1:]]
        logs.extend(["$ " + " ".join(display_command), result.stdout.rstrip(), f"Exit status: {result.returncode}", ""])
        results.append({"command": display_command, "exit_status": result.returncode})
    files = ["euler_civ.py", "report.py", "run_checks.py", "tests/test_euler_civ.py",
             "README.md", "TEACHING.md", "outputs/report.json"]
    metadata = {
        "python_version": sys.version,
        "python_implementation": platform.python_implementation(),
        "python_executable": Path(sys.executable).name,
        "command_display_note": "Interpreter paths are normalized to python3; subprocesses use the current sys.executable.",
        "platform": platform.platform(),
        "machine": platform.machine(),
        "dependencies": "Python standard library only",
        "tested_commands": results,
        "reproducibility_environment": {"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0"},
        "sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in files},
    }
    (OUTPUTS / "run.log").write_text("\n".join(logs), encoding="utf-8")
    (OUTPUTS / "environment.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("\n".join(logs))
    return 0 if all(result["exit_status"] == 0 for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
