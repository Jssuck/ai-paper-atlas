"""Reproduce the independent review with portable logs and bound source hashes."""

import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
LOGS = HERE / "logs"


def source_hashes():
    files = sorted(list(ROOT.glob("*.py")) + list(ROOT.glob("*.md")) + list((ROOT / "tests").glob("*.py"))
                   + list(HERE.glob("*.py")) + list(HERE.glob("README.md")))
    return {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in files}


def main():
    LOGS.mkdir(exist_ok=True)
    before = source_hashes()
    started = datetime.now(timezone.utc).isoformat()
    forbidden_asserts = []
    for name in before:
        if name.endswith(".py"):
            tree = ast.parse((ROOT / name).read_text(encoding="utf-8"), filename=name)
            forbidden_asserts.extend(f"{name}:{node.lineno}" for node in ast.walk(tree) if isinstance(node, ast.Assert))
    environment = {"python": sys.version, "implementation": platform.python_implementation(),
                   "platform": platform.platform(), "executable_name": Path(sys.executable).name,
                   "byteorder": sys.byteorder, "invocation_optimize": sys.flags.optimize,
                   "cwd": ". (reproduction root)", "utc_started": started,
                   "stdlib_only": True, "network_or_installation_required": False}
    (LOGS / "environment.json").write_text(json.dumps(environment, indent=2) + "\n", encoding="utf-8")
    stages, reviewer_summaries, demos = [], [], []
    for label, flags in (("normal", []), ("O", ["-O"]), ("OO", ["-OO"])):
        tasks = (("independent", ["independent-review/test_independent.py"]),
                 ("author-unit", ["-m", "unittest", "discover", "-s", "tests", "-v"]),
                 ("author-oracle", ["finite_oracle.py"]), ("demo", ["demo.py"]))
        for name, args in tasks:
            command = [sys.executable, "-B"] + flags + args
            begin = time.perf_counter()
            process = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=120)
            seconds = time.perf_counter() - begin
            output = (process.stdout + process.stderr).replace(str(ROOT), ".")
            log = f"logs/{name}-{label}.txt"
            (HERE / log).write_text(output, encoding="utf-8")
            stages.append({"stage": f"{name}-{label}", "command": [Path(sys.executable).name, "-B"] + flags + args,
                           "cwd": ".", "exit_code": process.returncode, "seconds": round(seconds, 6), "log": log})
            if name == "independent" and process.returncode == 0:
                reviewer_summaries.append(json.loads(process.stdout))
            if name == "demo":
                demos.append(process.stdout)
    begin = time.perf_counter()
    args = ["independent-review/mutations_independent.py"]
    process = subprocess.run([sys.executable, "-B"] + args, cwd=ROOT, text=True, capture_output=True, timeout=180)
    (LOGS / "mutations.json").write_text((process.stdout + process.stderr).replace(str(ROOT), "."), encoding="utf-8")
    stages.append({"stage": "independent-semantic-mutations-all-modes", "command": [Path(sys.executable).name, "-B"] + args,
                   "cwd": ".", "exit_code": process.returncode, "seconds": round(time.perf_counter() - begin, 6),
                   "log": "logs/mutations.json"})
    after = source_hashes()
    summaries_agree = len(reviewer_summaries) == 3 and len({json.dumps({key: value for key, value in r.items() if key != "optimize"}, sort_keys=True)
                                                          for r in reviewer_summaries}) == 1
    clean_paths = []
    for path in LOGS.iterdir():
        if path.is_file() and any(token in path.read_text(encoding="utf-8") for token in ("/" + "workspace/", "/" + "root/", "/" + "tmp/condillac-")):
            clean_paths.append(str(path.relative_to(HERE)))
    passed = (all(s["exit_code"] == 0 for s in stages) and before == after and not forbidden_asserts
              and summaries_agree and len(set(demos)) == 1 and not clean_paths)
    report = {"status": "PASS" if passed else "FAIL", "utc_started": started,
              "utc_finished": datetime.now(timezone.utc).isoformat(),
              "scope": "Independent reviewer scripts; bounded checks and targeted mutations are not a proof of all inputs or philosophical claims.",
              "sources_unchanged_during_run": before == after, "bare_assert_nodes": forbidden_asserts,
              "reviewer_summaries_identical_except_optimize": summaries_agree,
              "demo_text_identical": len(set(demos)) == 1, "private_path_hits": clean_paths,
              "independent_summaries": reviewer_summaries, "stages": stages, "source_sha256": after}
    (LOGS / "verification.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "stages": len(stages), "source_files": len(after),
                      "details": "independent-review/logs/verification.json"}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
