#!/usr/bin/env python3
"""Run, log, and verify the complete standard-library teaching package."""
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shlex
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    RESULTS.mkdir(exist_ok=True)
    started = datetime.now(timezone.utc).isoformat()
    timer = time.perf_counter()
    records = []
    execution = []
    temporary_root = None
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0")

    def run(args: list[str], label: str, hash_seed: str = "0") -> str:
        command = [sys.executable, *args]
        before = time.perf_counter()
        completed = subprocess.run(command, cwd=ROOT, env=dict(env, PYTHONHASHSEED=hash_seed),
                                   text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        elapsed = time.perf_counter() - before
        logged_command = [Path(sys.executable).name, *args]
        if temporary_root is not None:
            logged_command = [part.replace(str(temporary_root), "TEMP_DIR") for part in logged_command]
        records.append({"label": label, "command": logged_command, "pythonhashseed": hash_seed,
                        "returncode": completed.returncode, "elapsed_seconds": elapsed})
        block = f"$ PYTHONHASHSEED={hash_seed} {shlex.join(logged_command)}\n{completed.stdout}\nexit_code={completed.returncode}\n"
        execution.append(block)
        (RESULTS / "execution.log").write_text("\n".join(execution), encoding="utf-8")
        print(block, end="")
        if label == "unit_tests":
            (RESULTS / "tests.log").write_text(completed.stdout, encoding="utf-8")
        if completed.returncode:
            raise RuntimeError(f"{label} failed with exit code {completed.returncode}")
        return completed.stdout

    status = "failed"
    error = None
    try:
        source_names = sorted(path.name for path in ROOT.glob("*.py"))
        for name in source_names:
            ast.parse((ROOT / name).read_text(encoding="utf-8"), filename=name)
        execution.append("Syntax check via ast.parse: " + ", ".join(source_names) + "\nPASS\n")
        run(["-m", "unittest", "-v"], "unit_tests")
        run(["run_experiments.py"], "main_experiments")
        with tempfile.TemporaryDirectory(prefix="condillac-i4-") as temp:
            temporary_root = Path(temp)
            copies = []
            for seed in ("0", "137"):
                destination = Path(temp) / seed
                run(["run_experiments.py", "--output-dir", str(destination)], "determinism_" + seed, seed)
                copies.append(destination)
            hashes = {}
            for name in ("results.json", "summary.txt"):
                current = sha256(RESULTS / name)
                repeated = [sha256(path / name) for path in copies]
                if repeated != [current, current]:
                    raise AssertionError("Nondeterministic output: " + name)
                hashes[name] = {"delivered_sha256": current, "repeat_sha256": repeated, "byte_identical": True}
            write_json(RESULTS / "determinism.json", {"hash_seeds": [0, 137], "files": hashes,
                       "scope": "Deterministic model results only; environment, timing and logs can vary."})
        status = "passed"
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        execution.append(error + "\n")
    environment = {
        "started_utc": started, "finished_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version, "executable_name": Path(sys.executable).name, "platform": platform.platform(),
        "machine": platform.machine(), "working_directory": "this package directory",
        "log_path_policy": "Interpreter path is reduced to its filename; TEMP_DIR denotes the real temporary output directory.",
        "dependency_policy": "Python standard library only; no install, network, API call, or paid service",
        "elapsed_seconds_total": time.perf_counter() - timer, "status": status,
        "error": error, "commands": records,
    }
    write_json(RESULTS / "environment.json", environment)
    execution.append(f"FINAL STATUS: {status}\n")
    (RESULTS / "execution.log").write_text("\n".join(execution), encoding="utf-8")
    # Deliberately enumerate only author-owned files. External audit files are separate.
    deliverables = sorted([*ROOT.glob("*.py"), *ROOT.glob("*.md"),
                           *(RESULTS / name for name in ("results.json", "summary.txt", "tests.log",
                             "execution.log", "environment.json", "determinism.json") if (RESULTS / name).exists())])
    manifest = "".join(f"{sha256(path)}  {path.relative_to(ROOT).as_posix()}\n" for path in deliverables)
    (RESULTS / "manifest.sha256").write_text(manifest, encoding="utf-8")
    print(f"FINAL STATUS: {status}")
    return 0 if status == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
