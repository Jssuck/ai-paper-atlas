"""Record independent audit executions and distinguish semantic/framework failures.

Run from the reproduction directory: python3 -B audit/run_audit.py
Only audit/ files are written; author sources, results and logs are read-only.
"""
from datetime import datetime, timezone
import hashlib
from itertools import product
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "audit"
LOGS = AUDIT / "logs"
MODES = (("normal", []), ("O", ["-O"]), ("OO", ["-OO"]))
RECORDS = []


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run(name, mode, flags, args, expected_exit=0):
    command = [sys.executable, "-B", *flags, *args]
    environment = {**os.environ, "PYTHONHASHSEED": "0"}
    start = time.perf_counter()
    result = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, check=False)
    log_path = LOGS / f"{mode}.log"
    block = 1 + sum(record["mode"] == mode for record in RECORDS)
    header = {"block": block, "name": name, "mode": mode, "command": command, "cwd": ".",
              "environment_overrides": {"PYTHONHASHSEED": "0"}, "exit_code": result.returncode,
              "expected_exit_code": expected_exit, "stdout_bytes": len(result.stdout), "stderr_bytes": len(result.stderr)}
    with log_path.open("ab") as handle:
        handle.write(("=== COMMAND " + json.dumps(header, sort_keys=True) + " ===\n").encode())
        handle.write((f"--- STDOUT ({len(result.stdout)} bytes) ---\n").encode())
        handle.write(result.stdout)
        handle.write((f"\n--- STDERR ({len(result.stderr)} bytes) ---\n").encode())
        handle.write(result.stderr)
        handle.write(b"\n=== END COMMAND ===\n\n")
    record = {"name": name, "mode": mode, "command": command, "cwd": ".",
              "environment_overrides": {"PYTHONHASHSEED": "0"}, "exit_code": result.returncode,
              "expected_exit_code": expected_exit, "elapsed_seconds": time.perf_counter() - start,
              "combined_evidence_log": str(log_path.relative_to(ROOT)), "log_block": block,
              "stdout_bytes": len(result.stdout), "stderr_bytes": len(result.stderr),
              "stdout_sha256": sha(result.stdout), "stderr_sha256": sha(result.stderr)}
    match = re.search(rb"Ran (\d+) tests? in", result.stdout + result.stderr)
    if match:
        record["tests_run"] = int(match.group(1))
    RECORDS.append(record)
    require(result.returncode == expected_exit,
            f"{name}/{mode}: exit {result.returncode}, expected {expected_exit}; inspect {log_path.name} block {block}")
    return result


def check_reported(examples, finite):
    # Derive all advertised finite counts without calling finite_checks helpers.
    nrange = range(4)
    relation_cases = sum(2**(n + n*n) for n in nrange)
    successes = sum(2**(len(set(labels))**2) for n in nrange for labels in product((0, 1), repeat=n))
    expected = {
        "relations": {"domain_sizes": list(nrange), "available_representation_labels": 2,
                      "representation_tables": sum(2**n for n in nrange), "relation_cases": relation_cases,
                      "successful_descents": successes, "failed_descents": relation_cases-successes},
        "unary_predicates": {"domain_sizes": list(nrange), "predicate_cases": sum(4**n for n in nrange),
                             "successful_descents": sum(2**len(set(labels)) for n in nrange
                                                         for labels in product((0, 1), repeat=n))},
        "multisets": {"alphabet_size": 2, "input_counts_per_atom": [0, 1, 2], "multisets": 3**2,
                      "ordered_addition_pairs": (3**2)**2, "renaming_maps": 2**2,
                      "renaming_homomorphism_cases": (3**2)**2 * 2**2,
                      "projection_subsets": 2**2, "projection_homomorphism_cases": (3**2)**2 * 2**2,
                      "associativity_cases": (3**2)**3, "scale_factors": list(range(4)),
                      "scale_distribution_cases": (3**2)**2 * 4},
        "policies": {"stimulus_sizes": list(nrange), "actions": 2,
                     "truth_observation_cases": sum(4**n for n in nrange),
                     "individual_prediction_checks": sum(n*4**n for n in nrange)},
    }
    require(finite == expected, "finite_checks.py output disagrees with independent counting formulas")
    require(examples["finite_checks"] == expected, "examples.py finite summary differs")
    r = examples["relation_descent"]
    require(r["objects"] == ["white_1", "white_2", "blue_3"], "article section 3: objects")
    require(r["color_representation"] == {"white_1": "white", "white_2": "white", "blue_3": "blue"},
            "article section 3: colors")
    require(r["rank"] == {"white_1": 1, "white_2": 2, "blue_3": 3}, "article section 3: ranks")
    require(r["unary_is_white_quotient"] == {"white": True, "blue": False}, "white predicate")
    require(r["same_color_descends"] is True and r["strict_rank_order_descends"] is False,
            "article section 3: descent statuses")
    require({tuple(p["pair"]): p["value"] for p in r["same_color_quotient"]} ==
            {(a, b): a == b for a in ("white", "blue") for b in ("white", "blue")}, "same-color quotient")
    require(r["strict_rank_order_conflicts"] == [{"representation_pair": ["white", "white"],
            "true_pair": ["white_1", "white_2"], "false_pair": ["white_1", "white_1"]}],
            "article section 3: permitted exact conflict certificate")
    require(r["empty_domain_quotient"] == {}, "empty quotient example")
    c = examples["composition"]
    require(c["one_unit"] == {"unit": 1} and c["dozen_units"] == {"unit": 12} and c["dozen_total"] == 12,
            "article section 4: dozen")
    require(c["ordinary_set_cardinality"] == 1 and c["duplicate_entries_add"] == {"unit": 12},
            "multiplicity and duplicate input")
    require(c["renaming_loss"] == {"different_inputs": [{"blue": 1, "red": 2}, {"blue": 2, "red": 1}],
            "same_output": {"token": 3}, "outputs_equal": True}, "article section 4: rename collision")
    require(c["projection_loss"] == {"different_inputs": [{"blue": 1, "red": 2}, {"blue": 7, "red": 2}],
            "same_output": {"red": 2}, "outputs_equal": True}, "projection information loss")
    p = examples["finite_observations"]
    require(p["named_stimuli_colors"] == {"white_circle": "white", "white_square": "white",
            "blue_circle": "blue", "blue_square": "blue"}, "article section 6: cards")
    require(p["observations"] == [["white_circle", "1"], ["blue_circle", "0"]], "article section 6: observations")
    require(p["rule_table"] == {"white_circle": "1", "white_square": "1", "blue_circle": "0", "blue_square": "0"},
            "article section 6: color rule")
    require(p["lookup_table"] == {"white_circle": "1", "white_square": "0", "blue_circle": "0", "blue_square": "0"},
            "article section 6: memorization default")
    require((p["admissible_total_tables"], p["survivors"]) == (16, 4), "article section 6: four survivors")
    require((p["held_out"], p["held_out_possible_actions"], p["held_out_status"]) ==
            ("white_square", ["0", "1"], "underdetermined"), "article section 6: query")
    require((p["restricted_rule_only_status"], p["restricted_rule_only_prediction"]) == ("unanimous", "1"),
            "article section 6: conditional guarantee")
    require(p["two_candidate_survivors_after_positive_holdout"] == ["color_rule"], "named two-policy distinction")
    return {"advertised_counts": expected, "article_example_sections_checked": ["3.3", "4.3", "4.4", "6.4"],
            "all_numeric_and_structured_example_fields_checked": True}


def mutation_specs():
    return [
        ("accept_partial_quotient", "return RelationDescent(None if conflicts else quotient, tuple(conflicts))",
         "return RelationDescent(quotient, tuple(conflicts))"),
        ("omit_bad_rectangles", "return RelationDescent(None if conflicts else quotient, tuple(conflicts))",
         "return RelationDescent(None if conflicts else quotient, tuple(conflicts[:1]))"),
        ("symmetrize_ordered_labels", "quotient[block] = next(iter(witnesses))",
         "quotient[tuple(sorted(block))] = next(iter(witnesses))"),
        ("empty_quotient_is_failure", "return self.quotient is not None", "return bool(self.quotient)"),
        ("accept_integer_relations", "if any(type(value) is not bool for value in relation.values()):",
         "if any(value not in (False, True) for value in relation.values()):"),
        ("max_instead_of_multiset_add", "tuple(a + b for a, b in zip(self.counts, other.counts))",
         "tuple(max(a, b) for a, b in zip(self.counts, other.counts))"),
        ("overwrite_rename_collisions", "values[atom] += _natural(count, \"count\")",
         "values[atom] = _natural(count, \"count\")"),
        ("include_zero_in_support_dict", "return {atom: count for atom, count in zip(self.alphabet, self.counts) if count}",
         "return {atom: count for atom, count in zip(self.alphabet, self.counts)}"),
        ("accept_bool_counts", "if type(value) is not int or value < 0:",
         "if not isinstance(value, int) or value < 0:"),
        ("admit_incompatible_policies", "if all(policy.response(s) == a for s, a in observed.items()))",
         "if True or all(policy.response(s) == a for s, a in observed.items()))"),
        ("predict_from_empty_class", "return possibilities[0] if len(possibilities) == 1 else None",
         "return possibilities[0] if len(possibilities) == 1 else ('0' if not possibilities else None)"),
        ("permit_conflicting_observations", "if stimulus in observed and observed[stimulus] != response:",
         "if False:"),
    ]


def main():
    LOGS.mkdir(exist_ok=True)
    for old_log in LOGS.glob("*.log"):
        old_log.unlink()
    (AUDIT / "mutations").mkdir(exist_ok=True)
    started = datetime.now(timezone.utc).isoformat()
    input_paths = [ROOT / name for name in ("model.py", "finite_checks.py", "test_model.py", "examples.py", "run_checks.py")]
    baseline_hashes = {p.name: sha(p.read_bytes()) for p in input_paths}
    env_source = ("import json,sys,platform,os;print(json.dumps({'executable':sys.executable,'version':sys.version,"
                  "'optimization':sys.flags.optimize,'dont_write_bytecode':sys.dont_write_bytecode,"
                  "'platform':platform.platform(),'implementation':platform.python_implementation(),"
                  "'machine':platform.machine(),'PYTHONHASHSEED':os.environ.get('PYTHONHASHSEED')},sort_keys=True))")
    modes = []
    example_outputs = []
    independent_outputs = []
    try:
        for name, flags in MODES:
            environment = json.loads(run("environment", name, flags, ["-c", env_source]).stdout)
            require(environment["optimization"] == {"normal": 0, "O": 1, "OO": 2}[name], "mode probe")
            tests = run("author_tests", name, flags, ["-m", "unittest", "-v", "test_model.py"])
            require(RECORDS[-1].get("tests_run") == 47 and tests.stderr.rstrip().endswith(b"OK"), "47 unittest cases must pass")
            independent = run("independent_checks", name, flags, ["audit/independent_checks.py"])
            independent_outputs.append(independent.stdout)
            finite = run("author_finite_checks", name, flags, ["finite_checks.py"])
            examples = run("author_examples", name, flags, ["examples.py"])
            example_outputs.append(examples.stdout)
            field_check = check_reported(json.loads(examples.stdout), json.loads(finite.stdout))
            modes.append({"mode": name, "environment": environment,
                          "independent_counts": json.loads(independent.stdout)["counts"],
                          "author_result_verification": field_check})
        require(example_outputs[0] == example_outputs[1] == example_outputs[2], "cross-mode examples must be byte-identical")
        require(independent_outputs[0] == independent_outputs[1] == independent_outputs[2], "cross-mode audit must be byte-identical")
        require((ROOT / "results.json").read_bytes() == example_outputs[0], "stored results.json must equal new output")
        for name, _ in MODES:
            require((ROOT / "logs" / f"examples.{name}.json").read_bytes() == example_outputs[0], "stored author example log")
        author_summary = json.loads((ROOT / "run_summary.json").read_text())
        require(author_summary["success"] is True and len(author_summary["commands"]) == 9, "author runner summary")
        for record in author_summary["commands"]:
            require(record["exit_code"] == 0, "author runner unsuccessful command")
            if record["kind"] == "tests":
                require(record["tests_run"] == 47, "author runner test count")
                log = (ROOT / record["stdout_or_combined_log"]).read_text()
                require(re.search(r"Ran 47 tests in", log) is not None and log.rstrip().endswith("OK"), "author runner test log")
        source = (ROOT / "model.py").read_text()
        mutations = []
        for mutation_id, before, after in mutation_specs():
            require(source.count(before) == 1, f"mutation anchor not unique: {mutation_id}")
            mutant = source.replace(before, after, 1)
            path = AUDIT / "mutations" / f"{mutation_id}.py"
            path.write_text(mutant)
            mode_results = []
            for name, flags in MODES:
                result = run("mutation_" + mutation_id, name, flags,
                             ["audit/independent_checks.py", "--group", "probes", "--model-path", str(path.relative_to(ROOT))], 2)
                diagnostic = json.loads(result.stdout)
                require(diagnostic["status"] == "semantic_failure", "mutation must fail semantically, not in framework")
                require(result.stderr == b"", "semantic mutation must not crash with traceback")
                mode_results.append({"mode": name, **diagnostic})
            mutations.append({"id": mutation_id, "before": before, "after": after,
                              "generated_temporary_path": str(path.relative_to(ROOT)), "sha256": sha(path.read_bytes()), "outcomes": mode_results})
            path.unlink()
        (AUDIT / "mutations").rmdir()
        framework_results = []
        for name, flags in MODES:
            result = run("framework_missing_module_probe", name, flags,
                         ["audit/independent_checks.py", "--group", "probes", "--model-path", "audit/nonexistent-model.py"], 3)
            diagnostic = json.loads(result.stdout)
            require(diagnostic["status"] == "framework_error" and diagnostic["type"] == "FileNotFoundError", "framework failure must be classified separately")
            framework_results.append({"mode": name, **diagnostic})
        require({p.name: sha(p.read_bytes()) for p in input_paths} == baseline_hashes, "author source changed during audit")
        report = {"success": True, "started_at_utc": started, "finished_at_utc": datetime.now(timezone.utc).isoformat(),
                  "baseline_code_sha256": baseline_hashes, "commands": RECORDS, "modes": modes,
                  "example_outputs_byte_identical": True, "independent_outputs_byte_identical": True,
                  "stored_author_results_and_logs_match": True, "semantic_mutants_detected_per_mode": len(mutations),
                  "semantic_mutations": mutations, "framework_failure_probes": framework_results,
                  "framework_failures_counted_as_semantic_detections": 0}
        save_json(AUDIT / "execution_report.json", report)
        print(json.dumps({"success": True, "commands": len(RECORDS), "author_tests_per_mode": 47,
                          "semantic_mutants_per_mode": len(mutations), "framework_failures_counted_as_semantic": 0}, indent=2))
        return 0
    except Exception as error:
        save_json(AUDIT / "execution_report.json", {"success": False, "started_at_utc": started,
                  "baseline_code_sha256": baseline_hashes, "commands": RECORDS,
                  "error": f"{type(error).__name__}: {error}"})
        print(f"Audit failed: {type(error).__name__}: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
