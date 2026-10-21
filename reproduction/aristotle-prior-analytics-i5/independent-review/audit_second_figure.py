#!/usr/bin/env python3
"""Independent, deterministic audit; standard library only, no bare asserts.

Run from the reproduction root. Does not import the author's tests or use
production constants, policy filters, truth evaluator, or support decoder as an
oracle. Mutation copies exist only in memory; production files are never edited.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
from itertools import combinations, product
import json
import os
from pathlib import Path
import platform
import sys
import tempfile
import types

ROOT = Path(__file__).resolve().parents[1]
Q = tuple("AEIO")
TERMS = ("P", "M", "S")
POLICIES = ("allow-empty", "all-nonempty", "subject-nonempty")
# A literal truth-table basis, not production's integer bit decoder.
TYPES = ((False, False, False), (False, False, True),
         (False, True, False), (False, True, True),
         (True, False, False), (True, False, True),
         (True, True, False), (True, True, True))
MOODS = tuple("".join(x) for x in product(Q, repeat=3))
CLAUSES = tuple(product(Q, TERMS, TERMS))


class CheckFailure(Exception):
    pass


def check(condition, context):
    if not condition:
        raise CheckFailure(str(context))


def equal(actual, expected, context):
    check(actual == expected, f"{context}: actual={actual!r}, expected={expected!r}")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def truth(q, subject, predicate):
    """Set algebra only: no production call and no production constants."""
    outside = subject.difference(predicate)
    common = subject.intersection(predicate)
    return {"A": len(outside) == 0, "E": len(common) == 0,
            "I": len(common) > 0, "O": len(outside) > 0}[q]


def policy_ok(terms, policy):
    if policy == "allow-empty":
        return True
    if policy == "all-nonempty":
        return bool(terms["P"]) and bool(terms["M"]) and bool(terms["S"])
    if policy == "subject-nonempty":
        return bool(terms["S"])
    raise CheckFailure(f"unknown oracle policy {policy}")


def code_of(membership):
    # Boundary encoding only; semantic evaluations operate on tuple elements.
    return 4 * membership[0] + 2 * membership[1] + membership[2]


@dataclass(frozen=True)
class Model:
    types: tuple
    support: int
    terms: dict

    @property
    def size(self):
        return len(self.types)


# Generate supports by nonempty combinations, rather than scanning integer masks.
MODELS = []
for n in range(1, 9):
    for occupied in combinations(TYPES, n):
        MODELS.append(Model(occupied, sum(2 ** code_of(t) for t in occupied),
                            {name: frozenset(t for t in occupied if t[column])
                             for column, name in enumerate(TERMS)}))
MODELS.sort(key=lambda m: (m.size, m.support))
ELIGIBLE = {p: [m for m in MODELS if policy_ok(m.terms, p)] for p in POLICIES}


def clause_truth(clause, model):
    q, subject, predicate = clause
    return truth(q, model.terms[subject], model.terms[predicate])


def oracle_entailment(premises, conclusion, policy):
    premise_models = [m for m in ELIGIBLE[policy]
                      if all(clause_truth(c, m) for c in premises)]
    witnesses = [m for m in premise_models if not clause_truth(conclusion, m)]
    return premise_models, witnesses


def production_module(source=None, name="reviewed_second_figure"):
    module = types.ModuleType(name)
    module.__file__ = "second_figure.py"  # public, relative diagnostic path
    sys.modules[name] = module
    if source is None:
        source = (ROOT / "second_figure.py").read_text(encoding="utf-8")
    exec(compile(source, "second_figure.py", "exec", optimize=sys.flags.optimize), module.__dict__)
    return module


def validate_concrete(model, support, expected_size, context):
    equal(set(model), {"universe", "P", "M", "S"}, context + " concrete keys")
    u = set(model["universe"])
    equal(len(u), len(model["universe"]), context + " unique universe")
    equal(len(u), expected_size, context + " universe size")
    check(bool(u), context + " nonempty universe")
    terms = {t: set(model[t]) for t in TERMS}
    for t in TERMS:
        equal(len(model[t]), len(terms[t]), context + " no repeated extension labels")
        check(terms[t] <= u, context + " extension subset")
    memberships = {tuple(obj in terms[t] for t in TERMS) for obj in u}
    encoded = sum(2 ** code_of(t) for t in memberships)
    equal(encoded, support, context + " independent encoding")
    equal(len(memberships), len(u), context + " one object per occupied type")
    return terms


def semantic_checks(sf):
    count = 0
    for m in MODELS:
        equal(sf.occupied_atoms(m.support), tuple(sorted(code_of(t) for t in m.types)),
              f"occupied atoms {m.support}")
        for t in TERMS:
            equal(sf.extension(m.support, t), frozenset(code_of(x) for x in m.terms[t]),
                  f"extension {m.support} {t}")
        for clause in CLAUSES:
            expected = clause_truth(clause, m)
            equal(sf.holds(m.support, *clause), expected, f"atom truth {m.support} {clause}")
            q, x, y = clause
            equal(sf.evaluate_categorical(q, m.terms[x], m.terms[y]), expected,
                  f"direct evaluator {m.support} {clause}")
            count += 1
    policy_count = 0
    for p in POLICIES:
        expected = [m.support for m in ELIGIBLE[p]]
        equal(list(sf.iter_supports(p)), expected, f"complete minimum-size ordering {p}")
        for m in MODELS:
            equal(sf.satisfies_policy(m.support, p), policy_ok(m.terms, p),
                  f"policy membership {p} {m.support}")
            policy_count += 1
    equal([len(ELIGIBLE[p]) for p in POLICIES], [255, 218, 240], "oracle policy counts")
    equal(count, 9180, "atomic comparison count")
    equal(policy_count, 765, "policy comparison count")
    return {"atomic_cases": count, "truth_function_comparisons": count * 2,
            "policy_membership_cases": policy_count, "occupied_support_cases": len(MODELS),
            "extension_cases": len(MODELS) * 3}


def compare_result(result, premises, conclusion, policy, context):
    premise_models, witnesses = oracle_entailment(premises, conclusion, policy)
    equal(result.valid, not witnesses, context + " validity")
    equal(result.vacuous, not premise_models, context + " vacuity")
    equal(result.eligible_support_count, len(ELIGIBLE[policy]), context + " eligible count")
    equal(result.premise_support_count, len(premise_models), context + " premise count")
    equal(result.policy.value, policy, context + " policy")
    equal([(c.quantifier, c.subject, c.predicate) for c in result.premises], list(premises),
          context + " premise identities")
    equal((result.conclusion.quantifier, result.conclusion.subject, result.conclusion.predicate),
          conclusion, context + " conclusion identity")
    expected_mask = witnesses[0].support if witnesses else None
    equal(result.countermodel_support, expected_mask, context + " minimum cardinality and numeric tie-break")
    record = result.as_dict()
    for key, expected in (("valid", not witnesses), ("vacuous", not premise_models),
                          ("eligible_support_count", len(ELIGIBLE[policy])),
                          ("premise_support_count", len(premise_models)),
                          ("countermodel_support", expected_mask)):
        equal(record[key], expected, context + " serialized " + key)
    if witnesses:
        best = witnesses[0]
        equal(record["countermodel_size"], best.size, context + " serialized size")
        equal(record["countermodel_atoms"], sorted(code_of(t) for t in best.types),
              context + " serialized atoms")
        terms = validate_concrete(record["countermodel"], expected_mask, best.size, context)
        check(policy_ok(terms, policy), context + " concrete policy")
        for q, x, y in premises:
            check(truth(q, terms[x], terms[y]), context + " concrete premise")
        q, x, y = conclusion
        check(not truth(q, terms[x], terms[y]), context + " concrete conclusion false")
        # Exhaustive witnesses establish size minimality independently, not just
        # the production iterator's ordering or an assumed size bound.
        check(all(best.size <= m.size for m in witnesses), context + " global support minimality")
    else:
        for key in ("countermodel_size", "countermodel_atoms", "countermodel"):
            equal(record[key], None, context + " absent witness " + key)
    return record, witnesses


def classification_checks(sf):
    equal(sf.all_moods(), MOODS, "64 distinct, correctly ordered moods")
    rows, totals, sizes = {}, {}, {}
    for p in POLICIES:
        valid = []
        rows[p] = {}
        sizes[p] = Counter()
        for mood in MOODS:
            q, r, t = mood
            premises = ((q, "P", "M"), (r, "S", "M"))
            conclusion = (t, "S", "P")
            result = sf.classify_mood(mood, p)
            record, witnesses = compare_result(result, premises, conclusion, p, f"{p} {mood}")
            rows[p][mood] = record
            if witnesses:
                sizes[p][witnesses[0].size] += 1
            else:
                valid.append(mood)
        totals[p] = {"supports": len(ELIGIBLE[p]), "valid_moods": valid,
                     "valid_count": len(valid), "invalid_count": 64 - len(valid),
                     "minimum_countermodel_size_histogram": dict(sorted(sizes[p].items())),
                     "premise_support_counts": {q+r: rows[p][q+r+"A"]["premise_support_count"]
                                                for q, r in product(Q, repeat=2)}}
    expected = {"allow-empty": ["AEE", "AOO", "EAE", "EIO"],
                "all-nonempty": ["AEE", "AEO", "AOO", "EAE", "EAO", "EIO"],
                "subject-nonempty": ["AEE", "AEO", "AOO", "EAE", "EAO", "EIO"]}
    for p in POLICIES:
        equal(totals[p]["valid_moods"], expected[p], f"independently found valid moods {p}")
    return {"classifications": 192, "concrete_countermodels_and_minimality_checks":
            sum(x["invalid_count"] for x in totals.values()), "policies": totals}, rows


def direction_checks(sf):
    rows = []
    examples = [((("I", "P", "M"), ("E", "S", "M")), ("O", "P", "S"), True, "IE reverse"),
                ((("I", "P", "M"), ("E", "S", "M")), ("O", "S", "P"), False, "IE forward"),
                ((("E", "P", "M"), ("I", "S", "M")), ("O", "S", "P"), True, "EI forward"),
                ((("E", "P", "M"), ("I", "S", "M")), ("O", "P", "S"), False, "EI reverse"),
                ((("O", "P", "S"),), ("O", "S", "P"), False, "O nonconversion"),
                ((("A", "P", "M"), ("O", "P", "M")), ("I", "S", "P"), True, "vacuity"),
                ((), ("A", "P", "P"), True, "empty premises tautology")]
    for p in POLICIES:
        for premises, conclusion, valid, label in examples:
            result = sf.classify(tuple(sf.Clause(*c) for c in premises), sf.Clause(*conclusion), p)
            record, witnesses = compare_result(result, premises, conclusion, p, f"{p} {label}")
            equal(result.valid, valid, f"{p} {label} expected validity")
            rows.append({"policy": p, "case": label, "valid": result.valid,
                         "countermodel_support": record["countermodel_support"],
                         "countermodel_size": record["countermodel_size"]})
    return {"direction_and_general_entailment_cases": len(rows), "results": rows}


def compression_checks(sf):
    checked = 0
    for n in (1, 2, 3, 4):
        universe = tuple(f"object-{i}" for i in range(n))
        for memberships in product(TYPES, repeat=n):
            terms = {name: {universe[i] for i, t in enumerate(memberships) if t[column]}
                     for column, name in enumerate(TERMS)}
            expected_support = sum(2 ** code_of(t) for t in set(memberships))
            actual_support = sf.compress_model(universe, **terms)
            equal(actual_support, expected_support, "labeled finite model compression")
            # Compare all sentences before/after compression without calling the
            # production semantics. Includes duplicate types and outside objects.
            realized = sf.concrete_model(actual_support)
            out = validate_concrete(realized, expected_support, len(set(memberships)), "compression")
            for q, x, y in CLAUSES:
                equal(truth(q, terms[x], terms[y]), truth(q, out[x], out[y]),
                      "compression truth preservation")
            for p in POLICIES:
                equal(policy_ok(terms, p), policy_ok(out, p), "compression existence preservation")
            checked += 1
    equal(checked, 4680, "labeled models count")
    return {"labeled_models_sizes_one_through_four": checked,
            "compression_truth_preservation_cases": checked * len(CLAUSES),
            "compression_policy_preservation_cases": checked * len(POLICIES)}


def invalid_input_checks(sf):
    cases = []
    def add(label, fn, error):
        cases.append((label, fn, error))
    for value in (0, -1, 256, 2**100):
        for name, fn in (("occupied_atoms", lambda v=value: sf.occupied_atoms(v)),
                         ("extension", lambda v=value: sf.extension(v, "P")),
                         ("holds", lambda v=value: sf.holds(v, "A", "P", "M")),
                         ("concrete_model", lambda v=value: sf.concrete_model(v)),
                         ("satisfies_policy", lambda v=value: sf.satisfies_policy(v, "allow-empty"))):
            add(name + " range", fn, ValueError)
    for value in (True, False, 1.0, "1", None, [], {}):
        for name, fn in (("occupied_atoms", lambda v=value: sf.occupied_atoms(v)),
                         ("extension", lambda v=value: sf.extension(v, "P")),
                         ("holds", lambda v=value: sf.holds(v, "A", "P", "M")),
                         ("concrete_model", lambda v=value: sf.concrete_model(v)),
                         ("satisfies_policy", lambda v=value: sf.satisfies_policy(v, "allow-empty"))):
            add(name + " type", fn, TypeError)
    for value in ("", "a", "AA", "X", " A", "A ", None, 1, True, []):
        error = ValueError if isinstance(value, str) else TypeError
        add("quantifier holds", lambda v=value: sf.holds(1, v, "P", "M"), error)
        add("quantifier set", lambda v=value: sf.evaluate_categorical(v, [], []), error)
        add("quantifier Clause", lambda v=value: sf.Clause(v, "P", "M"), error)
    for value in ("", "p", "X", " P", None, 1, True, []):
        error = ValueError if isinstance(value, str) else TypeError
        add("term extension", lambda v=value: sf.extension(1, v), error)
        add("subject holds", lambda v=value: sf.holds(1, "A", v, "M"), error)
        add("predicate holds", lambda v=value: sf.holds(1, "A", "P", v), error)
        add("subject Clause", lambda v=value: sf.Clause("A", v, "M"), error)
        add("predicate Clause", lambda v=value: sf.Clause("A", "P", v), error)
    for value in ("", "ALLOW_EMPTY", "nonempty", "S-nonempty", None, 1, True, []):
        error = ValueError if isinstance(value, str) else TypeError
        add("policy iterator", lambda v=value: list(sf.iter_supports(v)), error)
        add("policy membership", lambda v=value: sf.satisfies_policy(1, v), error)
        add("policy classify", lambda v=value: sf.classify([], sf.Clause("A", "P", "P"), v), error)
        add("policy mood", lambda v=value: sf.classify_mood("EAE", v), error)
    for value in ("", "AE", "AEEE", "eae", "AXO", "E A", None, 123, True, ["E", "A", "E"]):
        error = ValueError if isinstance(value, str) else TypeError
        add("mood", lambda v=value: sf.classify_mood(v), error)
    for value in (None, 1, "A(P,M)", ["A(P,M)"], [None]):
        add("premises", lambda v=value: sf.classify(v, sf.Clause("A", "P", "P")), TypeError)
    for value in (None, 1, "A(P,M)", []):
        add("conclusion", lambda v=value: sf.classify([], v), TypeError)
    for args, error in ((([], [], [], []), ValueError), (([1], [2], [], []), ValueError),
                        (([1], [], [2], []), ValueError), (([1], [], [], [2]), ValueError),
                        (([[1]], [], [], []), TypeError), (([1], [[1]], [], []), TypeError),
                        ((None, [], [], []), TypeError)):
        add("model compression", lambda a=args: sf.compress_model(*a), error)
    for args in (("A", None, []), ("E", [], None), ("I", [[1]], []), ("O", [], [[1]])):
        add("set evaluator iterable/hashability", lambda a=args: sf.evaluate_categorical(*a), TypeError)
    for label, fn, error in cases:
        try:
            fn()
        except error:
            pass
        except Exception as exc:
            raise CheckFailure(f"{label}: expected {error.__name__}, got {type(exc).__name__}") from exc
        else:
            raise CheckFailure(f"{label}: did not reject invalid input with {error.__name__}")
    return {"invalid_input_calls": len(cases), "expected_exception_counts":
            dict(Counter(error.__name__ for _, _, error in cases))}


def report_checks(sf, rows):
    saved = json.loads((ROOT / "report.json").read_text(encoding="utf-8"))
    generated = sf.make_report()
    equal(saved, generated, "saved report is current")
    equal((ROOT / "REPORT.md").read_text(encoding="utf-8"), sf.render_markdown(generated),
          "saved Markdown is current")
    equal(set(saved["policies"]), set(POLICIES), "report policies")
    for p in POLICIES:
        equal(saved["policies"][p]["results"], rows[p], f"report all checked rows {p}")
        equal(saved["policies"][p]["support_count"], len(ELIGIBLE[p]), f"report support count {p}")
        equal(saved["policies"][p]["valid_moods"], [m for m in MOODS if rows[p][m]["valid"]],
              f"report valid list {p}")
    reversal_rows = 0
    for p in POLICIES:
        premises = (("I", "P", "M"), ("E", "S", "M"))
        for key, conclusion in (("forward_O_S_P", ("O", "S", "P")),
                                ("reverse_O_P_S", ("O", "P", "S"))):
            result = sf.classify(tuple(sf.Clause(*c) for c in premises), sf.Clause(*conclusion), p)
            checked_record, _ = compare_result(result, premises, conclusion, p, "saved reversal")
            equal(saved["reversal_check_IE"][p][key], checked_record, "saved IE reversal direction")
            reversal_rows += 1
    markdown_rows = 0
    policy = None
    for line in (ROOT / "REPORT.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("## ") and line[3:] in POLICIES:
            policy = line[3:]
        if not line.startswith("| "):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if not cells or cells[0] not in {a+b for a, b in product(Q, repeat=2)}:
            continue
        check(policy is not None, "Markdown policy section")
        pair = cells[0]
        expected = []
        for q in Q:
            row = rows[policy][pair+q]
            if row["valid"]:
                expected.append("V")
            else:
                atoms = ",".join(str(a) for a in row["countermodel_atoms"])
                expected.append(f"× {row['countermodel_size']} [{atoms}]")
        expected.append(str(rows[policy][pair+"A"]["premise_support_count"]))
        equal(cells[1:], expected, f"Markdown cells {policy} {pair}")
        markdown_rows += 1
    equal(markdown_rows, 48, "all Markdown data rows")
    with tempfile.TemporaryDirectory(prefix="second-figure-audit-") as tmp:
        jp, mp = Path(tmp) / "report.json", Path(tmp) / "REPORT.md"
        equal(sf.main(["--json", str(jp), "--markdown", str(mp)]), 0, "CLI function exit")
        equal(jp.read_bytes(), (ROOT / "report.json").read_bytes(), "CLI JSON bytes")
        equal(mp.read_bytes(), (ROOT / "REPORT.md").read_bytes(), "CLI Markdown bytes")
    return {"published_json_mood_rows_checked": 192, "published_json_reversal_rows_checked": reversal_rows,
            "published_markdown_rows_checked": markdown_rows, "generated_artifact_byte_checks": 2}


MUTATIONS = (
    ("O_converted_to_I", '    return outside\n', '    return both\n', "semantics"),
    ("E_mistakenly_same_as_I", '        return not both\n', '        return both\n', "semantics"),
    ("A_given_existential_import", '        return not outside\n',
     '        return not outside and any(atom & x_bit for atom in atoms)\n', "semantics"),
    ("S_policy_checks_P", 'Policy.SUBJECT_NONEMPTY: ("S",),',
     'Policy.SUBJECT_NONEMPTY: ("P",),', "semantics"),
    ("all_nonempty_policy_ignored", 'Policy.ALL_NONEMPTY: TERMS,',
     'Policy.ALL_NONEMPTY: (),', "semantics"),
    ("numeric_not_cardinality_order", 'key=lambda mask: (mask.bit_count(), mask)',
     'key=lambda mask: mask', "classification"),
    ("second_figure_conclusion_reversed", 'Clause(t, "S", "P"), policy)',
     'Clause(t, "P", "S"), policy)', "classification"),
    ("first_premise_reversed", 'Clause(q, "P", "M")',
     'Clause(q, "M", "P")', "classification"),
    ("last_witness_not_first", 'if witness is None and not conclusion.holds(support):',
     'if not conclusion.holds(support):', "classification"),
    ("premise_count_off_by_one", '    premise_count = 0\n',
     '    premise_count = 1\n', "classification"),
    ("outside_all_atom_dropped", 'range(8) if support & (1 << atom)',
     'range(1, 8) if support & (1 << atom)', "semantics"),
    ("boolean_mask_accepted", 'if type(value) is not int:',
     'if not isinstance(value, int):', "invalid_inputs"),
    ("compression_multiplicity_not_erased", '        mask |= 1 << atom',
     '        mask += 1 << atom', "compression"),
)


def mutation_checks():
    source = (ROOT / "second_figure.py").read_text(encoding="utf-8")
    probes = {"semantics": semantic_checks, "classification": classification_checks,
              "invalid_inputs": invalid_input_checks, "compression": compression_checks}
    results = []
    for index, (name, old, new, probe) in enumerate(MUTATIONS):
        equal(source.count(old), 1, f"mutation anchor {name}")
        mutant = production_module(source.replace(old, new, 1), f"mutant_{index}")
        try:
            probes[probe](mutant)
        except CheckFailure as exc:
            results.append({"name": name, "probe": probe, "outcome": "detected",
                            "evidence": str(exc)})
        except Exception as exc:
            # Crashes are recorded distinctly, not quietly counted as detected.
            raise CheckFailure(f"mutation {name} produced unexpected {type(exc).__name__}: {exc}") from exc
        else:
            raise CheckFailure(f"mutation {name} survived independent checks")
    return {"targeted_variants": len(results), "detected": len(results), "survivors": 0,
            "unexpected_errors": 0, "variants": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    files = ("second_figure.py", "test_second_figure.py", "report.json", "REPORT.md")
    before = {name: sha(ROOT / name) for name in files}
    sf = production_module()
    result = {"status": "PASS", "python": platform.python_version(),
              "implementation": platform.python_implementation(),
              "optimization": sys.flags.optimize, "hash_seed": os.environ.get("PYTHONHASHSEED"),
              "reviewed_sha256": before,
              "audit_script_sha256": sha(Path(__file__)),
              "oracle_basis": "all nonempty combinations of eight literal membership tuples; direct set algebra"}
    result["semantics"] = semantic_checks(sf)
    print("PASS: atomic truth, support enumeration/order and all policy memberships", flush=True)
    result["classification"], rows = classification_checks(sf)
    print("PASS: all 192 classifications, 176 concrete witnesses, full-support minimum size/tie-break", flush=True)
    result["directions"] = direction_checks(sf)
    result["compression"] = compression_checks(sf)
    print("PASS: direction/vacuity cases and all 4,680 labeled models of sizes 1..4", flush=True)
    result["invalid_inputs"] = invalid_input_checks(sf)
    result["reports"] = report_checks(sf, rows)
    result["mutations"] = mutation_checks()
    print("PASS: invalid inputs, saved/generated artifacts, all 13 targeted faulty variants detected", flush=True)
    after = {name: sha(ROOT / name) for name in files}
    equal(after, before, "reviewed files unchanged during audit")
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
