#!/usr/bin/env python3
"""Emit the deterministic, fully enumerated teaching report (stdlib only)."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from itertools import combinations

from euler_civ import (ALL_MODELS, TERMS, PRINTED_FORMS, REPAIRED_FORMS,
                       DERIVATIONS, Argument, canonical, check,
                       equivalent_groups, euler_style_candidates,
                       minimal_nonempty_assumptions, models_under, standard_candidates)

REGIMES = {"term_empty_permitted": (), "all_three_terms_nonempty": tuple(TERMS)}


def form_report(label: str, argument: Argument) -> dict:
    return {
        "label": label,
        "source_printed_page": 116 if list(PRINTED_FORMS).index(label) < 6 else 117,
        **argument.as_dict(),
        "structural_class": canonical(argument),
        "syntactic_class_without_ei_conversion": canonical(argument, False),
        "derivation": DERIVATIONS[label],
        "minimal_nonempty_assumptions": [list(s) for s in minimal_nonempty_assumptions(argument)],
        "all_nonempty_assumption_checks": [
            {"required_terms": list(subset), **check(argument, subset).as_dict(argument)}
            for size in range(4) for subset in combinations(TERMS, size)],
        "regimes": {name: check(argument, required).as_dict(argument)
                    for name, required in REGIMES.items()},
    }


def scope_report(named: list[tuple[str, Argument]], recap: dict[str, Argument]) -> dict:
    recap_keys = {canonical(argument) for argument in recap.values()}
    recap_syntactic_keys = {canonical(argument, False) for argument in recap.values()}
    data = {"candidate_count": len(named),
            "candidate_identifiers_unique": len({name for name, _ in named}) == len(named),
            "candidate_codes_unique": len({arg.code for _, arg in named}) == len(named),
            "all_candidate_structural_class_count": len({canonical(arg) for _, arg in named}),
            "regimes": {}, "cases": []}
    for name, required in REGIMES.items():
        valid = [(label, arg) for label, arg in named if check(arg, required).valid]
        groups = equivalent_groups(valid)
        uncovered = [group for group in groups if group["canonical_key"] not in recap_keys]
        syntactic_groups = equivalent_groups(valid, False)
        syntactic_uncovered = [g for g in syntactic_groups if g["canonical_key"] not in recap_syntactic_keys]
        data["regimes"][name] = {
            "valid_count": len(valid),
            "valid_ids": [label for label, _ in valid],
            "valid_structural_class_count": len(groups),
            "valid_structural_classes": groups,
            "recap_covered_valid_class_count": len(groups) - len(uncovered),
            "recap_uncovered_valid_classes": uncovered,
            "without_ei_conversion": {
                "valid_class_count": len(syntactic_groups),
                "valid_classes": syntactic_groups,
                "recap_covered_valid_class_count": len(syntactic_groups) - len(syntactic_uncovered),
                "recap_uncovered_valid_classes": syntactic_uncovered,
                "recap_covered_valid_candidate_count": sum(canonical(a, False) in recap_syntactic_keys for _, a in valid),
            },
        }
    for label, arg in named:
        data["cases"].append({"id": label, **arg.as_dict(), "canonical_key": canonical(arg),
                              "canonical_key_without_ei_conversion": canonical(arg, False),
                              "equivalent_repaired_recap_entries":
                                  [key for key, item in recap.items() if canonical(item) == canonical(arg)],
                              "regime_validity": {name: check(arg, required).valid
                                                  for name, required in REGIMES.items()}})
    return data


def build_report() -> dict:
    standard = [(f"{mood}-{figure}", arg) for mood, figure, arg in standard_candidates()]
    larger = [(arg.code, arg) for arg in euler_style_candidates()]
    particular = [(arg.code, arg) for arg in euler_style_candidates("IO")]
    printed_keys = {canonical(arg) for arg in PRINTED_FORMS.values()}
    repaired_keys = {canonical(arg) for arg in REPAIRED_FORMS.values()}
    return {
        "schema_version": 1,
        "title": "Euler 1768 Letter CIV: finite-model teaching reconstruction",
        "historical_scope": {
            "source": "Recap, printed pp. 116-117; preceding displayed rule on p. 116",
            "source_scans": ["1768-pdf137.png", "1768-pdf138.png"],
            "printed_recap_entries": len(PRINTED_FORMS),
            "printed_xvi": PRINTED_FORMS["XVI"].code,
            "teaching_repair_xvi": REPAIRED_FORMS["XVI"].code,
            "repair_status": "Interpretive teaching repair supported by preceding rule; not a verified formal erratum.",
            "warning": "The repaired syntactic quotient has 19 classes, matching the historical count numerically; E/I-conversion and modern candidate scopes produce other counts. Numerical agreement alone does not establish historical intent."
        },
        "semantics": {
            "universe": "Nonempty; arbitrary finite or infinite domains reduced to occupied membership atoms.",
            "atoms": [{"atom": atom, "membership": {t: bool(atom & (1 << i)) for i, t in enumerate(TERMS)}}
                      for atom in range(8)],
            "model_count": len(ALL_MODELS),
            "model_order": "Minimum number of occupied atoms, then numerical occupancy mask.",
            "regimes": {name: {"required_nonempty_terms": list(required),
                                "model_count": len(models_under(required))}
                        for name, required in REGIMES.items()},
            "moods": {"A": "subject subset of predicate; no existential import",
                      "E": "subject and predicate disjoint; no existential import",
                      "I": "subject intersects predicate",
                      "O": "subject has a member outside predicate"},
            "existence_assumptions": "All 8 subsets of {A,B,C}; reported minima use set inclusion.",
        },
        "printed_forms": [form_report(label, arg) for label, arg in PRINTED_FORMS.items()],
        "repaired_forms": [form_report(label, arg) for label, arg in REPAIRED_FORMS.items()],
        "syntactic_equivalence_without_ei_conversion": {
            "allowed": ["simultaneous permutation of three term names", "exchange premises"],
            "excluded": ["E/I term exchange", "subalternation", "semantic implication equivalence"],
            "printed_class_count": len({canonical(a, False) for a in PRINTED_FORMS.values()}),
            "printed_classes": equivalent_groups(PRINTED_FORMS.items(), False),
            "repaired_class_count": len({canonical(a, False) for a in REPAIRED_FORMS.values()}),
            "repaired_classes": equivalent_groups(REPAIRED_FORMS.items(), False),
        },
        "structural_equivalence": {
            "allowed": ["simultaneous permutation of three term names", "exchange premises", "exchange terms within E or I"],
            "excluded": ["subalternation", "contraposition", "exchange conclusion with a premise", "semantic implication equivalence"],
            "printed_class_count": len(printed_keys),
            "printed_classes": equivalent_groups(PRINTED_FORMS.items()),
            "repaired_class_count": len(repaired_keys),
            "repaired_classes": equivalent_groups(REPAIRED_FORMS.items()),
        },
        "standard_256": {
            "definition": "Four figures times 4 cubed moods, major premise first; S=C, P=B, M=A; conclusion C-B.",
            **scope_report(standard, REPAIRED_FORMS),
        },
        "euler_style_512": {
            "definition": "First premise qAB. Second pair AC, CA, BC, or CB. Conclusion is the unused pair in either direction. Each q is independently A/E/I/O.",
            "printed_xvi_in_scope": PRINTED_FORMS["XVI"].code in {arg.code for _, arg in larger},
            "all_repaired_entries_in_scope": all(arg.code in {x.code for _, x in larger} for arg in REPAIRED_FORMS.values()),
            **scope_report(larger, REPAIRED_FORMS),
        },
        "particular_first_256": {
            "definition": "The exact I/O-first slice of the 512-candidate universe; no claim about arbitrary predicate logic.",
            **scope_report(particular, REPAIRED_FORMS),
        },
    }


def encode_report(report: dict) -> str:
    return json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def summary(report: dict) -> str:
    lines = [report["title"], f"Models: {report['semantics']['model_count']} occupied-atom configurations"]
    for version in ("printed", "repaired"):
        forms = report[version + "_forms"]
        lines.append(f"{version.capitalize()} recap: {len(forms)} entries")
        for regime in REGIMES:
            valid = [f["label"] for f in forms if f["regimes"][regime]["valid"]]
            invalid = [f["label"] for f in forms if not f["regimes"][regime]["valid"]]
            lines.append(f"  {regime}: {len(valid)} valid; invalid: {', '.join(invalid) or 'none'}")
        lines.append(f"  classes without E/I conversion: {report['syntactic_equivalence_without_ei_conversion'][version + '_class_count']}")
        lines.append(f"  classes with E/I conversion: {report['structural_equivalence'][version + '_class_count']}")
    for key in ("standard_256", "euler_style_512", "particular_first_256"):
        scope = report[key]
        lines.append(f"{key}: {scope['candidate_count']} candidates")
        for regime in REGIMES:
            row = scope["regimes"][regime]
            lines.append(f"  {regime}: {row['valid_count']} valid; {row['valid_structural_class_count']} structural classes; "
                         f"{row['recap_covered_valid_class_count']} covered by repaired recap")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write deterministic report JSON to this path")
    parser.add_argument("--check", type=Path, help="Require byte identity with a previously generated JSON report")
    parser.add_argument("--json", action="store_true", help="Print JSON rather than the short summary")
    args = parser.parse_args()
    report = build_report()
    encoded = encode_report(report)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    if args.check:
        if args.check.read_bytes() != encoded.encode("utf-8"):
            parser.exit(1, "Report differs from stored reference.\n")
    print(encoded if args.json else summary(report), end="" if args.json else "\n")
    if not args.json:
        print("Report SHA-256: " + hashlib.sha256(encoded.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
