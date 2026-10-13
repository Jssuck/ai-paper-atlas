"""Run the same real checks in three interpreter modes and retain evidence."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys


ROOT = Path(__file__).resolve().parent


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> int:
    logs = ROOT / "logs"
    logs.mkdir(exist_ok=True)
    environment = {
        "started_utc": utc_now(),
        "python_executable": Path(sys.executable).name,
        "python_version": sys.version,
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "working_directory": ".",
        "execution_context": "this reproduction directory",
        "command_representation": "Interpreter basename is recorded; each subprocess uses the running interpreter.",
        "dependencies": "Python standard library only; Python 3.10 or later syntax",
        "source_sha256": {
            name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in ("model.py", "examples.py", "test_model.py", "run_checks.py")
        },
    }
    runs = []
    for mode, options in (("normal", []), ("O", ["-O"]), ("OO", ["-OO"])):
        for script in ("test_model.py", "examples.py"):
            command = [sys.executable, *options, script]
            started = utc_now()
            completed = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                                       encoding="utf-8", check=False)
            prefix = f"{mode}-{Path(script).stem}"
            stdout_path, stderr_path = logs / f"{prefix}.stdout.txt", logs / f"{prefix}.stderr.txt"
            stdout_path.write_text(completed.stdout, encoding="utf-8")
            stderr_path.write_text(completed.stderr, encoding="utf-8")
            record = {
                "mode": mode, "script": script,
                "command": [Path(sys.executable).name, *options, script],
                "started_utc": started, "finished_utc": utc_now(),
                "returncode": completed.returncode,
                "stdout": str(stdout_path.relative_to(ROOT)),
                "stderr": str(stderr_path.relative_to(ROOT)),
            }
            try:
                record["output"] = json.loads(completed.stdout)
            except json.JSONDecodeError as error:
                record["output_parse_error"] = str(error)
            runs.append(record)
            if script == "test_model.py" and "output" in record:
                report = record["output"]
                print(f"{mode}: {report['tests_run']} unittest methods; "
                      f"failures={report['failures']}; errors={report['errors']}; "
                      f"finite cases attempted={report['finite_case_groups_attempted']}")
            else:
                print(f"{mode}: {script}: exit={completed.returncode}")
    successful = all(run["returncode"] == 0 and "output_parse_error" not in run for run in runs)
    tests = [run for run in runs if run["script"] == "test_model.py"]
    successful = successful and all(run.get("output", {}).get("successful") is True for run in tests)
    environment["finished_utc"] = utc_now()
    (ROOT / "environment.json").write_text(json.dumps(environment, indent=2) + "\n", encoding="utf-8")
    summary = {
        "successful": successful,
        "subprocesses_run": len(runs),
        "unittest_method_executions": sum(run.get("output", {}).get("tests_run", 0) for run in tests),
        "count_note": "The same test suite is repeated in three modes; these are not distinct test designs.",
        "runs": runs,
    }
    (ROOT / "results.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print("PASS" if successful else "FAIL")
    return 0 if successful else 1


if __name__ == "__main__":
    sys.exit(main())
