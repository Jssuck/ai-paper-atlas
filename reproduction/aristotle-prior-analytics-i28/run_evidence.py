"""Run real checks and retain stdout/stderr with exit status and file hashes."""
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent

def main():
    logs = HERE / "logs"
    logs.mkdir(exist_ok=True)
    commands = [("tests", [sys.executable, "-B", "-m", "unittest", "-v", "test_model"]),
                ("demo", [sys.executable, "-B", "run_demo.py"]),
                ("optimized", [sys.executable, "-B", "-O", "-m", "unittest", "-v", "test_model"]),
                ("isolated", [sys.executable, "-B", "-I", "-c",
                 "import sys,unittest; sys.path.insert(0,'.'); "
                 "suite=unittest.defaultTestLoader.loadTestsFromName('test_model'); "
                 "r=unittest.TextTestRunner(verbosity=2).run(suite); "
                 "raise SystemExit(not r.wasSuccessful())"])]
    results = []
    for name, command in commands:
        result = subprocess.run(command, cwd=HERE, capture_output=True, text=True)
        (logs / (name + ".stdout.txt")).write_text(result.stdout, encoding="utf-8")
        (logs / (name + ".stderr.txt")).write_text(result.stderr, encoding="utf-8")
        # Interpreter path is normalized in the public record; raw output unchanged.
        results.append({"name": name, "command": ["python3", *command[1:]],
                        "exit_code": result.returncode})
    sources = ["model.py", "test_model.py", "run_demo.py", "run_evidence.py"]
    data = {"timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "environment": {"python": platform.python_version(),
                            "implementation": platform.python_implementation(),
                            "system": platform.system(), "machine": platform.machine(),
                            "dependencies": "Python standard library only"},
            "runs": results,
            "source_sha256": {p: hashlib.sha256((HERE / p).read_bytes()).hexdigest()
                              for p in sources}}
    (HERE / "evidence.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(data, indent=2))
    return 1 if any(r["exit_code"] for r in results) else 0

if __name__ == "__main__":
    raise SystemExit(main())
