"""Run only the independent audit, bind exact inputs and actual mode logs.

Run from the model directory: python3 -B independent-review/record_review.py.
The published paths are relative; child processes use the invoking interpreter.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "independent-review"
SPEC = "../../papers/1780/condillac-logic-part2-ch4.zh-CN.md"
INPUTS = ("finite_language.py", "examples.py", "demo.py", "test_finite_language.py",
          "verify.py", "record_evidence.py", "MODEL.zh-CN.md", "README.md",
          "WALKTHROUGH.zh-CN.md", "independent-review/check_language.py",
          "independent-review/record_review.py", "independent-review/review.zh-CN.md")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def snapshot():
    return {name: digest((ROOT / name).read_bytes()) for name in INPUTS}


def spec_digest():
    source = (ROOT / SPEC).read_text(encoding="utf-8")
    section = source[source.index("## 8 "):source.index("## 11 ")]
    return digest(section.encode("utf-8"))


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def check_producer_evidence():
    report = json.loads((ROOT / "evidence/verification.json").read_text(encoding="utf-8"))
    require(report["success"] is True, "producer did not report success")
    require(len(report["runs"]) == 6, "expected six producer runs")
    for run in report["runs"]:
        require(run["exit_code"] == 0, "producer run failed")
        require(digest((ROOT / "evidence" / run["log"]).read_bytes()) == run["log_sha256"],
                "producer log hash mismatch")
    for name, expected in report["source_sha256"].items():
        require(digest((ROOT / name).read_bytes()) == expected, "producer source hash mismatch: " + name)
    for mode, flag in (("normal", 0), ("O", 1), ("OO", 2)):
        log = (ROOT / "evidence" / f"verify-{mode}.txt").read_text(encoding="utf-8")
        require(f"optimize={flag}\n" in log, "producer actual optimization mode mismatch")
        require("PASS: 24 focused test methods" in log, "producer focused test result missing")
    demos = [(ROOT / "evidence" / f"demo-{mode}.txt").read_bytes() for mode in ("normal", "O", "OO")]
    require(len(set(demos)) == 1, "producer demo outputs differ")
    return {p.relative_to(ROOT).as_posix(): digest(p.read_bytes())
            for p in sorted((ROOT / "evidence").iterdir()) if p.is_file()}


def main():
    report = {"started_utc": datetime.now(timezone.utc).isoformat(),
              "python_version": sys.version, "implementation": platform.python_implementation(),
              "command_note": "Display commands use python3; actual child processes use the invoking sys.executable.",
              "cwd": ".", "runs": []}
    before = snapshot()
    spec_before = spec_digest()
    producer_before = check_producer_evidence()
    for mode, flags, expected_opt in (("normal", [], 0), ("O", ["-O"], 1), ("OO", ["-OO"], 2)):
        relative = "independent-review/check_language.py"
        result = subprocess.run([sys.executable, "-B", *flags, relative], cwd=ROOT,
                                capture_output=True, text=True, timeout=60)
        log_name = f"audit-{mode}.txt"
        output = result.stdout + ("\n[stderr]\n" + result.stderr if result.stderr else "")
        (OUT / log_name).write_text(output, encoding="utf-8")
        actual_mode = f"optimize={expected_opt}\n" in result.stdout
        report["runs"].append({"display_command": ["python3", "-B", *flags, relative],
                               "exit_code": result.returncode, "actual_mode_confirmed": actual_mode,
                               "log": "independent-review/" + log_name,
                               "log_sha256": digest((OUT / log_name).read_bytes())})
    after = snapshot()
    producer_after = check_producer_evidence()
    report["input_sha256"] = before
    report["inputs_unchanged"] = before == after
    report["producer_evidence_sha256"] = producer_before
    report["producer_evidence_unchanged"] = producer_before == producer_after
    report["spec_scope"] = {"path": SPEC, "from_heading_inclusive": "## 8 ",
                            "to_heading_exclusive": "## 11 ", "utf8_sha256": spec_before,
                            "unchanged": spec_before == spec_digest()}
    report["success"] = (report["inputs_unchanged"] and report["producer_evidence_unchanged"]
                         and report["spec_scope"]["unchanged"] and
                         all(run["exit_code"] == 0 and run["actual_mode_confirmed"] for run in report["runs"]))
    report["finished_utc"] = datetime.now(timezone.utc).isoformat()
    (OUT / "verification.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"success": report["success"], "runs": len(report["runs"]),
                      "report": "independent-review/verification.json"}, sort_keys=True))
    return 0 if report["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
