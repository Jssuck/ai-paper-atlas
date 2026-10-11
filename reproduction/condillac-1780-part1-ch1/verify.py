"""Capture real subprocess output, exit statuses, environment, and file hashes.

Run from any directory with Python 3.10+; logs are written beside this script.
The runner uses only the standard library and performs no network operations.
"""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys


def main() -> int:
    root = Path(__file__).resolve().parent
    logs = root / "logs"
    logs.mkdir(exist_ok=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0")
    jobs = (
        ("walkthrough.txt", [sys.executable, "-B", "walkthrough.py"]),
        ("unit-tests.txt", [sys.executable, "-B", "-m", "unittest", "-v", "test_model"]),
        ("exhaustive.json", [sys.executable, "-B", "exhaustive.py"]),
        ("exhaustive-optimized.json", [sys.executable, "-B", "-O", "exhaustive.py"]),
    )
    runs = []
    passed = True
    for filename, command in jobs:
        result = subprocess.run(command, cwd=root, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, check=False)
        (logs / filename).write_bytes(result.stdout)
        runs.append({"command": command, "exit_code": result.returncode,
                     "output": f"logs/{filename}",
                     "output_sha256": hashlib.sha256(result.stdout).hexdigest()})
        print(f"{filename}: exit {result.returncode}")
        passed = passed and result.returncode == 0
    optimized_equal = ((logs / "exhaustive.json").read_bytes()
                       == (logs / "exhaustive-optimized.json").read_bytes())
    passed = passed and optimized_equal
    sources = sorted(root.glob("*.py")) + sorted(root.glob("*.md"))
    compiled = []
    compile_errors = {}
    for source in sorted(root.glob("*.py")):
        try:
            compile(source.read_text(encoding="utf-8"), source.name, "exec")
        except (SyntaxError, UnicodeError, OSError) as error:
            compile_errors[source.name] = str(error)
            passed = False
        else:
            compiled.append(source.name)
    report = {
        "status": "PASS" if passed else "FAIL",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {"python": sys.version, "implementation": platform.python_implementation(),
                        "platform": platform.platform(), "machine": platform.machine(),
                        "standard_library_only": True, "network_used": False},
        "working_directory": "directory containing verify.py (absolute path intentionally omitted)",
        "entry_command": "python3 -B verify.py",
        "compiled_without_writing_bytecode": compiled,
        "compile_errors": compile_errors,
        "subprocesses": runs,
        "normal_and_optimized_oracle_output_equal": optimized_equal,
        "source_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
    }
    (logs / "verification.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"normal and optimized oracle outputs equal: {optimized_equal}")
    print(f"overall: {report['status']}; details: logs/verification.json")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
