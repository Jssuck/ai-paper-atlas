"""Run actual normal/-O/-OO processes and preserve auditable local evidence."""
from datetime import datetime, timezone
import hashlib
import json
import locale
from pathlib import Path
import platform
import subprocess
import sys
import quality_check


def digest(data):
    return hashlib.sha256(data).hexdigest()


def files(root):
    return {path.name: digest(path.read_bytes())
            for path in sorted(root.iterdir()) if path.suffix in (".py", ".md")}


def main():
    root = Path(__file__).resolve().parent
    evidence = root / "evidence"
    evidence.mkdir(exist_ok=True)
    before = files(root)
    report = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {
            "python_version": sys.version, "python_executable": sys.executable,
            "implementation": platform.python_implementation(), "python_build": platform.python_build(),
            "python_compiler": platform.python_compiler(), "platform": platform.platform(),
            "uname": {key: value for key, value in platform.uname()._asdict().items() if key != "node"}, "machine": platform.machine(),
            "byteorder": sys.byteorder, "filesystem_encoding": sys.getfilesystemencoding(),
            "preferred_encoding": locale.getpreferredencoding(False),
            "working_directory": ".", "recorder_flags": repr(sys.flags),
            "environment_scope": "Runtime and OS details only; account secrets, hostnames, and unrelated environment variables are not recorded.",
            "working_directory_note": "Published cwd is normalized to the package-relative directory . for portable public evidence; the absolute execution path is omitted.",
        },
        "source_sha256_before": before,
        "runs": [],
    }
    outputs = {}
    for mode, flags in (("normal", ()), ("O", ("-O",)), ("OO", ("-OO",))):
        for program in ("verify.py", "demo.py"):
            command = [sys.executable, "-B", *flags, program]
            completed = subprocess.run(command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
            filename = f"{Path(program).stem}-{mode}.txt"
            (evidence / filename).write_bytes(completed.stdout)
            outputs[(program, mode)] = completed.stdout
            report["runs"].append({"mode": mode, "program": program, "command": command,
                                   "working_directory": ".", "optimization_level": len(flags[0]) - 1 if flags else 0,
                                   "exit_code": completed.returncode, "log": filename,
                                   "log_sha256": digest(completed.stdout)})
    demo_equal = len({outputs[("demo.py", mode)] for mode in ("normal", "O", "OO")}) == 1
    summaries = []
    optimization_levels_verified = True
    for expected_level, mode in enumerate(("normal", "O", "OO")):
        runtime_lines = [line for line in outputs[("verify.py", mode)].splitlines() if line.startswith(b"RUNTIME ")]
        try:
            runtime = json.loads(runtime_lines[0][len(b"RUNTIME "):])
            optimization_levels_verified = optimization_levels_verified and len(runtime_lines) == 1 and runtime["optimization_level"] == expected_level
        except (IndexError, ValueError, KeyError):
            optimization_levels_verified = False
        summaries.append(tuple(line for line in outputs[("verify.py", mode)].splitlines()
                               if line.startswith((b"EXHAUSTIVE ", b"MUTATION ", b"PASS: "))))
    summary_equal = all(len(summary) == 3 for summary in summaries) and len(set(summaries)) == 1
    # The report filename must exist for the README's local link check.
    destination = evidence / "verification.json"
    destination.write_text("{}\n", encoding="utf-8")
    quality_destination = evidence / "source-quality.json"
    quality_destination.write_text("{}\n", encoding="utf-8")
    try:
        quality = quality_check.run()
    except Exception as error:
        quality = {"status": "failed", "type": type(error).__name__, "message": str(error)}
    quality_destination.write_text(json.dumps(quality, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    after = files(root)
    report.update({"source_sha256_after": after, "sources_unchanged": before == after,
                   "demo_outputs_byte_identical": demo_equal,
                   "verification_semantic_summaries_identical": summary_equal,
                   "actual_child_optimization_levels_verified": optimization_levels_verified,
                   "source_quality": quality["status"],
                   "source_quality_sha256": digest(quality_destination.read_bytes()),
                   "finished_utc": datetime.now(timezone.utc).isoformat()})
    passed = all(run["exit_code"] == 0 for run in report["runs"]) and before == after and demo_equal and summary_equal and optimization_levels_verified and quality["status"] == "passed"
    report["status"] = "passed" if passed else "failed"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("status", "sources_unchanged", "demo_outputs_byte_identical", "verification_semantic_summaries_identical", "source_quality")}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
