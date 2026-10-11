"""Reproduce the independent review without modifying author files.

Run: python independent-review/run_review.py
Outputs are confined to independent-review/. Existing review outputs are replaced.
"""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
AUTHOR_INPUTS = ["model.py", "enumerate_model.py", "demo.py", "verify.py", "tests/test_model.py", "README.md", "MODEL.zh-CN.md", "WALKTHROUGH.zh-CN.md", "validation/census.json", "validation/demo-output.txt", "validation/manifest.json", "validation/author-validation.log"]


def digests():
    return {path: sha256((ROOT / path).read_bytes()).hexdigest() for path in AUTHOR_INPUTS}


def main():
    started = datetime.now(timezone.utc).isoformat()
    before = digests()
    lines = ["INDEPENDENT REVIEW EXECUTION LOG", "UTC start: " + started, "Python: " + platform.python_version(), "Working directory: reproduction/condillac-1780-part1-ch3", ""]
    commands = [
        (["demo.py"], "rerun-demo.txt"),
        (["-m", "unittest", "discover", "-s", "tests", "-v"], None),
        (["-O", "-m", "unittest", "discover", "-s", "tests", "-v"], None),
        (["-OO", "-m", "unittest", "discover", "-s", "tests", "-v"], None),
        (["enumerate_model.py"], "rerun-census.json"),
        (["independent-review/oracle.py"], "oracle-normal.json"),
        (["-O", "independent-review/oracle.py"], "oracle-O.json"),
        (["-OO", "independent-review/oracle.py"], "oracle-OO.json"),
    ]
    results = []
    ok = True
    for args, filename in commands:
        run = subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True, check=False)
        # Keep logs portable: traceback paths, if any, refer to the public tree.
        stdout, stderr = (run.stdout.replace(str(ROOT), "."), run.stderr.replace(str(ROOT), "."))
        command = "python " + " ".join(args)
        lines.extend(("$ " + command, "exit code: " + str(run.returncode), "--- stdout ---", stdout, "--- stderr ---", stderr, ""))
        if filename:
            (OUT / filename).write_text(stdout, encoding="utf-8")
        results.append(dict(command=command, exit_code=run.returncode, output_file=filename))
        ok = ok and run.returncode == 0
        print(command + ": exit " + str(run.returncode), flush=True)
    after = digests()
    invariant = before == after
    author_manifest = json.loads((ROOT / "validation/manifest.json").read_text())
    manifest_matches = all(before[name] == digest for name, digest in author_manifest["sha256"].items())
    demo_matches = (OUT / "rerun-demo.txt").read_bytes() == (ROOT / "validation/demo-output.txt").read_bytes()
    census_matches = json.loads((OUT / "rerun-census.json").read_text()) == json.loads((ROOT / "validation/census.json").read_text())
    modes = [json.loads((OUT / name).read_text()) for name in ("oracle-normal.json", "oracle-O.json", "oracle-OO.json")] if ok else []
    mode_payloads = [{k: v for k, v in mode.items() if k != "optimize"} for mode in modes]
    modes_agree = len(mode_payloads) == 3 and mode_payloads[0] == mode_payloads[1] == mode_payloads[2]
    ok = ok and invariant and manifest_matches and demo_matches and census_matches and modes_agree
    ended = datetime.now(timezone.utc).isoformat()
    final_checks = dict(inputs_unchanged=invariant, author_manifest_matches=manifest_matches, saved_demo_matches=demo_matches, saved_census_matches=census_matches, optimization_modes_agree=modes_agree)
    lines.extend(("Final checks: " + json.dumps(final_checks), "UTC end: " + ended, "PASS" if ok else "FAIL"))
    (OUT / "execution.log").write_text("\n".join(lines) + "\n", encoding="utf-8")
    summary = dict(review_kind="independent review, not author validation", utc_start=started, utc_end=ended, python=platform.python_version(), commands=results, final_checks=final_checks, status="PASS" if ok else "FAIL", reviewed_sha256=before, input_sha256_after=after, review_scripts_sha256={name: sha256((OUT / name).read_bytes()).hexdigest() for name in ("oracle.py", "run_review.py")})
    (OUT / "results.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
