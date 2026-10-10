"""Run the shipped commands and retain real logs, timing, environment and hashes."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"


def now():
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    OUT.mkdir(exist_ok=True)
    started = now()
    commands = [
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        [sys.executable, "reproduce.py", "--out", "results"],
        [sys.executable, "walkthrough.py"],
    ]
    environment = {
        "started_utc": started,
        "python_version": sys.version,
        "python_executable": "python (the interpreter running this script)",
        "platform": platform.platform(),
        "implementation": platform.python_implementation(),
        "working_directory": ". (package root)",
        "external_python_dependencies": [],
        "installed_anything_for_run": False,
        "network_needed_for_run": False,
        "notebook_execution": "Not applicable: the deliverable is an annotated .py walkthrough, not a notebook or kernel run.",
    }
    log = ["Gergonne 1817 reproduction: actual validation log", f"Started UTC: {started}",
           json.dumps(environment, ensure_ascii=False, indent=2)]
    runs = []
    for command in commands:
        public_command = ["python", *command[1:]]
        begin = time.perf_counter()
        run = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, check=False, encoding="utf-8")
        elapsed = time.perf_counter() - begin
        runs.append({"command": public_command, "exit_code": run.returncode, "elapsed_seconds": round(elapsed, 6)})
        log.extend(["", "$ " + " ".join(public_command), run.stdout,
                    f"Exit code: {run.returncode}; elapsed: {elapsed:.6f} s"])
        print(run.stdout, end="")
        if run.returncode != 0:
            break
    environment.update({"finished_utc": now(), "commands": runs,
                        "all_commands_passed": len(runs) == len(commands) and all(r["exit_code"] == 0 for r in runs)})
    (OUT / "validation.log").write_text("\n".join(log) + "\n", encoding="utf-8")
    (OUT / "environment.json").write_text(json.dumps(environment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tracked = sorted(p for p in ROOT.rglob("*") if p.is_file()
                     and "__pycache__" not in p.parts and p.name != "sha256_manifest.json")
    manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked}
    (OUT / "sha256_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print("Validation log:", "results/validation.log")
    print("All commands passed:", environment["all_commands_passed"])
    return 0 if environment["all_commands_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
