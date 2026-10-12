"""Regenerate local reproducibility logs using only the current Python and stdlib."""

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys


def main():
    root = Path(__file__).resolve().parent
    logs = root / "logs"
    logs.mkdir(exist_ok=True)
    environment = {
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "os": platform.system(),
        "machine": platform.machine(),
        "dependencies": "Python standard library only",
        "pythonhashseed": "0",
        "pythondontwritebytecode": "1",
        "source_sha256": {
            name: hashlib.sha256((root / name).read_bytes()).hexdigest()
            for name in ("model.py", "demo.py", "test_model.py", "run_checks.py")
        },
    }
    (logs / "environment.json").write_text(
        json.dumps(environment, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1")
    failed = False
    for name, flags in (("normal", []), ("optimized", ["-O"]), ("double-optimized", ["-OO"])):
        sections = []
        for arguments in (
            ["-c", "import sys; print('optimization level:', sys.flags.optimize)"],
            ["-m", "unittest", "-v", "test_model"],
            ["demo.py"],
        ):
            command = [sys.executable, *flags, *arguments]
            result = subprocess.run(
                command, cwd=root, env=env, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True, encoding="utf-8", check=False,
            )
            display = "python3 " + " ".join([*flags, *arguments])
            if arguments[0] == "-c":
                display = " ".join(["python3", *flags, "-c", repr(arguments[1])])
            sections.extend((f"$ {display}\n", result.stdout, f"exit_code: {result.returncode}\n\n"))
            failed = failed or result.returncode != 0
        (logs / f"{name}.log").write_text("".join(sections), encoding="utf-8")
        print(f"Wrote logs/{name}.log")
    print("Wrote logs/environment.json")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
