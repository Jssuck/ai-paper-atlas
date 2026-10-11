"""Recreate execution evidence, locally and without network or dependencies."""
import hashlib
import json
import os
from pathlib import Path
import platform
import shlex
import subprocess
import sys
import time
from datetime import datetime, timezone


def main():
    root = Path(__file__).resolve().parent
    os.chdir(root)
    mode = ("optimized" if sys.flags.optimize == 1 else
            "optimized-2" if sys.flags.optimize == 2 else "")
    logdir = Path("logs") / mode
    outdir = Path("outputs") / mode
    (root / logdir).mkdir(parents=True, exist_ok=True)
    (root / outdir).mkdir(parents=True, exist_ok=True)
    # An optimized parent must actually test optimized children.
    python = [sys.executable] + (["-" + "O" * sys.flags.optimize] if sys.flags.optimize else [])
    environment = {
        "run_started_utc_from_executor_clock": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "python_executable": Path(sys.executable).name,
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "dependencies": "Python standard library only",
        "network_used": False,
        "randomness_used": False,
        "notebook_used": False,
        "optimization_level": sys.flags.optimize,
        "working_directory": ". (package root)",
    }
    (root / logdir / "environment.json").write_text(json.dumps(environment, indent=2) + "\n")
    plans = [(python + ["-m", "unittest", "discover", "-s", "tests", "-v"],
              logdir / "unit-tests.txt"),
             (python + ["walkthrough.py"], outdir / "walkthrough.json"),
             (python + ["exhaustive.py"], outdir / "exhaustive.json")]
    commands = []
    for command, destination in plans:
        started = time.perf_counter()
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8",
                                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        elapsed = time.perf_counter() - started
        text = result.stdout + result.stderr
        (root / destination).write_text(text, encoding="utf-8")
        record = {"command": shlex.join(["python3", *command[1:]]), "output": str(destination),
                  "optimization_level": sys.flags.optimize,
                  "exit_code": result.returncode, "elapsed_seconds": round(elapsed, 6)}
        commands.append(record)
        print(json.dumps(record))
        if result.returncode:
            (root / logdir / "commands.json").write_text(json.dumps(commands, indent=2) + "\n")
            print(text, file=sys.stderr)
            return result.returncode
    (root / logdir / "commands.json").write_text(json.dumps(commands, indent=2) + "\n")
    hashes = {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in sorted(root.rglob("*"))
              if path.is_file() and path.suffix in (".py", ".md")
              and "__pycache__" not in path.parts
              and "independent-review" not in path.relative_to(root).parts}
    (root / logdir / "source-hashes.json").write_text(json.dumps(hashes, indent=2) + "\n")
    print("PASS: unit tests, walkthrough, and finite independent-oracle comparisons")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
