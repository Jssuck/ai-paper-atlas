#!/usr/bin/env python3
"""Separately authored review oracle; standard library, no project enumerators.

Enumerates S and P independently as all subsets of {0,...,n-1}, n=1..5.
Expected truth uses membership counts. Production functions are invoked only as
systems under test, never to obtain the oracle's model space or expected truth.
Run from any directory: python3 path/to/review/independent_oracle.py.
"""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import csv
import hashlib
import json
from pathlib import Path
import platform
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import euler_semantics as sut  # noqa: E402
import run as output_generator  # noqa: E402

FORMS = ("A", "E", "I", "O")
MODES = ("allow_empty_terms", "nonempty_terms")


def independent_models(max_size=5):
    """No use of SUT labeled_models, canonical_model, or representatives."""
    for n in range(1, max_size + 1):
        for s_encoding in range(2 ** n):
            for p_encoding in range(2 ** n):
                memberships = tuple(
                    (bool(s_encoding & 2 ** x), bool(p_encoding & 2 ** x))
                    for x in range(n)
                )
                yield n, memberships


def oracle(memberships):
    # The four counts arise directly from the pair of membership indicators;
    # no production set operations, truth functions, or atom methods are reused.
    counts = Counter(memberships)
    both = counts[(True, True)]
    only_s = counts[(True, False)]
    only_p = counts[(False, True)]
    outside = counts[(False, False)]
    cells = (both, only_s, only_p, outside)
    values = {"A": only_s == 0, "E": both == 0, "I": both > 0, "O": only_s > 0}
    occupancy = sum(2 ** k for k, count in enumerate(cells) if count > 0)
    nonempty_terms = both + only_s > 0 and both + only_p > 0
    return values, occupancy, nonempty_terms, cells


def read_sut_model(model):
    return tuple((x in model.subject, x in model.predicate) for x in sorted(model.universe))


def check(condition, description):
    if not condition:
        raise AssertionError(description)


def main():
    started = datetime.now(timezone.utc).isoformat()
    print(f"started_at_utc={started}")
    print(f"python={sys.version.replace(chr(10), ' ')}")
    print(f"platform={platform.platform()}")
    print("oracle: independently enumerate two subsets, count point memberships; sizes 1..5")
    records = []
    unique = {mode: {} for mode in MODES}
    by_size = Counter()
    nonempty_by_size = Counter()
    for n, memberships in independent_models():
        expected, mask, nonempty, cells = oracle(memberships)
        by_size[n] += 1
        nonempty_by_size[n] += int(nonempty)
        model = sut.Model(set(range(n)), {i for i, (s, p) in enumerate(memberships) if s},
                          {i for i, (s, p) in enumerate(memberships) if p})
        check(model.truth() == expected, f"truth disagreement: n={n}, memberships={memberships}")
        check(model.occupancy() == mask, "occupancy disagreement")
        check(tuple(len(x) for x in model.atoms()) == cells, "atom counts disagreement")
        check(model.admitted(MODES[0]), "nonempty U incorrectly rejected")
        check(model.admitted(MODES[1]) == nonempty, "mode admission disagreement")
        compressed = sut.canonical_model(mask)
        reduced_truth, reduced_mask, reduced_nonempty, reduced_cells = oracle(read_sut_model(compressed))
        check(reduced_truth == expected and reduced_mask == mask and reduced_nonempty == nonempty,
              "canonical compression changed truth or admission")
        check(len(compressed.universe) == sum(c > 0 for c in cells), "compression retained multiplicity")
        records.append((n, expected, mask, nonempty))
        unique[MODES[0]][mask] = expected
        if nonempty:
            unique[MODES[1]][mask] = expected
    check(dict(by_size) == {1: 4, 2: 16, 3: 64, 4: 256, 5: 1024}, "labeled model count")
    check(dict(nonempty_by_size) == {1: 1, 2: 9, 3: 49, 4: 225, 5: 961}, "nonempty model count")
    check(len(records) == 1364 and sum(r[3] for r in records) == 1245, "total labeled count")
    print("PASS: 1364 independently generated labeled models; 1245 have both terms nonempty")
    print("PASS: sizes 1..4 reproduce 340/284; size 5 adds 1024/961, not a disjoint 1364-model sample")

    expected_counts = {MODES[0]: {"A": 7, "E": 7, "I": 8, "O": 8},
                       MODES[1]: {"A": 4, "E": 2, "I": 8, "O": 6}}
    expected_joint = {MODES[0]: {"AE": 3, "AI": 4, "EO": 4, "IO": 4},
                      MODES[1]: {"AI": 4, "EO": 2, "IO": 4}}
    saved = json.loads((ROOT / "results/results.json").read_text(encoding="utf-8"))
    check(output_generator.experiment() == saved, "saved results.json differs from fresh experiment()")
    summaries = {}
    query_checks = 0
    valid_queries = Counter()
    countermodel_size_counts = {mode: Counter() for mode in MODES}
    for mode in MODES:
        space = unique[mode]
        actual = sut.representatives(mode)
        counts = {f: sum(t[f] for t in space.values()) for f in FORMS}
        joint = dict(sorted(Counter("".join(f for f in FORMS if t[f]) for t in space.values()).items()))
        strict_count = sum((mask & 7) == 7 for mask in space)
        check(len(space) == (15 if mode == MODES[0] else 10), "mode pattern total")
        check(counts == expected_counts[mode], "A/E/I/O pattern counts")
        check(joint == expected_joint[mode], "joint truth pattern counts")
        check(strict_count == 2, "strict overlap pattern count")
        check({oracle(read_sut_model(m))[1] for m in actual} == set(space), "representative coverage")
        check(len(actual) == len(space), "representative duplicates")
        expected_order = sorted(space, key=lambda mask: (sum(bool(mask & 2 ** k) for k in range(4)), mask))
        check([oracle(read_sut_model(m))[1] for m in actual] == expected_order, "representative order")
        data = saved["modes"][mode]
        check(data["representative_count"] == len(space), "saved pattern count")
        check(data["true_counts"] == counts, "saved truth counts")
        check(data["joint_truth_pattern_counts"] == joint, "saved joint counts")
        check(data["strict_overlap_count"] == strict_count, "saved strict overlap count")
        admitted = [r for r in records if mode == MODES[0] or r[3]]
        for premise_encoding in range(16):
            premises = tuple(f for i, f in enumerate(FORMS) if premise_encoding & 2 ** i)
            for conclusion in FORMS:
                query_checks += 1
                bad = [(n, mask) for n, values, mask, _ in admitted
                       if all(values[p] for p in premises) and not values[conclusion]]
                expected_min = min(bad) if bad else None
                witness = sut.counterexample(premises, conclusion, mode)
                check((witness is None) == (expected_min is None),
                      f"entailment disagreement: {mode}, {premises} => {conclusion}")
                if witness is None:
                    valid_queries[mode] += 1
                else:
                    values, mask, allowed, cells = oracle(read_sut_model(witness))
                    check(all(values[p] for p in premises) and not values[conclusion], "not a countermodel")
                    check(mode == MODES[0] or allowed, "countermodel inadmissible")
                    check((len(witness.universe), mask) == expected_min, "minimum size/mask tiebreak disagreement")
                    countermodel_size_counts[mode][len(witness.universe)] += 1
                if len(premises) == 1:
                    entry = data["implication_matrix"][premises[0]][conclusion]
                    check(entry["valid"] == (witness is None), "saved single-premise result")
                    check(entry["counterexample"] == (None if witness is None else witness.as_dict()),
                          "saved single-premise countermodel")
        nonreflexive = []
        for premise in FORMS:
            for conclusion in FORMS:
                if premise != conclusion and all(not v[premise] or v[conclusion] for v in space.values()):
                    nonreflexive.append(f"{premise}=>{conclusion}")
        check(nonreflexive == ([] if mode == MODES[0] else ["A=>I", "E=>O"]), "non-reflexive implications")
        check(all(v["A"] != v["O"] and v["E"] != v["I"] for v in space.values()), "contradictory pairs")
        # Stronger, fragment-specific observation: every attainable truth vector
        # already occurs on <=2 points. This does not preserve all four atoms.
        small_truth = {tuple(v[f] for f in FORMS) for n, v, mask, allowed in admitted if n <= 2}
        all_truth = {tuple(v[f] for f in FORMS) for v in space.values()}
        check(small_truth == all_truth, "two-point bound for pure A/E/I/O truth vectors")
        summaries[mode] = {"occupancy_patterns": len(space), "true_counts": counts,
                           "joint_truth_pattern_counts": joint, "strict_overlap_patterns": strict_count,
                           "nonreflexive_single_premise_implications": nonreflexive,
                           "valid_consequence_queries": valid_queries[mode],
                           "countermodel_minimum_size_counts": dict(countermodel_size_counts[mode])}
        print(f"PASS: {mode}: {len(space)} patterns; counts={counts}; joint={joint}; strict overlap={strict_count}")
    check(query_checks == 128, "consequence query total")
    print("PASS: all 128 premise-subset/conclusion/mode queries, including minimum size and numeric-mask tiebreak")
    print("PASS: fresh generator equals stored results.json; all saved implication entries match independent semantics")

    with (ROOT / "results/models.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    check(len(rows) == 25, "CSV row count")
    row_keys = set()
    for row in rows:
        mode, mask = row["mode"], int(row["mask"])
        key = mode, mask
        check(key not in row_keys, "duplicate CSV model")
        row_keys.add(key)
        u, s, p = (json.loads(row[name]) for name in ("U", "S", "P"))
        memberships = tuple((x in s, x in p) for x in u)
        values, actual_mask, allowed, cells = oracle(memberships)
        check(actual_mask == mask and mask in unique[mode], "CSV mask or mode")
        check({f: bool(int(row[f])) for f in FORMS} == values, "CSV truth")
        check(tuple(int(row[name]) for name in ("both", "s_only", "p_only", "outside")) == tuple(int(c > 0) for c in cells),
              "CSV occupancy fields")
    check(row_keys == {(mode, mask) for mode in MODES for mask in unique[mode]}, "CSV coverage")
    print("PASS: 25 CSV rows match independent semantics and exactly cover both mode spaces")
    print("PASS: theoretical scope review: four-atom compression is sufficient, not minimal; pure fixed-pair A/E/I/O needs at most 2 points")
    print("LIMIT: finite tests do not prove the infinite-domain claim; the four-atom compression argument does")
    print("LIMIT: no historical-priority, original-page, image-rendering, syllogistic, or arbitrary-formula-parser validation")
    report = {
        "status": "PASS", "started_at_utc": started, "finished_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "platform": platform.platform(),
        "oracle_method": "Independent pairs of subsets; point-membership counts; no production enumerators used for expectations",
        "sizes": [1, 2, 3, 4, 5], "labeled_models": len(records),
        "labeled_models_both_terms_nonempty": sum(r[3] for r in records),
        "labeled_by_size": dict(by_size), "nonempty_by_size": dict(nonempty_by_size),
        "consequence_queries": query_checks, "modes": summaries,
        "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                          for name in ("euler_semantics.py", "run.py", "tests/test_semantics.py", "README.zh-CN.md", "review/independent_oracle.py")},
    }
    (ROOT / "review/independent_results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
