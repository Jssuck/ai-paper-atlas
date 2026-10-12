"""Isolated in-memory source mutations; unexpected errors are never kills."""
import json
from pathlib import Path
import sys
import types
from semantic_probes import check, run_probes

MUTANTS = (
    ("prototype_for_universal", "return left <= right", "return not left or next(x for x in self.objects if x in left) in right"),
    ("overlap_for_inclusion", "return left <= right", "return bool(left & right)"),
    ("strict_for_nonstrict", "return left <= right", "return left < right"),
    ("erase_counterexample", "return next((x for x in self.objects if x in left and x not in right), None)", "return None"),
    ("remove_zero_edge_path", "if source == target:", "if False and source == target:"),
    ("reverse_edges", "adjacent[a].append(b)", "adjacent[b].append(a)"),
    ("direct_edges_only", "while queue:", "for _ in range(min(1, len(queue))):"),
    ("bypass_whole_graph_gate", "if invalid:", "if False and invalid:"),
    ("merge_coincident_extensions", "and self.find_path(a, b) is not None\n                          and self.find_path(b, a) is not None", "and self.same_extension(a, b)"),
    ("rename_reverses_extensions", "return ClassSystem(self.objects, new_labels, self.extensions,", "return ClassSystem(self.objects, new_labels, tuple(reversed(self.extensions)),"),
)


def evaluate(name, source):
    module_name = "_condillac_mutant_" + name
    module = types.ModuleType(module_name)
    sys.modules[module_name] = module
    try:
        try:
            code = compile(source, f"<{name}>", "exec")
            exec(code, module.__dict__)
        except Exception as error:
            return {"name": name, "status": "harness_error", "stage": "compile_or_import",
                    "error_type": type(error).__name__}
        report = run_probes(module)
        if report["errors"]:
            status = "harness_error"
        elif report["failures"]:
            status = "killed_semantic"
        else:
            status = "survived"
        return {"name": name, "status": status, **report}
    finally:
        del sys.modules[module_name]


def run():
    source = Path(__file__).with_name("named_classes.py").read_text(encoding="utf-8")
    unchanged = evaluate("unchanged_control", source)
    check(unchanged["status"] == "survived", "unmodified control failed")
    malformed = evaluate("syntax_error_control", source + "\nTHIS IS NOT VALID PYTHON !\n")
    check(malformed["status"] == "harness_error", "syntax error was misclassified as a semantic kill")
    broken_runtime = evaluate("runtime_error_control", source.replace("return left <= right", "return 1 / 0", 1))
    check(broken_runtime["status"] == "harness_error", "runtime crash was misclassified as a semantic kill")
    reports = []
    for name, old, new in MUTANTS:
        check(source.count(old) == 1, f"mutation target is not unique: {name}")
        report = evaluate(name, source.replace(old, new, 1))
        reports.append(report)
        check(report["status"] == "killed_semantic", f"mutant was not semantically killed: {name}: {report}")
    return {"semantic_mutants": reports, "controls": [unchanged, malformed, broken_runtime],
            "counts": {"killed_semantic": sum(x["status"] == "killed_semantic" for x in reports),
                       "survived": sum(x["status"] == "survived" for x in reports),
                       "harness_error": sum(x["status"] == "harness_error" for x in reports)}}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
