"""Run the actual standard-library checks and record commands and source hashes."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
MODES = {"normal": [], "O": ["-O"], "OO": ["-OO"]}


def main():
    logs = ROOT / "logs"
    logs.mkdir(exist_ok=True)
    commands = [("logs/demo.json", [sys.executable, "-B", "demo.py"])]
    for mode, flags in MODES.items():
        commands.extend([
            (f"logs/tests-{mode}.log", [sys.executable, *flags, "-B", "-m", "unittest", "-v", "test_model"]),
            (f"logs/exhaustive-{mode}.json", [sys.executable, *flags, "-B", "exhaustive.py"]),
        ])
    commands.append(("logs/mutation-summary.json", [sys.executable, "-B", "mutation_check.py"]))
    independent = ROOT / "independent-review" / "run_audit.py"
    independent_present = independent.is_file()
    if independent_present:
        commands.append(("logs/independent-run-audit.log",
                         [sys.executable, "-B", "independent-review/run_audit.py"]))
    results = []
    for filename, command in commands:
        destination = ROOT / filename
        destination.parent.mkdir(parents=True, exist_ok=True)
        timed_out = False
        try:
            process = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=180)
            raw = process.stdout + process.stderr
            code = process.returncode
        except subprocess.TimeoutExpired:
            timed_out = True
            raw = "Run-all command exceeded 180 seconds. No pass claimed.\n"
            code = None
        destination.write_text(raw.replace(str(ROOT), "PROJECT_ROOT"), encoding="utf-8")
        results.append({"command": [Path(command[0]).name, *command[1:]],
                        "returncode": code, "timed_out": timed_out, "log": filename})
    sources = [path for path in ROOT.rglob("*")
               if path.is_file() and path.suffix in (".py", ".md")
               and not any(part.startswith(".mutation-") for part in path.parts)]
    hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in sorted(sources)}
    record = {"recorded_at_utc": datetime.now(timezone.utc).isoformat(),
              "python_version": platform.python_version(),
              "implementation": platform.python_implementation(),
              "operating_system": platform.system(), "system_release": platform.release(),
              "machine": platform.machine(), "interpreter": Path(sys.executable).name,
              "dependencies": "Python standard library only", "minimum_syntax_version": "3.10",
              "working_directory": ".", "commands": results, "source_sha256": hashes}
    (ROOT / "environment.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    summary = {"success": all(row["returncode"] == 0 for row in results),
               "independent_entrypoint_present": independent_present, "commands": results}
    (logs / "run-all-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0 if summary["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
