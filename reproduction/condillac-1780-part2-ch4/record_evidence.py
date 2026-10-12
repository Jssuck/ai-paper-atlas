"""Re-run delivered source under normal/-O/-OO and record actual outputs.

No packages, network access, installs, or remote writes are needed. Persisted
commands are portable displays, not private absolute executable/workspace paths.
"""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys


ROOT = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hashes() -> dict[str, str]:
    return {p.name: sha256(p) for p in sorted(ROOT.iterdir())
            if p.is_file() and p.suffix in (".py", ".md")}


def save_report(out: Path, report: dict) -> None:
    (out / "verification.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    out = ROOT / "evidence"
    out.mkdir(exist_ok=True)
    report = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "platform": platform.platform(),
        "command_convention": "Portable display: executable basename only; actual execution uses sys.executable. cwd is relative to this package.",
        "source_sha256_before": source_hashes(),
        "runs": [],
        "status": "running",
        "success": False,
    }
    # A timeout/crash must not leave a previous successful manifest as the latest report.
    save_report(out, report)
    demos = []
    success = True
    for mode, flags in (("normal", []), ("O", ["-O"]), ("OO", ["-OO"])):
        for script in ("verify.py", "demo.py"):
            command = [sys.executable, "-B", *flags, script]
            result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=60)
            log_name = f"{script[:-3]}-{mode}.txt"
            text = result.stdout
            if result.stderr:
                text += "\n[stderr]\n" + result.stderr
            (out / log_name).write_text(text, encoding="utf-8")
            report["runs"].append({"command": [Path(sys.executable).name, *command[1:]],
                                   "cwd": ".", "exit_code": result.returncode,
                                   "log": log_name, "log_sha256": sha256(out / log_name)})
            save_report(out, report)
            success = success and result.returncode == 0
            if script == "demo.py":
                demos.append(result.stdout)
    report["demo_outputs_equal_across_modes"] = len(set(demos)) == 1
    report["source_sha256"] = source_hashes()
    report["source_hashes_match_before_after"] = report["source_sha256_before"] == report["source_sha256"]
    success = success and report["demo_outputs_equal_across_modes"] and report["source_hashes_match_before_after"]
    report["finished_utc"] = datetime.now(timezone.utc).isoformat()
    report["status"] = "complete"
    report["success"] = success
    save_report(out, report)
    print(json.dumps({"success": success, "runs": len(report["runs"]),
                      "demo_outputs_equal_across_modes": report["demo_outputs_equal_across_modes"],
                      "source_hashes_match_before_after": report["source_hashes_match_before_after"],
                      "report": "evidence/verification.json"}, sort_keys=True))
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
