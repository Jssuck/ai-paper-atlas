"""Inject bounded wrong-result probes into verification entry points.

No production files are changed. Logs contain portable command descriptions;
the host interpreter/source-directory absolute paths are deliberately omitted.
Optional argv[1] selects an earlier saved source snapshot for regression evidence.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
PROBES = {
    "exhaustive_wrong_query": '''
import model, exhaustive
model.Reconstruction.difference = lambda self, u, v: (999,) * self.book.dimension
exhaustive.check_family(1, (-2, -1, 0, 1, 2), 4)
''',
    "walkthrough_wrong_fixture": '''
import walkthrough
walkthrough.TRUTH["A"] = (999,)
walkthrough.run_examples()
''',
}
rows = []
for name, probe in PROBES.items():
    for flag in (None, "-O", "-OO"):
        body = "import sys\nsys.dont_write_bytecode = True\nsys.path.insert(0, " + repr(str(ROOT)) + ")\ntry:\n"
        body += "".join("    " + line + "\n" for line in probe.strip().splitlines())
        body += ('except Exception as error:\n'
                 '    print(type(error).__name__ + ": " + str(error))\n'
                 '    raise SystemExit(2)\n'
                 'print("PASS returned despite injected wrong result")\n')
        command = [sys.executable] + ([flag] if flag else []) + ["-c", body]
        run = subprocess.run(command, text=True, capture_output=True)
        rows.append({"probe": name, "optimization": flag or "normal",
                     "portable_command": "python3 " + ((flag + " ") if flag else "") +
                     "-c <bounded " + name + " probe in this script>",
                     "exit_code": run.returncode,
                     "wrong_result_rejected": run.returncode == 2,
                     "stdout": run.stdout.strip(), "stderr": run.stderr.strip()})
passed = all(row["wrong_result_rejected"] for row in rows)
print(json.dumps({"status": "PASS" if passed else "FAIL_OPEN_REPRODUCED", "python": sys.version,
                  "normalization": "Local absolute interpreter and source paths omitted; probe outcomes unchanged.",
                  "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                                    for name in ("model.py", "exhaustive.py", "walkthrough.py")},
                  "probes": rows}, ensure_ascii=False, indent=2))
raise SystemExit(0 if passed else 1)
