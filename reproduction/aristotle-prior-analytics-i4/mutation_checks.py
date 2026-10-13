#!/usr/bin/env python3
"""Sixteen targeted semantic/boundary mutations; temporary copies are discarded.

This is a small fault-sensitivity exercise, not independent auditing and not
an estimate of all possible bugs. A mutant is killed only by a recorded test
assertion failure, never merely by a crash, import error, or timeout.
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent
MUTATIONS = (
    ("A_reverse_subset", "return x <= y", "return y <= x", "test_atomic_truth_against_independent_oracle"),
    ("A_strict_subset", "return x <= y", "return x < y", "test_atomic_truth_against_independent_oracle"),
    ("A_add_existential_import", "return x <= y", "return bool(x) and x <= y", "test_complement_pairs_and_empty_vacuity"),
    ("E_inequality_instead_disjoint", "return x.isdisjoint(y)", "return x != y", "test_atomic_truth_against_independent_oracle"),
    ("I_subset_instead_overlap", "return bool(x & y)", "return bool(x) and x <= y", "test_atomic_truth_against_independent_oracle"),
    ("O_reverse_difference", "return bool(x - y)", "return bool(y - x)", "test_atomic_truth_against_independent_oracle"),
    ("O_symmetric_difference", "return bool(x - y)", "return bool(x ^ y)", "test_atomic_truth_against_independent_oracle"),
    ("O_overlap_instead_difference", "return bool(x - y)", "return bool(x & y)", "test_atomic_truth_against_independent_oracle"),
    ("omit_outside_all_type", "combinations(range(8), size)", "combinations(range(1, 8), size)", "test_enumeration_complete_and_unique"),
    ("omit_all_three_type", "combinations(range(8), size)", "combinations(range(7), size)", "test_enumeration_complete_and_unique"),
    ("omit_eight_type_support", "for size in range(1, 9)", "for size in range(1, 8)", "test_enumeration_complete_and_unique"),
    ("nonempty_any_not_all_terms", "or all(self.extension(t) for t in TERM_BITS)", "or any(self.extension(t) for t in TERM_BITS)", "test_enumeration_complete_and_unique"),
    ("major_argument_reversal", 'model.holds(major, "M", "P")', 'model.holds(major, "P", "M")', "test_all_premise_pairs_have_models"),
    ("minor_argument_reversal", 'model.holds(minor, "S", "M")', 'model.holds(minor, "M", "S")', "test_all_premise_pairs_have_models"),
    ("forward_reverse_swapped", '("P", "S") if reverse else ("S", "P")', '("S", "P") if reverse else ("P", "S")', "test_exact_forward_classification"),
    ("bool_accepted_as_membership_int", "if type(value) is not int:", "if not isinstance(value, int):", "test_support_numeric_type_boundaries"),
)


def main():
    source = (ROOT / "categorical.py").read_text(encoding="utf-8")
    records = []
    for name, original, replacement, test_name in MUTATIONS:
        if source.count(original) != 1:
            raise RuntimeError(f"mutation anchor is not unique: {name}")
        with tempfile.TemporaryDirectory(prefix="i4-mutation-") as directory:
            target = pathlib.Path(directory)
            (target / "categorical.py").write_text(source.replace(original, replacement, 1), encoding="utf-8")
            shutil.copyfile(ROOT / "walkthrough.py", target / "walkthrough.py")
            shutil.copytree(ROOT / "tests", target / "tests", ignore=shutil.ignore_patterns("__pycache__"))
            command = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v", "-k", test_name]
            result = subprocess.run(command, cwd=target, text=True, capture_output=True, timeout=30)
            output = result.stdout + result.stderr
            killed = (result.returncode == 1 and "FAIL:" in output and "AssertionError" in output
                      and "ERROR:" not in output and "Ran 1 test" in output)
            records.append({"mutation": name, "test": test_name, "command": command,
                            "returncode": result.returncode, "killed_by_assertion": killed,
                            "test_output": output})
    report = {"scope": "16 targeted mutations; no claim of independent audit or universal fault coverage",
              "killed": sum(row["killed_by_assertion"] for row in records),
              "total": len(records), "records": records}
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["killed"] == report["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
