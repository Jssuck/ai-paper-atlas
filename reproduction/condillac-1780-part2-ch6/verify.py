"""Run the local verification matrix and save auditable evidence, without installs."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "evidence"
AUTHOR_SOURCES = (
    "condillac_model.py", "demo.py", "mutation_check.py", "test_condillac_model.py",
    "test_mutation_check.py", "verify.py", "MODEL.zh-CN.md", "README.md", "WALKTHROUGH.zh-CN.md",
)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    EVIDENCE.mkdir(exist_ok=True)
    env = dict(os.environ)
    env.pop("PYTHONOPTIMIZE", None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONHASHSEED"] = "0"
    records = []

    def run(label, arguments):
        command = [sys.executable, *arguments]
        start = time.monotonic()
        result = subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True, timeout=120)
        stdout_path = EVIDENCE / f"{label}.stdout.txt"
        stderr_path = EVIDENCE / f"{label}.stderr.txt"
        stdout_path.write_text(result.stdout, encoding="utf-8")
        stderr_path.write_text(result.stderr, encoding="utf-8")
        record = {"label": label, "command": command, "returncode": result.returncode,
                  "seconds": round(time.monotonic() - start, 6),
                  "stdout": str(stdout_path.relative_to(ROOT)), "stderr": str(stderr_path.relative_to(ROOT)),
                  "stdout_sha256": sha256(stdout_path), "stderr_sha256": sha256(stderr_path)}
        records.append(record)
        return result

    env_probe = "import json,platform,sys; print(json.dumps({'python':sys.version,'executable':sys.executable,'platform':platform.platform(),'optimize':sys.flags.optimize},indent=2))"
    demos = []
    mutation_summaries = []
    counts = []
    for mode, flags in (("normal", []), ("O", ["-O"]), ("OO", ["-OO"])):
        run(f"environment_{mode}", [*flags, "-c", env_probe])
        test_result = run(f"tests_{mode}", [*flags, "-m", "unittest", "discover", "-v"])
        match = re.search(r"Ran (\d+) tests?", test_result.stderr)
        counts.append(int(match.group(1)) if match else None)
        mutations = run(f"mutations_{mode}", [*flags, "mutation_check.py"])
        try:
            mutation_summaries.append(json.loads(mutations.stdout))
        except json.JSONDecodeError:
            mutation_summaries.append(None)
        demos.append(run(f"demo_{mode}", [*flags, "demo.py"]).stdout)
    walkthrough_command = (
        "import pathlib,re; "
        "text=pathlib.Path('WALKTHROUGH.zh-CN.md').read_text(encoding='utf-8'); "
        "blocks=re.findall(r'^```python\\n(.*?)^```',text,re.M|re.S); "
        "exec(compile('\\n'.join(blocks),'WALKTHROUGH.zh-CN.md','exec'))"
    )
    run("walkthrough", ["-c", walkthrough_command])
    try:
        demo_equal = all(json.loads(demos[0]) == json.loads(item) for item in demos[1:])
    except (IndexError, json.JSONDecodeError):
        demo_equal = False
    sources = [ROOT / name for name in AUTHOR_SOURCES]
    summary = {
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "executable": sys.executable, "platform": platform.platform(),
        "working_directory": "reproduction/condillac-1780-part2-ch6/", "dependencies": "Python standard library only",
        "environment_overrides": {"PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1", "PYTHONOPTIMIZE": "removed, flags explicit"},
        "test_counts_by_mode": dict(zip(("normal", "O", "OO"), counts)),
        "demo_outputs_equal": demo_equal,
        "mutation_summaries_by_mode": dict(zip(("normal", "O", "OO"), mutation_summaries)),
        "source_sha256": {str(path.relative_to(ROOT)): sha256(path) for path in sources},
        "runs": records,
    }
    passed = (all(r["returncode"] == 0 for r in records)
              and all(count is not None and count > 0 for count in counts)
              and len(set(counts)) == 1 and demo_equal
              and all(s is not None and s["baseline_passes"] == 6 and s["behavior_detected"] == 6 and s["harness_errors"] == 0
                      for s in mutation_summaries))
    summary["passed"] = passed
    (EVIDENCE / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"passed": passed, "runs": len(records), "test_counts": counts,
                      "demo_outputs_equal": demo_equal, "summary": "evidence/summary.json"}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
