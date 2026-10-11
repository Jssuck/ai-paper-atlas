"""Valid semantic mutations executed against the actual unit tests under -OO."""

import ast
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parent
MUTATIONS = (
    ("remove_decay", "habit_model.py",
     "trace.append((1 - alpha) * trace[-1] + alpha * u)",
     "trace.append(trace[-1] + alpha * u)"),
    ("invert_practice", "habit_model.py",
     "trace.append((1 - alpha) * trace[-1] + alpha * u)",
     "trace.append((1 - alpha) * trace[-1] + alpha * (1 - u))"),
    ("reverse_time_weights", "habit_model.py",
     "(1 - alpha) ** (n - 1 - k) * u", "(1 - alpha) ** k * u"),
    ("invert_action_indicator", "habit_model.py",
     "int(a == tracked_action)", "int(a != tracked_action)"),
    ("any_observation_suffices", "action_model.py",
     "if all(policy.action(intention, context) == action for context, action in observations)",
     "if any(policy.action(intention, context) == action for context, action in observations)"),
    ("discard_later_observations", "action_model.py",
     "if all(policy.action(intention, context) == action for context, action in observations)",
     "if all(policy.action(intention, context) == action for context, action in observations[:1])"),
    ("discard_later_contexts", "action_model.py",
     "signature = tuple(policy.action(intention, context) for context in contexts)",
     "signature = tuple(policy.action(intention, context) for context in contexts[:1])"),
    ("ignore_required_actions", "action_model.py",
     "if required <= code and not code & forbidden", "if not code & forbidden"),
    ("ignore_forbidden_actions", "action_model.py",
     "if required <= code and not code & forbidden", "if required <= code"),
    ("empty_family_permits", "action_model.py",
     'if not codes:\n        return "inconsistent"', 'if not codes:\n        return "all_permit"'),
)


def run():
    results = []
    details = []
    for name, filename, original, replacement in MUTATIONS:
        with tempfile.TemporaryDirectory(prefix=".mutation-", dir=ROOT) as temporary:
            temporary = Path(temporary)
            for source in ("habit_model.py", "action_model.py", "demo.py"):
                shutil.copy2(ROOT / source, temporary / source)
            shutil.copytree(ROOT / "tests", temporary / "tests", ignore=shutil.ignore_patterns("__pycache__"))
            source = (temporary / filename).read_text(encoding="utf-8")
            if source.count(original) != 1:
                raise RuntimeError(f"mutation anchor must occur exactly once: {name}")
            mutated = source.replace(original, replacement)
            ast.parse(mutated, filename=filename)
            (temporary / filename).write_text(mutated, encoding="utf-8")
            process = subprocess.run([sys.executable, "-B", "-OO", "-m", "unittest", "discover", "-s", "tests"],
                                     cwd=temporary, text=True, capture_output=True, timeout=30)
            output = (process.stdout + process.stderr).replace(str(temporary), ".")
            ran = re.search(r"Ran (\d+) tests?", output)
            summary = re.search(r"FAILED \(([^)]+)\)", output)
            counts = {} if summary is None else dict((k, int(v)) for k, v in re.findall(r"(\w+)=(\d+)", summary.group(1)))
            killed = (process.returncode != 0 and ran is not None and int(ran.group(1)) == 27
                      and counts.get("failures", 0) > 0 and counts.get("errors", 0) == 0)
            results.append({"name": name, "module": filename, "syntax_valid": True,
                            "tests_run": int(ran.group(1)) if ran else 0,
                            "failures": counts.get("failures", 0), "errors": counts.get("errors", 0),
                            "exit_code": process.returncode, "status": "KILLED" if killed else "NOT_VALIDLY_KILLED"})
            details.append(f"===== {name} =====\n{output}")
    (ROOT / "logs").mkdir(exist_ok=True)
    (ROOT / "logs" / "mutation-details.txt").write_text("\n".join(details), encoding="utf-8")
    return {"status": "PASS" if all(r["status"] == "KILLED" for r in results) else "FAIL",
            "scope": "10 targeted valid author-written semantic mutations; not exhaustive or external review",
            "mode": "-OO", "mutations": results}


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["status"] == "PASS" else 1)
