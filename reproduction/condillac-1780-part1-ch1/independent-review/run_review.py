"""Capture this separate review without altering the author's source or logs.

Run from any directory: python3 -B path/to/independent-review/run_review.py
Only this directory's logs are updated. Author verify.py runs in a temporary copy.
"""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    review = Path(__file__).resolve().parent
    root = review.parent
    release = root.parents[1]
    article = release / "papers/1780/condillac-logic-part1-ch1.zh-CN.md"
    logs = review / "logs"
    logs.mkdir(exist_ok=True)
    source_files = sorted(root.glob("*.py")) + sorted(root.glob("*.md")) + [article]
    before = {str(p.relative_to(release)): digest(p) for p in source_files}
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED="0")
    results = []
    aliases = {str(root): str(root.relative_to(release))}

    def public_path(value):
        rendered = str(value)
        for absolute, relative in aliases.items():
            rendered = rendered.replace(absolute, relative)
        return rendered

    def execute(name, command, cwd):
        started = datetime.now(timezone.utc).isoformat()
        result = subprocess.run(command, cwd=cwd, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, check=False, timeout=600)
        output = logs / name
        output.write_bytes(result.stdout)
        results.append({"command": list(map(public_path, command)), "cwd": public_path(cwd),
                        "started_at_utc": started, "exit_code": result.returncode,
                        "log": str(output.relative_to(review)), "sha256": digest(output)})
        print(f"{name}: exit {result.returncode}", flush=True)
        return result.returncode == 0

    passed = True
    for optimized in (False, True):
        suffix = "-optimized" if optimized else ""
        prefix = [sys.executable, "-B"] + (["-O"] if optimized else [])
        jobs = ((f"author-unittest{suffix}.txt", ["-m", "unittest", "-v", "test_model"], root),
                (f"author-exhaustive{suffix}.json", [str(root / "exhaustive.py")], Path("/tmp")),
                (f"robustness{suffix}.txt", [str(review / "test_robustness.py")], Path("/tmp")),
                (f"independent-oracle{suffix}.json", [str(review / "independent_oracle.py")], Path("/tmp")),
                (f"counts-mutations{suffix}.json", [str(review / "check_counts_and_mutations.py")], Path("/tmp")))
        for name, args, cwd in jobs:
            passed = execute(name, prefix + args, cwd) and passed
    passed = execute("walkthrough-unrelated-cwd.txt",
                     [sys.executable, "-B", str(root / "walkthrough.py")], Path("/tmp")) and passed
    # Check the author's aggregate entry point from a different CWD and a path
    # containing spaces, preserving original author logs and deliverable hashes.
    with tempfile.TemporaryDirectory(prefix="condillac review ") as temporary:
        snapshot = Path(temporary) / "teaching package"
        snapshot.mkdir()
        aliases[str(snapshot)] = "<temporary-copy>"
        for path in source_files:
            if path.parent == root:
                shutil.copy2(path, snapshot / path.name)
        passed = execute("verify-unrelated-cwd.txt",
                         [sys.executable, "-B", str(snapshot / "verify.py")], Path("/tmp")) and passed
        verify_result = snapshot / "logs/verification.json"
        if verify_result.exists():
            shutil.copy2(verify_result, logs / "copied-author-verification.json")
    equal = {}
    for name in ("author-exhaustive", "independent-oracle", "counts-mutations"):
        equal[name] = ((logs / f"{name}.json").read_bytes()
                       == (logs / f"{name}-optimized.json").read_bytes())
    after = {str(p.relative_to(release)): digest(p) for p in source_files}
    passed = passed and all(equal.values()) and before == after
    report = {"status": "PASS" if passed else "FAIL", "recorded_at_utc":
              datetime.now(timezone.utc).isoformat(),
              "environment": {"python": sys.version, "platform": platform.platform(),
                              "machine": platform.machine(), "network_used": False},
              "author_sources_unchanged_during_run": before == after,
              "path_note": "Package paths are recorded relative to the release root; the isolated CLI copy is labeled <temporary-copy>. Commands actually received resolved absolute script paths when invoked from /tmp.",
              "normal_optimized_json_equal": equal, "subprocesses": results,
              "audited_source_sha256": after,
              "review_code_sha256": {p.name: digest(p) for p in sorted(review.glob("*.py"))}}
    (logs / "review-verification.json").write_text(json.dumps(report, ensure_ascii=False,
                                                            indent=2) + "\n", encoding="utf-8")
    print(f"review status: {report['status']}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
