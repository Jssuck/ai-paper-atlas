"""Reviewer-authored, executable semantic mutations, distinct from author suite."""

import ast
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
MUTATIONS = (
    ("erase_initial_trace", "habit_model.py", "trace = [initial]", "trace = [Fraction(0)]"),
    ("alpha_decay_instead_of_complement", "habit_model.py", "(1 - alpha) * trace[-1] + alpha * u", "alpha * trace[-1] + alpha * u"),
    ("unweighted_practice", "habit_model.py", "(1 - alpha) * trace[-1] + alpha * u", "(1 - alpha) * trace[-1] + u"),
    ("one_extra_initial_decay", "habit_model.py", "(1 - alpha) ** n * initial", "(1 - alpha) ** (n + 1) * initial"),
    ("one_extra_input_decay", "habit_model.py", "(1 - alpha) ** (n - 1 - k) * u", "(1 - alpha) ** (n - k) * u"),
    ("closed_form_adds_baseline", "habit_model.py", "return (1 - alpha) ** n * initial", "return 1 + (1 - alpha) ** n * initial"),
    ("accept_boolean_initial", "habit_model.py", "isinstance(value, bool) or not isinstance(value, (int, Fraction))", '(isinstance(value, bool) and name != "initial") or not isinstance(value, (int, Fraction))'),
    ("accept_boolean_inputs", "habit_model.py", "type(u) is not int", "not isinstance(u, int)"),
    ("accept_endpoint_alpha", "habit_model.py", "if not 0 < alpha < 1:", "if not 0 <= alpha <= 1:"),
    ("indicator_always_one", "habit_model.py", "int(a == tracked_action)", "int(a == a)"),
    ("ignore_intention_row", "action_model.py", "self.rows[self.intentions.index(intention)][self.contexts.index(context)]", "self.rows[0][self.contexts.index(context)]"),
    ("only_last_observation", "action_model.py", "for context, action in observations)", "for context, action in observations[-1:])"),
    ("reject_matching_observations", "action_model.py", "policy.action(intention, context) == action for context, action in observations", "policy.action(intention, context) != action for context, action in observations"),
    ("empty_record_has_no_candidates", "action_model.py", "if all(policy.action", "if observations and all(policy.action"),
    ("last_context_partition_only", "action_model.py", "for context in contexts)\n        blocks", "for context in contexts[-1:])\n        blocks"),
    ("never_merge_equivalent_intentions", "action_model.py", "signature = tuple(policy.action(intention, context) for context in contexts)", "signature = (intention,)"),
    ("required_strict_subset", "action_model.py", "if required <= code and not code & forbidden", "if required < code and not code & forbidden"),
    ("forbidden_means_required", "action_model.py", "if required <= code and not code & forbidden", "if required <= code and forbidden <= code"),
    ("overlap_has_one_code", "action_model.py", "if required & forbidden:\n        return ()", "if required & forbidden:\n        return (required,)"),
    ("empty_family_forbids", "action_model.py", 'if not codes:\n        return "inconsistent"', 'if not codes:\n        return "all_forbid"'),
    ("any_permit_means_all_permit", "action_model.py", "if judgments == {True}:", "if True in judgments:"),
    ("any_forbid_means_all_forbid", "action_model.py", "if judgments == {False}:", "if False in judgments:"),
    ("allow_duplicate_labels", "action_model.py", "if len(set(values)) != len(values):", "if False:"),
)


def run():
    results, details = [], []
    baseline = subprocess.run([sys.executable, "-B", "independent-review/test_independent.py", "--quick"],
                              cwd=ROOT, text=True, capture_output=True, timeout=30)
    baseline_summary = json.loads(baseline.stdout)
    if baseline.returncode != 0 or baseline_summary["errors"] or baseline_summary["failures"]:
        raise RuntimeError("Unmutated reviewer regression baseline must pass before mutation testing")
    expected_tests = baseline_summary["tests"]
    for name, filename, anchor, replacement in MUTATIONS:
        source = (ROOT / filename).read_text(encoding="utf-8")
        if source.count(anchor) != 1:
            raise RuntimeError(f"Mutation anchor count is not one: {name}")
        mutated = source.replace(anchor, replacement)
        ast.parse(mutated, filename=filename)
        compile(mutated, filename, "exec")
        with tempfile.TemporaryDirectory(prefix="condillac-independent-") as tmp:
            tmp = Path(tmp)
            for module in ("habit_model.py", "action_model.py"):
                shutil.copy2(ROOT / module, tmp / module)
            (tmp / filename).write_text(mutated, encoding="utf-8")
            (tmp / "independent-review").mkdir()
            shutil.copy2(HERE / "test_independent.py", tmp / "independent-review" / "test_independent.py")
            for label, flags in (("normal", []), ("O", ["-O"]), ("OO", ["-OO"])):
                command = [sys.executable, "-B"] + flags + ["independent-review/test_independent.py", "--quick"]
                process = subprocess.run(command, cwd=tmp, text=True, capture_output=True, timeout=30)
                output = (process.stdout + process.stderr).replace(str(tmp), ".").replace(str(ROOT), ".")
                match = re.search(r"Ran (\d+) tests?", output)
                summary = json.loads(process.stdout) if process.stdout.startswith("{") else {}
                count = int(match.group(1)) if match else 0
                failures, errors = summary.get("failures", 0), summary.get("errors", 0)
                killed = process.returncode != 0 and count == expected_tests and failures > 0 and errors == 0
                status = ("KILLED_BY_ASSERTION" if killed else "SURVIVED" if process.returncode == 0
                          else "INVALID_KILL_IMPORT_OR_RUNTIME_ERROR")
                results.append({"mutation": name, "file": filename, "mode": label, "syntax_valid": True,
                                "tests": count, "failures": failures, "errors": errors,
                                "exit_code": process.returncode, "classification": status})
                details.append(f"===== {name}; mode={label} =====\n{output}")
    (HERE / "logs").mkdir(exist_ok=True)
    (HERE / "logs" / "mutation-details.txt").write_text("\n".join(details), encoding="utf-8")
    return {"status": "PASS" if all(r["classification"] == "KILLED_BY_ASSERTION" for r in results) else "FAIL",
            "mutations": len(MUTATIONS), "executions": len(results), "modes": ["normal", "O", "OO"],
            "baseline_tests": expected_tests,
            "policy": "Syntax/import/runtime failures do not count as semantic kills; every reviewer regression test must run, with assertion failures and zero errors.",
            "results": results}


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["status"] == "PASS" else 1)
