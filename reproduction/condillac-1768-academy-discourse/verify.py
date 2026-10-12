"""Run and record the checks under normal, -O, and -OO interpreters."""
import ast
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

ROOT = Path(__file__).resolve().parent


def main():
    logs = ROOT / "logs"
    logs.mkdir(exist_ok=True)
    sources = ["model.py", "demo.py", "test_model.py", "verify.py"]
    for name in ("model.py", "demo.py"):
        parsed = ast.parse((ROOT / name).read_text(encoding="utf-8"))
        if any(isinstance(node, ast.Assert) for node in ast.walk(parsed)):
            raise RuntimeError(f"production assert found in {name}")
    environment = {
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "python_executable_basename": Path(sys.executable).name,
        "python_version": sys.version,
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "working_directory": ".",
        "command_display": "Commands use the active interpreter; public labels normalize its path to python3.",
        "dependencies": "Python standard library only; no network or installation required",
        "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sources},
        "expected_results_sha256": hashlib.sha256((ROOT / "examples" / "expected_results.json").read_bytes()).hexdigest(),
    }
    (logs / "environment.json").write_text(json.dumps(environment, indent=2) + "\n", encoding="utf-8")
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0")
    expected = (ROOT / "examples" / "expected_results.json").read_bytes()
    for name, flags in (("normal", []), ("optimized", ["-O"]), ("double-optimized", ["-OO"])):
        commands = [
            [sys.executable, *flags, "-c", "import sys; print('optimize=' + str(sys.flags.optimize)); print('debug=' + str(__debug__))"],
            [sys.executable, *flags, "-m", "unittest", "-v", "test_model"],
            [sys.executable, *flags, "demo.py"],
        ]
        chunks = []
        test_count = None
        for command in commands:
            result = subprocess.run(command, cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
            chunks.extend(["$ " + shlex.join(["python3", *command[1:]]) + "\n", result.stdout.decode("utf-8"), f"exit_code={result.returncode}\n"])
            (logs / f"{name}.log").write_text("".join(chunks), encoding="utf-8")
            if result.returncode != 0:
                raise RuntimeError(f"{name}: command failed; inspect its exact log")
            if command[-1] == "test_model":
                matched = re.search(rb"Ran (\d+) tests? in", result.stdout)
                if matched is None:
                    raise RuntimeError("could not verify executed unittest count")
                test_count = int(matched.group(1))
            if command[-1] == "demo.py" and result.stdout != expected:
                raise RuntimeError(f"{name}: demo differs from checked-in exact expected results")
        chunks.append("exact_demo_bytes_match=True\nproduction_assert_count=0\n")
        (logs / f"{name}.log").write_text("".join(chunks), encoding="utf-8")
        print(f"{name}: {test_count} tests passed; exact demo bytes match; production assert count 0")
    print("All three interpreter modes passed. Logs and environment metadata are in logs/.")


if __name__ == "__main__":
    main()
