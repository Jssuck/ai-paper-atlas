#!/usr/bin/env python3
"""Independent set-and-orbit audit. Imports no reproduction implementation.

Run from the reproduction directory:
    python3 review/independent_oracle.py

The historical fixture was separately checked against the page images. The
published JSON is an object under test, never a source of expected answers.
"""
from __future__ import annotations

import copy
import hashlib
import itertools as it
import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAMES = "ABC"
KINDS = "AEIO"
LABELS = ("I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII XVIII XIX XX").split()
# Three-character codes: quantifier/mood, subject, predicate.
SOURCE_ROWS = (
    "AAB ACA ACB", "AAB ICA ICB", "AAB ECB ECA", "AAB EBC ECA",
    "AAB OCB OCA", "AAB ABC ICA", "EAB ACA ECB", "EAB ACB ECA",
    "EAB ICA OCB", "EAB IAC OCB", "EAB ICB OCA", "EAB IBC OCA",
    "IAB AAC ICB", "IAB ABC ICA", "OAB AAC OCB", "OAB ACB OAB",
    "AAB IAC ICB", "EAB AAC OCB", "EAB ABC OCA", "AAB AAC ICB",
)
PRINTED = dict(zip(LABELS, (tuple(row.split()) for row in SOURCE_ROWS)))
REPAIRED = dict(PRINTED, XVI=("OAB", "ACB", "OAC"))
ASSUMPTIONS = tuple(tuple(c) for n in range(4) for c in it.combinations(NAMES, n))
REGIMES = {"term_empty_permitted": (), "all_three_terms_nonempty": tuple(NAMES)}

# Generate membership vectors first, then independently enumerate all nonempty
# subsets using combinations. No production masks/model constructors are used.
VECTORS = {a + 2*b + 4*c: (a, b, c) for a, b, c in it.product((0, 1), repeat=3)}
MODELS = []
for size in range(1, 9):
    for points in it.combinations(range(8), size):
        sets = {name: frozenset(p for p in points if VECTORS[p][j])
                for j, name in enumerate(NAMES)}
        MODELS.append((points, sets))
MODELS.sort(key=lambda m: (len(m[0]), sum(2**p for p in m[0])))


def holds(code, sets):
    kind, subject, predicate = code
    left, right = sets[subject], sets[predicate]
    if kind == "A":
        return left.issubset(right)
    if kind == "E":
        return left.isdisjoint(right)
    if kind == "I":
        return not left.isdisjoint(right)
    if kind == "O":
        return bool(left.difference(right))
    raise ValueError(code)


def encode(row):
    return row[0] + "," + row[1] + "=>" + row[2]


@lru_cache(None)
def inspect(row, required=()):
    eligible = [(p, s) for p, s in MODELS if all(s[n] for n in required)]
    premises = [(p, s) for p, s in eligible if holds(row[0], s) and holds(row[1], s)]
    failures = [(p, s) for p, s in premises if not holds(row[2], s)]
    witness = None
    if failures:
        points, sets = failures[0]
        witness = {
            "occupancy": sum(2**p for p in points),
            "occupied_atoms": list(points),
            "universe_size": len(points),
            "universe": [f"x{p}" for p in points],
            "sets": {n: [f"x{p}" for p in sorted(sets[n])] for n in NAMES},
            "premises_true": [True, True], "conclusion_true": False,
        }
    return {"valid": not failures, "models_checked": len(eligible),
            "premise_satisfying_models": len(premises),
            "counterexample_count": len(failures), "minimal_counterexample": witness}


def minima(row):
    sufficient = [s for s in ASSUMPTIONS if inspect(row, s)["valid"]]
    return [list(s) for s in sufficient if not any(set(t) < set(s) for t in sufficient)]


@lru_cache(None)
def orbit_key(row, ei=True):
    # Explicitly enumerate every allowed E/I orientation and both premise
    # orders, rather than invoking the implementation's local normalization.
    alternatives = [((p, p[0] + p[2] + p[1]) if ei and p[0] in "EI" else (p,)) for p in row]
    orbit = set()
    for oriented in it.product(*alternatives):
        for perm in it.permutations(NAMES):
            rename = dict(zip(NAMES, perm))
            renamed = tuple(p[0] + rename[p[1]] + rename[p[2]] for p in oriented)
            orbit.add(encode(renamed))
            orbit.add(encode((renamed[1], renamed[0], renamed[2])))
    return min(orbit)


def grouping(named, ei=True):
    groups = {}
    for label, row in named:
        groups.setdefault(orbit_key(row, ei), []).append(label)
    return [{"canonical_key": key, "members": labels} for key, labels in sorted(groups.items())]


def standard():
    # Define conventional figures first in their usual S/P/M names, then map
    # to the release's A/B/C names. This does not use its candidate generator.
    pairs = (("MP", "SM"), ("PM", "SM"), ("MP", "MS"), ("PM", "MS"))
    mapping = str.maketrans({"M": "A", "P": "B", "S": "C"})
    rows = []
    for figure, (major, minor) in enumerate(pairs, 1):
        for moods in it.product(KINDS, repeat=3):
            row = tuple(q + pair.translate(mapping) for q, pair in zip(moods, (major, minor, "SP")))
            rows.append(("".join(moods) + f"-{figure}", row))
    return rows


def larger():
    # Build all ordered pairs independently and require each unordered pair
    # to occur once. The first premise's ordered pair is fixed as AB.
    pairs = tuple("".join(p) for p in it.permutations(NAMES, 2))
    rows = []
    for pair2, pair3 in it.product(pairs, repeat=2):
        if len({frozenset("AB"), frozenset(pair2), frozenset(pair3)}) != 3:
            continue
        for q1, q2, q3 in it.product(KINDS, repeat=3):
            row = (q1 + "AB", q2 + pair2, q3 + pair3)
            rows.append((encode(row), row))
    return rows


def census(named):
    recap = {orbit_key(r) for r in REPAIRED.values()}
    data = {"candidates": len(named), "regimes": {}}
    for regime, required in REGIMES.items():
        valid = [(label, r) for label, r in named if inspect(r, required)["valid"]]
        groups = grouping(valid)
        uncovered = [g for g in groups if g["canonical_key"] not in recap]
        data["regimes"][regime] = {
            "valid_count": len(valid), "valid_ids": [label for label, _ in valid],
            "valid_structural_class_count": len(groups), "valid_structural_classes": groups,
            "recap_covered_valid_class_count": len(groups) - len(uncovered),
            "recap_uncovered_valid_classes": uncovered,
        }
    return data


CHECKS = 0


def same(actual, expected, where):
    global CHECKS
    CHECKS += 1
    if actual != expected:
        raise AssertionError(f"{where}: actual {actual!r}; expected {expected!r}")


def verify_report(report):
    same(report["semantics"]["model_count"], len(MODELS), "model count")
    for name, required in REGIMES.items():
        same(report["semantics"]["regimes"][name]["model_count"],
             sum(all(sets[t] for t in required) for _, sets in MODELS), f"models: {name}")
    for version, fixture in (("printed", PRINTED), ("repaired", REPAIRED)):
        forms = report[version + "_forms"]
        same([f["label"] for f in forms], LABELS, version + " labels/order")
        for item, (label, row) in zip(forms, fixture.items()):
            name = f"{version}/{label}"
            same(item["code"], encode(row), name + " transcription")
            same(item["premises"], list(row[:2]), name + " premise data")
            same(item["conclusion"], row[2], name + " conclusion data")
            same(item["structural_class"], orbit_key(row), name + " orbit")
            same(item["syntactic_class_without_ei_conversion"], orbit_key(row, False), name + " narrow orbit")
            same(item["minimal_nonempty_assumptions"], minima(row), name + " existence minima")
            expected = [{"required_terms": list(s), **inspect(row, s)} for s in ASSUMPTIONS]
            same(item["all_nonempty_assumption_checks"], expected, name + " all 8 checks/witnesses")
            for regime, required in REGIMES.items():
                same(item["regimes"][regime], inspect(row, required), name + "/" + regime)
        groups = grouping(fixture.items())
        same(report["structural_equivalence"][version + "_class_count"], len(groups), version + " class count")
        same(report["structural_equivalence"][version + "_classes"], groups, version + " exact classes")
        narrow = grouping(fixture.items(), False)
        same(report["syntactic_equivalence_without_ei_conversion"][version + "_class_count"], len(narrow), version + " narrow count")
        same(report["syntactic_equivalence_without_ei_conversion"][version + "_classes"], narrow, version + " narrow groups")
    all_rows = larger()
    scopes = {"standard_256": standard(), "euler_style_512": all_rows,
              "particular_first_256": [(n, r) for n, r in all_rows if r[0][0] in "IO"]}
    for scope, expected in scopes.items():
        data = report[scope]
        same(data["candidate_count"], len(expected), scope + " candidate count")
        cases = {item["id"]: item for item in data["cases"]}
        same(len(cases), len(data["cases"]), scope + " no duplicate ids")
        same(set(cases), {n for n, _ in expected}, scope + " complete candidate identity set")
        same(data["candidate_identifiers_unique"], True, scope + " id uniqueness flag")
        same(data["candidate_codes_unique"], True, scope + " code uniqueness flag")
        same(data["all_candidate_structural_class_count"], len({orbit_key(r) for _, r in expected}), scope + " all classes")
        for label, row in expected:
            item = cases[label]
            same(item["code"], encode(row), scope + "/" + label + " code")
            same(item["premises"], list(row[:2]), scope + "/" + label + " premises")
            same(item["conclusion"], row[2], scope + "/" + label + " conclusion")
            same(item["canonical_key"], orbit_key(row), scope + "/" + label + " orbit")
            same(item["canonical_key_without_ei_conversion"], orbit_key(row, False), scope + "/" + label + " narrow orbit")
            same(item["equivalent_repaired_recap_entries"],
                 [n for n, r in REPAIRED.items() if orbit_key(r) == orbit_key(row)], scope + "/" + label + " recap mapping")
            for regime, required in REGIMES.items():
                same(item["regime_validity"][regime], inspect(row, required)["valid"], scope + "/" + label + "/" + regime)
        computed = census(expected)
        for regime in REGIMES:
            for key, value in computed["regimes"][regime].items():
                actual = data["regimes"][regime][key]
                # Generator order is not a semantic assertion. Compare exact
                # members/identifiers as sets but retain class keys and counts.
                if key == "valid_ids":
                    actual, value = sorted(actual), sorted(value)
                elif key.endswith("classes"):
                    actual = [{**g, "members": sorted(g["members"])} for g in actual]
                    value = [{**g, "members": sorted(g["members"])} for g in value]
                same(actual, value, scope + "/" + regime + "/" + key)
            valid = [(n, r) for n, r in expected if inspect(r, REGIMES[regime])["valid"]]
            groups = grouping(valid, False)
            recap = {orbit_key(r, False) for r in REPAIRED.values()}
            uncovered = [g for g in groups if g["canonical_key"] not in recap]
            narrow = {"valid_class_count": len(groups), "valid_classes": groups,
                      "recap_covered_valid_class_count": len(groups)-len(uncovered),
                      "recap_uncovered_valid_classes": uncovered,
                      "recap_covered_valid_candidate_count": sum(orbit_key(r, False) in recap for _, r in valid)}
            for key, value in narrow.items():
                actual = data["regimes"][regime]["without_ei_conversion"][key]
                if key.endswith("classes"):
                    actual = [{**g, "members": sorted(g["members"])} for g in actual]
                    value = [{**g, "members": sorted(g["members"])} for g in value]
                same(actual, value, scope + "/" + regime + "/narrow/" + key)
    same(report["historical_scope"]["printed_xvi"], encode(PRINTED["XVI"]), "printed XVI metadata")
    same(report["historical_scope"]["teaching_repair_xvi"], encode(REPAIRED["XVI"]), "repaired XVI metadata")
    same(report["euler_style_512"]["printed_xvi_in_scope"], False, "printed XVI scope")
    same(report["euler_style_512"]["all_repaired_entries_in_scope"], True, "repaired scope")


def main():
    report = json.loads((ROOT / "outputs/report.json").read_text(encoding="utf-8"))
    verify_report(report)
    checks = CHECKS
    rows = standard()
    direct_keys = {orbit_key(r, False) for r in REPAIRED.values()}
    valid_all = [(n, r) for n, r in rows if inspect(r, tuple(NAMES))["valid"]]
    missing = [n for n, r in valid_all if orbit_key(r, False) not in direct_keys]
    same(missing, ["AAI-1", "EAO-1", "AEO-2", "EAO-2", "AEO-4"], "direct table coverage missing five")
    same(len({orbit_key(r, False) for r in PRINTED.values()}), 20, "printed narrow count")
    same(len(direct_keys), 19, "repaired narrow count")
    same([g["members"] for g in grouping(REPAIRED.items(), False) if len(g["members"]) > 1],
         [["V", "XVI"]], "only narrow merger")
    same({n: minima(r) for n, r in REPAIRED.items() if not inspect(r)["valid"]},
         {"VI": [["A"]], "XVIII": [["A"]], "XIX": [["B"]], "XX": [["A"]]}, "four existence minima")
    # Deliberate corrupted reports must be rejected. This checks that the
    # independent comparison does not merely print expected totals.
    negative_controls = []
    for name, change in (
        ("extra_model", lambda r: r["semantics"].__setitem__("model_count", 256)),
        ("silently_repaired_source", lambda r: r["printed_forms"][15].__setitem__("code", "OAB,ACB=>OAC")),
        ("wrong_existence_minimum", lambda r: r["repaired_forms"][5].__setitem__("minimal_nonempty_assumptions", [["B"]])),
        ("missing_candidate", lambda r: r["standard_256"]["cases"].pop()),
        ("wrong_witness", lambda r: r["repaired_forms"][5]["all_nonempty_assumption_checks"][0]["minimal_counterexample"].__setitem__("universe_size", 2)),
        ("wrong_narrow_count", lambda r: r["syntactic_equivalence_without_ei_conversion"].__setitem__("repaired_class_count", 9)),
    ):
        corrupted = copy.deepcopy(report)
        change(corrupted)
        try:
            verify_report(corrupted)
        except AssertionError:
            negative_controls.append({"mutation": name, "rejected": True})
        else:
            raise AssertionError("Undetected negative control: " + name)
    result = {
        "status": "PASS", "method": "Independent combinations of membership vectors, set semantics, explicit transformation orbits; imports no implementation functions.",
        "report_field_comparisons": checks,
        "models": len(MODELS),
        "models_all_terms_nonempty": sum(all(s.values()) for _, s in MODELS),
        "model_counts_by_required_terms": {"".join(q) or "none": sum(all(s[n] for n in q) for _, s in MODELS) for q in ASSUMPTIONS},
        "recap": {version: {"entries": len(fixture),
            "valid_empty_allowed": sum(inspect(r)["valid"] for r in fixture.values()),
            "valid_all_nonempty": sum(inspect(r, tuple(NAMES))["valid"] for r in fixture.values()),
            "classes_without_ei_symmetry": grouping(fixture.items(), False),
            "classes_with_ei_symmetry": grouping(fixture.items()),
            "forms": [{"id": n, "formulas": list(r), "minimal_nonempty_assumptions": minima(r),
                       "regimes": {k: inspect(r, v) for k, v in REGIMES.items()}} for n, r in fixture.items()]}
            for version, fixture in (("printed", PRINTED), ("repaired", REPAIRED))},
        "standard_256": census(rows), "euler_style_512": census(larger()),
        "particular_first_256": census([(n, r) for n, r in larger() if r[0][0] in "IO"]),
        "direct_standard_coverage": {"comparison": "Global term renaming plus premise swap; E/I exchange excluded.",
            "all_nonempty_valid": len(valid_all), "covered": len(valid_all)-len(missing), "missing": missing,
            "repaired_recap_to_standard": {label: [n for n, r in rows if orbit_key(r, False) == orbit_key(row, False)]
                                           for label, row in REPAIRED.items()}},
        "negative_controls": negative_controls,
        "sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in
                   ("euler_civ.py", "report.py", "tests/test_euler_civ.py", "outputs/report.json", "review/independent_oracle.py")},
    }
    destination = ROOT / "review/independent-results.json"
    destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS: {checks} exact report-field comparisons; 255 models, 218 all-nonempty.")
    print("Printed/repaired: 16/20 valid with empty terms; 20/20 all-nonempty.")
    print("Narrow classes: 20 printed, 19 repaired. With E/I exchange: 10 printed, 9 repaired.")
    print("Standard: 15/24 valid; direct table covers 19/24; five missing: " + ", ".join(missing))
    print("Six deliberate report mutations were all rejected.")
    print("Results: review/independent-results.json")


if __name__ == "__main__":
    main()
