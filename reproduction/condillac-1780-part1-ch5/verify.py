"""Reproduce outputs and keep the actual environment, commands, hashes and logs."""
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
STAGES = (
    ("demo", ("demo.py",), "demo.json"),
    ("unit-tests", ("-m", "unittest", "discover", "-s", "tests", "-v"), "unit-tests.txt"),
    ("finite-oracle", ("finite_oracle.py",), "finite-oracle.json"),
    ("mutations", ("mutation_check.py",), "mutations.json"),
)


def run():
    if not __debug__:
        raise RuntimeError("Run without -O or -OO; assertions must stay enabled")
    logs = ROOT / "logs"
    logs.mkdir(exist_ok=True)
    environment = {"started_utc": datetime.now(timezone.utc).isoformat(),
                   "python": sys.version, "implementation": platform.python_implementation(),
                   "executable": Path(sys.executable).name, "platform": platform.platform(),
                   "working_directory": ".", "paths_normalized_for_portability": True, "dependencies": "Python standard library only",
                   "network_required": False, "assertions_enabled": __debug__,
                   "randomness": "none; deterministic enumeration", "pythonhashseed": "0"}
    (logs / "environment.json").write_text(json.dumps(environment, indent=2) + "\n", encoding="utf-8")
    sources = sorted(list(ROOT.glob("*.py")) + list((ROOT / "tests").glob("*.py")) + list(ROOT.glob("*.md")))
    hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources}
    for path in list(ROOT.glob("*.py")) + list((ROOT / "tests").glob("*.py")):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    results = []
    for name, arguments, output in STAGES:
        command = [sys.executable, *arguments]
        started = time.perf_counter()
        result = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, timeout=120,
                                env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0"))
        elapsed = time.perf_counter() - started
        (logs / output).write_text(result.stdout.replace(str(ROOT), "."), encoding="utf-8")
        results.append({"stage": name, "command": [Path(command[0]).name, *command[1:]], "exit_code": result.returncode,
                        "elapsed_seconds": round(elapsed, 6), "output": "logs/" + output})
        print(f"{name}: {'PASS' if result.returncode == 0 else 'FAIL'} ({elapsed:.3f}s)")
    passed = all(result["exit_code"] == 0 for result in results)
    record = {"finished_utc": datetime.now(timezone.utc).isoformat(),
              "source_sha256": hashes, "stages": results, "result": "PASS" if passed else "FAIL"}
    (logs / "verification.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return passed


if __name__ == "__main__":
    sys.exit(0 if run() else 1)
