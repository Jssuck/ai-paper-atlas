"""Re-run and record author validation; this is not an independent audit."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import platform
import subprocess
import sys


def main() -> int:
    root = Path(__file__).resolve().parent
    output = root / "validation"
    output.mkdir(exist_ok=True)
    started = datetime.now(timezone.utc).isoformat()
    commands = [
        (["demo.py"], "demo-output.txt"),
        (["-m", "unittest", "discover", "-s", "tests", "-v"], None),
        (["-O", "-m", "unittest", "discover", "-s", "tests", "-v"], None),
        (["-OO", "-m", "unittest", "discover", "-s", "tests", "-v"], None),
        (["enumerate_model.py"], "census.json"),
    ]
    lines = ["AUTHOR VALIDATION — not independent review", f"UTC start: {started}",
             f"Python: {platform.python_version()}", f"Implementation: {platform.python_implementation()}"]
    successful = True
    for arguments, filename in commands:
        result = subprocess.run([sys.executable, *arguments], cwd=root, text=True, capture_output=True, check=False)
        label = "python " + " ".join(arguments)
        lines.extend(("", "$ " + label, f"exit code: {result.returncode}", "--- stdout ---", result.stdout,
                      "--- stderr ---", result.stderr))
        print(f"{label}: exit {result.returncode}")
        successful = successful and result.returncode == 0
        if filename:
            (output / filename).write_text(result.stdout, encoding="utf-8")
    lines.extend(("", f"UTC end: {datetime.now(timezone.utc).isoformat()}", "ALL COMMANDS PASSED" if successful else "VALIDATION FAILED"))
    (output / "author-validation.log").write_text("\n".join(lines) + "\n", encoding="utf-8")
    paths = ["model.py", "enumerate_model.py", "demo.py", "verify.py", "tests/test_model.py",
             "README.md", "MODEL.zh-CN.md", "WALKTHROUGH.zh-CN.md"]
    manifest = {"validation_kind": "author validation, not independent review", "utc_start": started,
                "python": platform.python_version(), "all_commands_passed": successful,
                "sha256": {path: hashlib.sha256((root / path).read_bytes()).hexdigest() for path in paths}}
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
