#!/usr/bin/env python3
"""Generate auditable JSON/text results; no dependencies or network calls."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys

from euler_logic import (
    Argument, CATALOG, KINDS, REGIMES, TERMS, audit_fixed_first, catalog_matches,
    check_argument, ei_conversion_variants, explicit_examples, models, s,
)


def build_report():
    catalog_checks = {
        regime: [check_argument(argument, regime) for argument in CATALOG]
        for regime in REGIMES
    }
    variant_checks = {
        regime: [check_argument(variant, regime) for argument in CATALOG
                 for variant in ei_conversion_variants(argument)]
        for regime in REGIMES
    }
    converse_checks = {
        kind: check_argument(
            Argument(f"{kind}-converse", (s(kind, "A", "B"),), s(kind, "B", "A")),
            "empty_terms_allowed",
        ) for kind in KINDS
    }
    common_subject = Argument(
        "common_subject_existence", (s("A", "A", "B"), s("A", "A", "C")),
        s("I", "C", "B"),
    )
    particular_non_exclusion = Argument(
        "I_does_not_entail_O", (s("I", "A", "B"),), s("O", "A", "B"),
    )
    # Compare A5's conclusion to A's existence under exactly A5's premises.
    a5_equivalence_failures = [
        model.raw_mask for model in models()
        if all(model.evaluate(p) for p in CATALOG[4].premises)
        and model.evaluate(CATALOG[4].conclusion) != model.term_nonempty("A")
    ]
    return {
        "scope": "Modern set-theoretic reconstruction of nine supplied CIII forms; not a claim about all of Euler's syllogistic.",
        "semantics": {
            "A(X,Y)": "X is a subset of Y (no existential import)",
            "E(X,Y)": "X and Y are disjoint (no existential import)",
            "I(X,Y)": "X and Y have a nonempty intersection",
            "O(X,Y)": "X minus Y is nonempty",
        },
        "model_space": {
            "term_bits": {"A": 1, "B": 2, "C": 4},
            "occupancy_bit_meaning": "bit r records occupancy of type r, whose bits record membership in A,B,C",
            "raw_masks": 256,
            "distinct_nonempty_universe_models": 255,
            "zero_mask_policy": "Add one outside-all-terms witness; raw 0 and raw 1 are equivalent.",
            "assumptions": {
                regime: {
                    "selected_raw_masks": len(models(regime)),
                    "distinct_models": len({m.occupied_mask for m in models(regime)}),
                } for regime in REGIMES
            },
            "completeness_basis": "The region-abstraction theorem in PROOF.md, not a bounded numeric extrapolation.",
        },
        "catalog_checks": catalog_checks,
        "E_I_conversion_variant_checks": variant_checks,
        "simple_converse_checks": converse_checks,
        "I_implies_O_checks": {regime: check_argument(particular_non_exclusion, regime) for regime in REGIMES},
        "A5_conclusion_equivalent_to_A_existence_given_premises": not a5_equivalence_failures,
        "A5_existence_equivalence_counterexample_masks": a5_equivalence_failures,
        "fixed_first_audits": [audit_fixed_first(kind, regime) for regime in REGIMES for kind in ("A", "E")],
        "common_subject_case": {
            "formula": str(common_subject),
            "checks": {regime: check_argument(common_subject, regime) for regime in REGIMES},
            "displayed_matches_ordered": list(catalog_matches(common_subject)),
            "displayed_matches_unordered": list(catalog_matches(common_subject, True)),
            "interpretation": "A valid existence-dependent common-subject case absent from the nine displayed formulas under either explicit matching convention. Historical 'form' equivalence may be broader; no claim to have reconstructed it.",
        },
        "explicit_examples": explicit_examples(),
    }


def render_text(report):
    lines = [
        "Euler Letter CIII: modern set-semantics reproduction",
        "===================================================",
        report["scope"], "",
        "MODEL SPACE",
        "256 raw occupancy masks; 255 distinct nonempty-universe models.",
        "Raw mask 0 is given an outside witness and duplicates raw mask 1.",
        "A, E have no existential import. I, O assert a witness.",
        "A/E/I/O use all/subset, disjoint, some/intersection, some-not/difference.",
        "The finite check is complete for this fragment by PROOF.md's reduction.", "",
        "NINE DISPLAYED FORMS",
    ]
    for regime in REGIMES:
        summary = report["model_space"]["assumptions"][regime]
        lines.append(f"{regime}: {summary['selected_raw_masks']} raw masks / {summary['distinct_models']} distinct models")
        for check in report["catalog_checks"][regime]:
            status = "VALID" if check["valid"] else "INVALID"
            lines.append(f"  {check['label']}: {status}; {check['formula']}; premise masks={check['premise_satisfying_raw_masks']} raw/{check['distinct_premise_satisfying_models']} distinct; counterexample masks={len(check['counterexample_raw_masks'])} raw/{check['distinct_counterexample_models']} distinct")
    lines.extend(["", "CONVERSION AND EXISTENCE CHECKS"])
    for regime in REGIMES:
        checks = report["E_I_conversion_variant_checks"][regime]
        lines.append(f"{regime}: {len(checks)} explicit E/I conversion variants; {sum(bool(c['valid']) for c in checks)} valid.")
    for kind in KINDS:
        check = report["simple_converse_checks"][kind]
        lines.append(f"{kind}(A,B) => {kind}(B,A): {'VALID' if check['valid'] else 'INVALID'}")
    lines.append("I(A,B) => O(A,B): INVALID in all three regimes.")
    lines.append("Under A5's premises, I(C,A) iff A is nonempty: " + str(report["A5_conclusion_equivalent_to_A_existence_given_premises"]))
    lines.extend(["", "FIXED-FIRST-PREMISE AUDIT", "Each row checks 128 candidates: 16 second premises x 8 endpoint conclusions.",
                  "Matching always permits bijective term renaming and E/I conversion.",
                  "Ordered matching keeps premise order; unordered matching also exchanges the premises.",
                  "Neither matching adds subalternation or chains derived rules.",
                  "Additional candidates are not automatically historical omissions; see PROOF.md."])
    for audit in report["fixed_first_audits"]:
        lines.extend([
            f"{audit['regime']}, first {audit['first_premise']}:",
            f"  valid={audit['valid_ordered_candidates']}/128; E/I-only classes={audit['valid_classes_modulo_E_I_conversion_only']}; displayed matches ordered={audit['valid_candidates_matching_displayed_ordered']}, unordered={audit['valid_candidates_matching_displayed_unordered']}",
            "  Additional valid candidates even with unordered matching:",
        ])
        lines.extend("    " + formula for formula in audit["additional_valid_candidates_unordered"])
        if not audit["additional_valid_candidates_unordered"]:
            lines.append("    (none)")
    common = report["common_subject_case"]
    lines.extend(["", "FOCUSED COMMON-SUBJECT CASE", common["formula"]])
    for regime in REGIMES:
        check = common["checks"][regime]
        lines.append(f"  {regime}: {'VALID' if check['valid'] else 'INVALID'}")
    lines.append(common["interpretation"])
    lines.extend(["", "EXPLICIT NAMED EXAMPLES"])
    examples = report["explicit_examples"]
    for group in sorted(examples):
        value = examples[group]
        for example in value if isinstance(value, list) else [value]:
            lines.append(f"{group}: {example['name']}")
            lines.append("  universe=" + str(example["universe"]) + "; terms=" + str(example["terms"]))
            lines.append("  premises=" + " & ".join(example["premises"]) + "; true=" + str(example["all_premises_true"]))
            if "conclusion" in example:
                lines.append("  conclusion=" + example["conclusion"] + "; true=" + str(example["conclusion_true"]))
            if "C_to_B_relations" in example:
                lines.append("  C-to-B A/E/I/O=" + str(example["C_to_B_relations"]))
    return "\n".join(lines) + "\n"


def environment_record():
    root = Path(__file__).resolve().parent
    paths = [root / "euler_logic.py", root / "reproduce.py", root / "tests" / "test_euler_logic.py"]
    return {
        "recorded_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "dependencies": "Python standard library only; no packages installed",
        "network_used_by_reproduction": False,
        "source_sha256": {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("results"), help="Output directory (default: results)")
    args = parser.parse_args()
    report = build_report()
    # Expected failures are research results; assertions detect contradictions
    # with the supplied modern formalization, not invalid arguments themselves.
    for regime, checks in report["catalog_checks"].items():
        for check in checks:
            expected = not (regime == "empty_terms_allowed" and check["label"] == "A5")
            if check["valid"] != expected:
                raise AssertionError(f"Unexpected catalog result: {check}")
    if not report["A5_conclusion_equivalent_to_A_existence_given_premises"]:
        raise AssertionError("A5 existence equivalence failed")
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    rendered = render_text(report)
    (args.output / "report.txt").write_text(rendered, encoding="utf-8")
    environment = environment_record()
    (args.output / "environment.json").write_text(json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(rendered, end="")
    print(f"\nWrote {args.output / 'report.json'}, {args.output / 'report.txt'}, and {args.output / 'environment.json'}")


if __name__ == "__main__":
    main()
