"""Independent audit oracles. No assertions, third-party packages, or author checks.

Exit 0: checks passed; 2: semantic discrepancy; 3: audit/import/framework error.
--group probes gives small targeted semantic checks used to validate mutations.
"""
import argparse
from collections import Counter
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
COUNTS = {}


class AuditFailure(Exception):
    pass


def check(actual, expected, name):
    if actual != expected:
        raise AuditFailure(f"{name}: actual={actual!r}; expected={expected!r}")


def rejected(call, name):
    try:
        call()
    except ValueError:
        return
    raise AuditFailure(f"{name}: expected ValueError but input was accepted")


def load_model(path):
    if not path.is_file():
        raise FileNotFoundError(f"model input does not exist: {path.name}")
    spec = importlib.util.spec_from_file_location("audit_subject_model", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def probes(m):
    # Counterexamples are chosen directly from the advertised semantic contracts.
    d = ("x", "y", "z", "w")
    rep = dict(zip(d, ("a", "a", "b", "b")))
    rel = {(x, y): (x, y) in {("x", "y"), ("x", "z"), ("z", "x"), ("z", "w")}
           for x in d for y in d}
    result = m.descend_relation(d, rep, rel)
    check(result.quotient, None, "probe.relation.reject_conflicting_quotient")
    check({c.representation_pair for c in result.conflicts}, set(product(("a", "b"), repeat=2)),
          "probe.relation.every_bad_rectangle")
    for c in result.conflicts:
        check(rel[c.true_pair], True, "probe.relation.true_witness")
        check(rel[c.false_pair], False, "probe.relation.false_witness")
    directional = {(x, y): rep[x] == "a" and rep[y] == "b" for x in d for y in d}
    check(m.descend_relation(d, rep, directional).quotient,
          {("a", "a"): False, ("a", "b"): True, ("b", "a"): False, ("b", "b"): False},
          "probe.relation.direction_is_retained")
    check(m.descend_relation((), {}, {}).quotient, {}, "probe.relation.empty_image")
    check(m.descend_relation((), {}, {}).descends, True, "probe.relation.empty_is_success")
    check(m.descend_unary(d, rep, {x: rep[x] == "a" for x in d}).quotient,
          {"a": True, "b": False}, "probe.unary.retained_color")
    rejected(lambda: m.descend_relation(("x",), {"x": "a"}, {("x", "x"): 1}),
             "probe.relation.integer_is_not_bool")
    left = m.Multiset.from_pairs(("a", "b"), (("a", 2), ("b", 1)))
    right = m.Multiset.from_pairs(("a", "b"), (("a", 1), ("b", 2)))
    check(left.add(right).counts, (3, 3), "probe.multiset.coordinate_addition")
    check(left.rename(("token",), {"a": "token", "b": "token"}).counts, (3,),
          "probe.multiset.collision_adds_counts")
    check(m.Multiset.from_pairs(("a", "b"), (("a", 2), ("a", 3), ("b", 0))).as_dict(),
          {"a": 5}, "probe.multiset.duplicates_accumulate_zero_absent")
    rejected(lambda: left.scale(True), "probe.multiset.bool_is_not_natural")
    rejected(lambda: m.Multiset.from_pairs(("a",), (("outside", 0),)),
             "probe.multiset.zero_unknown_atom")
    d = ("first", "second")
    a = ("0", "1")
    policies = m.enumerate_policies(d, a)
    space = m.version_space(d, a, policies, (("first", "1"),))
    check({p.responses for p in space.survivors}, {("1", "0"), ("1", "1")},
          "probe.policy.compatibility")
    check(space.possible_actions("second"), ("0", "1"), "probe.policy.held_out_ambiguity")
    check(space.unanimous("second"), None, "probe.policy.no_false_unanimity")
    empty = m.version_space(d, a, (), ())
    check(empty.status("second"), "empty_version_space", "probe.policy.empty_status")
    check(empty.unanimous("second"), None, "probe.policy.no_empty_vacuous_prediction")
    rejected(lambda: m.version_space(d, a, policies, (("first", "0"), ("first", "1"))),
             "probe.policy.conflicting_observations")
    rejected(lambda: space.possible_actions("outside"), "probe.policy.outside_query")
    COUNTS["targeted_probes"] = "passed"


def relations(m):
    # Oracle constructs every quotient table, expands it to a bitmask on X^2,
    # then looks up every possible input table. It never calls the model to
    # compute an expectation and does not use a fiber-constancy existence test.
    case_count = success_count = rep_count = conflict_count = 0
    unary_cases = unary_success = 0
    by_size = []
    for n in range(4):
        d = tuple(f"o{i}" for i in range(n))
        ordered_pairs = tuple((x, y) for x in d for y in d)
        current_cases = current_success = 0
        for codes in product(("a", "b", "unused_if_absent"), repeat=n):
            rep_count += 1
            rep = dict(zip(d, codes))
            image = tuple(sorted(set(codes)))
            label_pairs = tuple((a, b) for a in image for b in image)
            expansions = {}
            for output in product((False, True), repeat=len(label_pairs)):
                quotient = dict(zip(label_pairs, output))
                encoded = sum(int(quotient[rep[x], rep[y]]) << i for i, (x, y) in enumerate(ordered_pairs))
                if encoded in expansions:
                    raise AuditFailure("oracle.quotient_uniqueness: duplicate expanded quotient")
                expansions[encoded] = quotient
            for encoded in range(1 << len(ordered_pairs)):
                rel = {p: bool(encoded & (1 << i)) for i, p in enumerate(ordered_pairs)}
                expected = expansions.get(encoded)
                result = m.descend_relation(d, rep, rel)
                check(result.quotient, expected, "relation.exhaustive_factorization")
                check(result.descends, encoded in expansions, "relation.descends_status")
                # Separate witness audit requires exactly every bad rectangle,
                # no omissions/duplicates, and the documented first witness.
                expected_conflicts = {}
                for block in label_pairs:
                    positions = [p for p in ordered_pairs if (rep[p[0]], rep[p[1]]) == block]
                    yes = [p for p in positions if rel[p]]
                    no = [p for p in positions if not rel[p]]
                    if yes and no:
                        expected_conflicts[block] = (yes[0], no[0])
                actual_conflicts = {c.representation_pair: (c.true_pair, c.false_pair) for c in result.conflicts}
                check(actual_conflicts, expected_conflicts, "relation.complete_conflict_certificates")
                check(len(result.conflicts), len(expected_conflicts), "relation.no_duplicate_certificates")
                success_count += int(encoded in expansions)
                current_success += int(encoded in expansions)
                case_count += 1
                current_cases += 1
                conflict_count += len(expected_conflicts)
            unary_expansions = {}
            for vals in product((False, True), repeat=len(image)):
                q = dict(zip(image, vals))
                unary_expansions[tuple(q[rep[x]] for x in d)] = q
            for values in product((False, True), repeat=n):
                p = dict(zip(d, values))
                result = m.descend_unary(d, rep, p)
                check(result.quotient, unary_expansions.get(values), "unary.exhaustive_factorization")
                expected_conflicts = {}
                for label in image:
                    yes = [x for x in d if rep[x] == label and p[x]]
                    no = [x for x in d if rep[x] == label and not p[x]]
                    if yes and no:
                        expected_conflicts[label] = (yes[0], no[0])
                check({label: (yes, no) for label, yes, no in result.conflicts}, expected_conflicts,
                      "unary.complete_conflict_certificates")
                check(len(result.conflicts), len(expected_conflicts), "unary.no_duplicate_certificates")
                unary_cases += 1
                unary_success += int(values in unary_expansions)
        by_size.append({"domain_size": n, "cases": current_cases, "successful": current_success})
    check(case_count, sum(3**n * 2**(n*n) for n in range(4)), "relation.case_count_formula")
    check((rep_count, case_count, success_count, unary_cases, unary_success),
          (40, 13975, 3475, 259, 163), "relation.independent_totals")
    COUNTS["relations"] = {"available_labels": 3, "representation_tables": rep_count,
                           "relation_cases": case_count, "successful": success_count,
                           "failed": case_count - success_count, "conflict_certificates": conflict_count,
                           "by_domain_size": by_size, "unary_cases": unary_cases,
                           "unary_successful": unary_success}


def bags(m):
    # Counter expansion is the oracle; the subject stores fixed vectors.
    atoms = ("a", "b", "c")
    target = ("x", "y")
    inputs = list(product(range(3), repeat=3))
    additions = renamings = projections = scalings = associativity = 0
    for lc in inputs:
        l_tokens = [a for a, count in zip(atoms, lc) for _ in range(count)]
        left = m.Multiset.from_pairs(reversed(atoms), ((t, 1) for t in l_tokens))
        check(left.counts, lc, "multiset.token_encoding")
        check(left.support, tuple(a for a in atoms if a in l_tokens), "multiset.support")
        check(left.as_dict(), dict(Counter(l_tokens)), "multiset.counter_view")
        for rc in inputs:
            r_tokens = [a for a, count in zip(atoms, rc) for _ in range(count)]
            right = m.Multiset(atoms, rc)
            all_tokens = l_tokens + r_tokens
            total = left.add(right)
            check(total.as_dict(), dict(Counter(all_tokens)), "multiset.independent_addition")
            check(total.total, len(all_tokens), "multiset.total_addition")
            check(total, right.add(left), "multiset.commutative")
            additions += 1
            for images in product(target, repeat=3):
                mapping = dict(zip(atoms, images))
                expected = dict(Counter(mapping[t] for t in all_tokens))
                output = total.rename(target, mapping)
                check(output.as_dict(), expected, "multiset.rename_counter_oracle")
                check(output, left.rename(target, mapping).add(right.rename(target, mapping)),
                      "multiset.rename_homomorphism")
                check(output.total, len(all_tokens), "multiset.rename_total")
                renamings += 1
            for k in range(len(atoms) + 1):
                for kept in combinations(atoms, k):
                    expected = dict(Counter(t for t in all_tokens if t in kept))
                    projected = total.project(kept)
                    check(projected.as_dict(), expected, "multiset.projection_counter_oracle")
                    check(projected.alphabet, kept, "multiset.projection_alphabet")
                    check(projected, left.project(kept).add(right.project(kept)),
                          "multiset.projection_homomorphism")
                    projections += 1
            for factor in range(4):
                check(total.scale(factor).as_dict(), dict(Counter(all_tokens * factor)),
                      "multiset.scale_counter_oracle")
                check(total.scale(factor), left.scale(factor).add(right.scale(factor)),
                      "multiset.scale_distributive")
                scalings += 1
            for tc in inputs:
                third = m.Multiset(atoms, tc)
                check(total.add(third), left.add(right.add(third)), "multiset.associative")
                associativity += 1
    # Exhaustive collision/injectivity equivalence on zero/one-unit witnesses.
    injection_cases = 0
    for source_size in range(4):
        source = atoms[:source_size]
        for target_size in range(4):
            labels = ("x", "y", "z")[:target_size]
            for values in product(labels, repeat=source_size):
                mapping = dict(zip(source, values))
                vectors = [tuple(0 for _ in source)] + [tuple(int(i == j) for i in range(source_size))
                                                        for j in range(source_size)]
                images = [m.Multiset(source, v).rename(labels, mapping).counts for v in vectors]
                check(len(set(images)) == len(images), len(set(values)) == len(values),
                      "multiset.injectivity_unit_witnesses")
                injection_cases += 1
    COUNTS["multisets"] = {"source_atoms": 3, "input_multisets": len(inputs), "addition_pairs": additions,
                           "renaming_cases": renamings, "projection_cases": projections,
                           "scale_cases": scalings, "associativity_cases": associativity,
                           "injectivity_maps": injection_cases}


def policies(m):
    # Exhaust every admitted subset of binary tables on up to three stimuli.
    # Observations are enumerated as partial functions (unseen/0/1), unlike the
    # author's truth-table x mask enumeration, which repeats some records.
    cases = queries = empty = unanimous = ambiguous = 0
    for n in range(4):
        d = tuple(f"s{i}" for i in range(n))
        actions = ("0", "1")
        raw_tables = tuple(product(actions, repeat=n))
        all_policies = m.enumerate_policies(d, actions)
        check({p.responses for p in all_policies}, set(raw_tables), "policy.enumeration_complete")
        check(len(all_policies), len(raw_tables), "policy.enumeration_no_duplicates")
        for included in product((False, True), repeat=len(raw_tables)):
            # Build independent policies directly, not from enumerate_policies.
            admitted = tuple(m.DeterministicPolicy(f"p{i}", d, table)
                             for i, (table, keep) in enumerate(zip(raw_tables, included)) if keep)
            for partial in product((None, "0", "1"), repeat=n):
                obs = tuple((d[i], val) for i, val in enumerate(partial) if val is not None)
                compatible = tuple(p for p in admitted if tuple(p.responses[i] for i in range(n)
                                   if partial[i] is not None) == tuple(x for x in partial if x is not None))
                result = m.version_space(d, actions, admitted, obs)
                check(result.survivors, compatible, "policy.independent_subset_filter")
                cases += 1
                for i, stimulus in enumerate(d):
                    expected = tuple(sorted({p.responses[i] for p in compatible}))
                    status = "empty_version_space" if not expected else "unanimous" if len(expected) == 1 else "underdetermined"
                    check(result.possible_actions(stimulus), expected, "policy.possible_actions")
                    check(result.status(stimulus), status, "policy.status")
                    check(result.unanimous(stimulus), expected[0] if len(expected) == 1 else None,
                          "policy.nonvacuous_unanimity")
                    queries += 1
                    empty += not expected
                    unanimous += len(expected) == 1
                    ambiguous += len(expected) > 1
    check(cases, sum(2 ** (2**n) * 3**n for n in range(4)), "policy.case_count_formula")
    check(queries, sum(n * 2 ** (2**n) * 3**n for n in range(4)), "policy.query_count_formula")
    # Complete behavior still does not distinguish named mechanisms.
    p = m.DeterministicPolicy("mechanism_a", ("s",), ("0",))
    q = m.DeterministicPolicy("mechanism_b", ("s",), ("0",))
    check(m.version_space(("s",), ("0",), (p, q), (("s", "0"),)).survivors, (p, q),
          "policy.extensional_equivalence_not_mechanism_identity")
    COUNTS["policies"] = {"stimulus_sizes": [0, 1, 2, 3], "all_admissible_subsets": True,
                          "class_partial_observation_cases": cases, "prediction_queries": queries,
                          "empty_queries": empty, "unanimous_queries": unanimous,
                          "underdetermined_queries": ambiguous}


def invalid_inputs(m):
    tests = []
    def add(name, call):
        tests.append((name, call))
    d = ("x", "y")
    rep = {"x": "a", "y": "a"}
    r = {p: False for p in product(d, repeat=2)}
    for bad in ("xy", b"xy", ("x", "x"), ("",), (1,), (True,)):
        add(f"relation.domain.{bad!r}", lambda bad=bad: m.descend_relation(bad, {}, {}))
    for bad in ({}, {"x": "a"}, {**rep, "outside": "a"}, {**rep, "x": ""}, {**rep, "x": 1}):
        add(f"relation.representation.{bad!r}", lambda bad=bad: m.descend_relation(d, bad, r))
    for bad in ({p: v for p, v in r.items() if p != ("x", "y")}, {**r, ("outside", "x"): True}):
        add("relation.exact_ordered_pair_domain", lambda bad=bad: m.descend_relation(d, rep, bad))
    for value in (0, 1, -1, 0.0, 1.0, None, "False"):
        add(f"relation.strict_boolean.{value!r}", lambda value=value: m.descend_relation(d, rep, {**r, ("x", "y"): value}))
        add(f"unary.strict_boolean.{value!r}", lambda value=value: m.descend_unary(d, rep, {"x": value, "y": False}))
    add("relation.empty_extra_representation", lambda: m.descend_relation((), {"x": "a"}, {}))
    add("relation.empty_extra_pair", lambda: m.descend_relation((), {}, {("a", "a"): False}))
    add("unary.exact_domain", lambda: m.descend_unary(d, rep, {"x": False}))
    unit = m.Multiset.from_pairs(("a",), (("a", 1),))
    for value in (-1, True, False, 1.0, "1", None):
        add(f"multiset.from_pairs.count.{value!r}", lambda value=value: m.Multiset.from_pairs(("a",), (("a", value),)))
        add(f"multiset.direct.count.{value!r}", lambda value=value: m.Multiset(("a",), (value,)))
        add(f"multiset.scale.factor.{value!r}", lambda value=value: unit.scale(value))
    class IntSubclass(int):
        pass
    add("multiset.count.strict_int_subclass", lambda: m.Multiset(("a",), (IntSubclass(1),)))
    add("multiset.negative_input_no_cancellation", lambda: m.Multiset.from_pairs(("a",), (("a", 3), ("a", -2))))
    for alphabet, counts in [(("b", "a"), (1, 0)), (("a", "a"), (1, 1)), (("a",), ()), (["a"], (1,)), (("a",), [1])]:
        add("multiset.canonical_storage", lambda alphabet=alphabet, counts=counts: m.Multiset(alphabet, counts))
    for bad in (("outside",), ("a", "a"), "a"):
        add("multiset.projection_domain", lambda bad=bad: unit.project(bad))
    for target, mapping in [((), {"a": "x"}), (("x",), {}), (("x",), {"a": "outside"}),
                            (("x",), {"a": "x", "outside": "x"}), (("x", "x"), {"a": "x"}),
                            (("x",), {"a": True})]:
        add("multiset.rename_total_function", lambda target=target, mapping=mapping: unit.rename(target, mapping))
    add("multiset.add_distinct_alphabet", lambda: unit.add(m.Multiset.from_pairs(("b",))))
    add("multiset.add_nonmultiset", lambda: unit.add(1))
    check(m.Multiset.from_pairs(()).rename(("x",), {}).counts, (0,), "multiset.empty_source_to_nonempty_target")
    check(m.Multiset.from_pairs(()).rename((), {}).counts, (), "multiset.empty_rename")
    p = m.DeterministicPolicy("p", d, ("0", "1"))
    for obs in ((("outside", "0"),), (("x", "outside"),), (("x", "0"), ("x", "1")),
                ((True, "0"),), (("x", 0),)):
        add("policy.observation_domain_and_consistency", lambda obs=obs: m.version_space(d, ("0", "1"), (p,), obs))
    for bad in (m.DeterministicPolicy("bad", tuple(reversed(d)), ("0", "1")),
                m.DeterministicPolicy("bad", d, ("0", "outside")), object()):
        add("policy.admissible_domain_and_range", lambda bad=bad: m.version_space(d, ("0", "1"), (bad,), ()))
    add("policy.duplicate_names", lambda: m.version_space(d, ("0", "1"), (p, p), ()))
    for actions in ((), ("0", "0"), (True,), "01"):
        add("policy.action_alphabet", lambda actions=actions: m.enumerate_policies(d, actions))
        add("policy.version_action_alphabet", lambda actions=actions: m.version_space(d, actions, (), ()))
    for domain in (("x", "x"), ("",), (0,), "xy"):
        add("policy.stimulus_alphabet", lambda domain=domain: m.enumerate_policies(domain, ("0",)))
    for name, domain, response in [("", d, ("0", "1")), ("p", d, ("0",)), ("p", d, ("0", True)),
                                   ("p", list(d), ("0", "1")), ("p", d, ["0", "1"])]:
        add("policy.constructor_totality", lambda name=name, domain=domain, response=response: m.DeterministicPolicy(name, domain, response))
    vs = m.version_space(d, ("0", "1"), (p,), ())
    for name, method in (("response", p.response), ("possible_actions", vs.possible_actions),
                         ("status", vs.status), ("unanimous", vs.unanimous)):
        add(f"policy.out_of_range.{name}", lambda method=method: method("outside"))
    for name, call in tests:
        rejected(call, name)
    once = m.version_space(d, ("0", "1"), (p,), (("x", "0"),))
    check(m.version_space(d, ("0", "1"), (p,), (("x", "0"),) * 5), once, "policy.repeat_idempotent")
    check(len(m.enumerate_policies((), ("0", "1"))), 1, "policy.empty_domain_unique_table")
    COUNTS["invalid_input_cases"] = len(tests)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=Path, default=ROOT / "model.py")
    parser.add_argument("--group", choices=("all", "probes"), default="all")
    args = parser.parse_args()
    try:
        model = load_model(args.model_path)
        probes(model)
        if args.group == "all":
            relations(model)
            bags(model)
            policies(model)
            invalid_inputs(model)
    except AuditFailure as error:
        print(json.dumps({"status": "semantic_failure", "failure": str(error)}, sort_keys=True))
        return 2
    except Exception as error:
        print(json.dumps({"status": "framework_error", "type": type(error).__name__, "failure": str(error)}, sort_keys=True))
        return 3
    print(json.dumps({"status": "passed", "counts": COUNTS}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
