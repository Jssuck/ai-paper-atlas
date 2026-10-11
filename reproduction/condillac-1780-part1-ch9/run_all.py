"""Reproduce checked outputs and an environment/source-fingerprint record."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def main():
    logs = ROOT / "logs"
    logs.mkdir(exist_ok=True)
    commands = [
        ("logs/demo.json", [sys.executable, "-B", "demo.py"]),
        ("logs/tests-normal.log", [sys.executable, "-B", "-m", "unittest", "-v", "test_model"]),
        ("logs/tests-O.log", [sys.executable, "-O", "-B", "-m", "unittest", "-v", "test_model"]),
        ("logs/tests-OO.log", [sys.executable, "-OO", "-B", "-m", "unittest", "-v", "test_model"]),
        ("logs/mutation-summary.json", [sys.executable, "-B", "mutation_check.py"]),
    ]
    for mode, flags in (("normal", []), ("O", ["-O"]), ("OO", ["-OO"])):
        commands.extend([
            (f"logs/independent-check-{mode}.json", [sys.executable, *flags, "-B", "independent_check.py"]),
            (f"independent-review/logs/tests-{mode}.log", [sys.executable, *flags, "-B", "independent-review/test_independent.py"]),
            (f"independent-review/logs/harness-{mode}.log", [sys.executable, *flags, "-B", "independent-review/audit_harness.py"]),
        ])
    results = []
    for filename, command in commands:
        process = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
        raw = (process.stdout + process.stderr).replace(str(ROOT), "PROJECT_ROOT")
        destination = ROOT / filename
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(raw, encoding="utf-8")
        results.append({"command": [Path(command[0]).name, *command[1:]],
                        "returncode": process.returncode, "log": filename})
    independent = {}
    for mode in ("normal", "O", "OO"):
        try:
            independent[mode] = json.loads((logs / f"independent-check-{mode}.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            independent[mode] = {"success": False, "reason": "No valid independent result"}
    (logs / "independent-checks.json").write_text(json.dumps(independent, indent=2), encoding="utf-8")
    source_files = [path for path in ROOT.iterdir() if path.suffix in (".py", ".md")]
    source_files.extend((ROOT / "independent-review").glob("*.py"))
    fingerprints = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
                    for path in sorted(source_files)}
    record = {"recorded_at_utc": datetime.now(timezone.utc).isoformat(),
              "python_version": platform.python_version(),
              "implementation": platform.python_implementation(),
              "platform": platform.system(), "platform_release": platform.release(),
              "machine": platform.machine(),
              "interpreter_name": Path(sys.executable).name,
              "python_dependencies": "standard library only",
              "minimum_syntax_version": "3.10",
              "working_directory": ".",
              "commands": results,
              "source_sha256": fingerprints}
    (ROOT / "environment.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    summary = {"success": all(item["returncode"] == 0 for item in results),
               "commands": results}
    print(json.dumps(summary, indent=2))
    return 0 if summary["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
