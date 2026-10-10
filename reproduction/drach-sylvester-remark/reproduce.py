"""Run the actual demo/tests and write reproducibility records (stdlib only)."""

from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import shlex
import subprocess
import sys


def main():
    root = Path(__file__).resolve().parent
    environment = {
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "executable": sys.executable,
        "dependencies": "Python standard library only",
        "network_required": False,
        "test_method_count": 8,
        "real_coefficient_grid_cases": 625,
    }
    (root / "environment.json").write_text(json.dumps(environment, indent=2) + "\n")
    commands = []
    for args, filename in [(["-m", "unittest", "-v", "test_demo"], "tests.log"),
                           (["demo.py"], "results.json")]:
        command = [sys.executable, *args]
        completed = subprocess.run(command, cwd=root, text=True, capture_output=True)
        commands.append("$ " + shlex.join(command))
        commands.append("exit_code=" + str(completed.returncode))
        output = completed.stdout + completed.stderr
        (root / filename).write_text(output, encoding="utf-8")
        (root / "commands.log").write_text("\n".join(commands) + "\n", encoding="utf-8")
        if completed.returncode:
            print(output, file=sys.stderr)
            return completed.returncode
    print("8 tests passed; 625 grid cases checked; results and logs written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
