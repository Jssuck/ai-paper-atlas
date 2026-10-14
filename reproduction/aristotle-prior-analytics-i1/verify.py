"""Run the author checks in three interpreter modes and save actual logs."""

from datetime import datetime, timezone
from pathlib import Path
import platform
import shlex
import subprocess
import sys


def main() -> int:
    root = Path(__file__).resolve().parent
    logs = [
        "Author-run verification; this file does not claim an independent audit.",
        "UTC run start: " + datetime.now(timezone.utc).isoformat(),
        "Working directory: " + str(root),
        "Python executable: " + sys.executable,
        "Python version: " + sys.version.replace("\n", " "),
        "Platform: " + platform.platform(),
        "Dependencies: Python standard library only; no installation or network step.",
        "",
    ]
    reports = []
    successful = True
    for flags in ((), ("-O",), ("-OO",)):
        command = [sys.executable, *flags, "-B", "-m", "unittest", "-v", "test_model"]
        result = subprocess.run(command, cwd=root, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, check=False)
        logs.extend(["$ " + shlex.join(command), result.stdout.rstrip(),
                     "Exit code: " + str(result.returncode), ""])
        successful = successful and result.returncode == 0
        command = [sys.executable, *flags, "-B", "demo.py"]
        result = subprocess.run(command, cwd=root, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, check=False)
        logs.extend(["$ " + shlex.join(command),
                     "Exit code: " + str(result.returncode),
                     "Report bytes: " + str(len(result.stdout))])
        if result.stderr:
            logs.append(result.stderr.decode("utf-8", errors="replace").rstrip())
        logs.append("")
        successful = successful and result.returncode == 0
        reports.append(result.stdout)
    identical = len(reports) == 3 and bool(reports[0]) and all(r == reports[0] for r in reports)
    successful = successful and identical
    logs.append("Normal/-O/-OO report bytes identical: " + str(identical))
    logs.append("Overall author verification passed: " + str(successful))
    if successful:
        (root / "report.json").write_bytes(reports[0])
    (root / "verification.txt").write_text("\n".join(logs) + "\n", encoding="utf-8")
    print("\n".join(logs))
    return 0 if successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
