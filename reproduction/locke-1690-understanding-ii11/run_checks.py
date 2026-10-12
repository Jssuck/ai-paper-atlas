"""Capture actual stdlib test/example runs in three Python optimization modes."""

import hashlib
import json
from pathlib import Path
import platform
import re
import subprocess
import sys
import time
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parent
LOGS = ROOT / "logs"


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def main():
    LOGS.mkdir(exist_ok=True)
    started = timestamp()
    probe_source = ("import json,sys; print(json.dumps({'executable':sys.executable,"
                    "'version':sys.version,'optimization':sys.flags.optimize,"
                    "'bytecode_writes_disabled':sys.dont_write_bytecode},sort_keys=True))")
    records = []
    outputs = []
    environments = []
    for name, flags in (("normal", []), ("O", ["-O"]), ("OO", ["-OO"])):
        commands = (
            ("environment", ["-c", probe_source], f"environment.{name}.json"),
            ("tests", ["-m", "unittest", "-v", "test_model.py"], f"tests.{name}.log"),
            ("examples", ["examples.py"], f"examples.{name}.json"),
        )
        for kind, args, filename in commands:
            command = [sys.executable, "-B", *flags, *args]
            clock_start = time.perf_counter()
            process = subprocess.run(command, cwd=ROOT, capture_output=True, check=False)
            elapsed = time.perf_counter() - clock_start
            stdout_path = LOGS / filename
            stderr_path = LOGS / f"{kind}.{name}.stderr.log"
            if kind == "tests":
                # unittest normally writes to stderr. The combined log preserves
                # both captured streams; the unmodified stderr is also retained.
                stdout_path.write_bytes(process.stdout + process.stderr)
            else:
                stdout_path.write_bytes(process.stdout)
            stderr_path.write_bytes(process.stderr)
            record = {"mode": name, "kind": kind, "command": command,
                      "exit_code": process.returncode, "elapsed_seconds": elapsed,
                      "stdout_or_combined_log": str(stdout_path.relative_to(ROOT)),
                      "stderr_log": str(stderr_path.relative_to(ROOT))}
            if kind == "tests":
                match = re.search(rb"Ran (\d+) tests? in", process.stdout + process.stderr)
                record["tests_run"] = int(match.group(1)) if match else None
            elif kind == "environment" and process.returncode == 0:
                environments.append({"mode": name, **json.loads(process.stdout)})
            elif kind == "examples" and process.returncode == 0:
                json.loads(process.stdout)
                outputs.append(process.stdout)
                record["output_sha256"] = hashlib.sha256(process.stdout).hexdigest()
            records.append(record)
    commands_passed = all(record["exit_code"] == 0 for record in records)
    outputs_equal = len(outputs) == 3 and outputs[0] == outputs[1] == outputs[2]
    probes_verified = [entry["optimization"] for entry in environments] == [0, 1, 2]
    tests_identified = all((record.get("tests_run") or 0) > 0 for record in records if record["kind"] == "tests")
    success = commands_passed and outputs_equal and probes_verified and tests_identified
    environment = {"recorded_at_utc": started, "platform": platform.platform(),
                   "machine": platform.machine(), "python_implementation": platform.python_implementation(),
                   "dependency_policy": "Python standard library only; no installation or network required",
                   "interpreter_modes": environments}
    summary = {"started_at_utc": started, "finished_at_utc": timestamp(),
               "success": success, "all_commands_passed": commands_passed,
               "all_modes_verified": probes_verified, "example_outputs_byte_identical": outputs_equal,
               "test_counts_read_from_logs": tests_identified, "commands": records}
    (ROOT / "environment.json").write_text(json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (ROOT / "run_summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if success:
        (ROOT / "results.json").write_bytes(outputs[0])
    print(json.dumps({key: value for key, value in summary.items() if key != "commands"}, indent=2, sort_keys=True))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
