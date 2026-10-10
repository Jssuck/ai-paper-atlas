"""Generate reviewable, deterministic reconstruction results (stdlib only)."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
from pathlib import Path

from gergonne import (
    ELEVEN, FIGURES, FOURTEEN, LETTERS, MODERN_FIGURE, RELATIONS, SIX,
    Literal, Model, Mood, candidates, conversion_targets, countermodel,
    equivalence_classes, models, proposition, reduction_closure,
    reductio_certificates, relation_triple, rule59_violations, valid_moods,
    weakened_neighbors,
)


def dump_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def dump_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def mood_record(mood: Mood, nonempty: bool = True) -> dict:
    witness = countermodel(mood, nonempty)
    premise_models = [m for m in models(nonempty) if mood.premises_hold(m)]
    return {
        "id": mood.id,
        "original_figure": mood.figure,
        "modern_figure": MODERN_FIGURE[mood.figure],
        "letters": "".join(mood.kinds),
        "original_ascii": mood.original_ascii,
        "literals": [x.text() for x in mood.literals()],
        "premise_model_count": len(premise_models),
        "valid": witness is None,
        "rule59_violations": list(rule59_violations(mood)),
        "countermodel": None if witness is None else witness.as_dict(),
    }


def example_record(figure: int, major: str, minor: str) -> dict:
    template = Mood(figure, major, minor, "A")
    applicable = [m for m in models() if template.premises_hold(m)]
    return {
        "premises": [x.text() for x in template.literals()[:2]],
        "original_premises_ascii": " ".join(template.original_ascii.split()[:2]),
        "relation_pairs": sorted({"".join(relation_triple(m)[:2]) for m in applicable}),
        "possible_conclusion_relations": sorted({relation_triple(m)[2] for m in applicable}),
        "entailed_conclusion_kinds": [k for k in LETTERS
                                      if all(Literal(k, "P", "G").holds(m) for m in applicable)],
        "premise_model_count": len(applicable),
        "minimal_witness_per_conclusion_relation": {
            r: next(m.as_dict() for m in applicable if relation_triple(m)[2] == r)
            for r in RELATIONS if any(relation_triple(m)[2] == r for m in applicable)
        },
    }


def reductions_record() -> dict:
    groups14 = equivalence_classes(False)
    groups11 = equivalence_classes(True)
    group_id = {mood: i for i, group in enumerate(groups11) for mood in group}
    edges = sorted({(group_id[m], group_id[n]) for m in valid_moods()
                    for n in weakened_neighbors(m) if group_id[m] != group_id[n]})
    source_groups = [i for i in range(len(groups11)) if not any(b == i for _, b in edges)]
    return {
        "counts": [len(valid_moods()), len(groups14), len(groups11), len(source_groups), 2],
        "caution": "24→14→11 uses equivalence; 11→6 uses entailment; 6→2 uses reductio, not equivalence classes.",
        "premise_conversion_classes": [[m.id for m in g] for g in groups14],
        "with_conclusion_conversion_classes": [[m.id for m in g] for g in groups11],
        "source_fourteen_representatives": [m.id for m in FOURTEEN],
        "source_eleven_representatives": [m.id for m in ELEVEN],
        "class_subsumption_edges": edges,
        "source_class_indices": source_groups,
        "source_six_representatives": [m.id for m in SIX],
        "six_closure_size": len(reduction_closure(SIX)),
        "four_reductio_certificates": reductio_certificates(),
    }


def opposition_record(nonempty: bool = True) -> dict:
    patterns = sorted({tuple(Literal(k, "P", "G").holds(m) for k in LETTERS)
                       for m in models(nonempty)})
    return {
        "column_order": list(LETTERS),
        "truth_patterns": patterns,
        "contradictories_A_n": all(a != n for a, _, _, n in patterns),
        "contradictories_N_a": all(n != a for _, n, a, _ in patterns),
        "contraries_A_N_never_both_true": all(not (a and n) for a, n, _, _ in patterns),
        "subcontraries_a_n_never_both_false": all(a or n for _, _, a, n in patterns),
        "subalternation_A_a": all(not a or i for a, _, i, _ in patterns),
        "subalternation_N_n": all(not n or o for _, n, _, o in patterns),
    }


def source_table_crosscheck() -> dict:
    """Compare to an independently image-transcribed historical fixture."""
    fixture = json.loads((Path(__file__).parent / "source_tables.json").read_text(encoding="utf-8"))
    expected = {(pair[0], pair[1], last) for last, pairs in fixture["row_lists"].items()
                for pair in pairs}
    actual = {relation_triple(m) for m in models()}
    printed55 = {k: set(pairs) for k, pairs in fixture["section55"]["printed_premise_pairs_by_conclusion"].items()}
    emended55 = {k: set(pairs) for k, pairs in fixture["section55"]["proposed_emended_premise_pairs_by_conclusion"].items()}
    computed55 = {
        k: {r1 + r2 for r1 in RELATIONS for r2 in RELATIONS
            if all(Literal(k, "P", "G").holds(m) for m in models()
                   if relation_triple(m)[:2] == (r1, r2))}
        for k in LETTERS
    }
    expected58 = {f"{f}:{word}" for f, words in fixture["section58"]["moods_by_original_figure"].items()
                  for word in words}
    actual58 = {m.id for m in valid_moods()}
    return {
        "fixture": "source_tables.json",
        "source": fixture["source"],
        "transcription": fixture["transcription"],
        "exact_set_match": actual == expected,
        "expected_count": len(expected),
        "computed_count": len(actual),
        "missing": sorted(expected - actual),
        "extra": sorted(actual - expected),
        "computed_rows_H_X_I_C_D": {r: sum(t[2] == r for t in actual) for r in RELATIONS},
        "section55_printed_exact_match": printed55 == computed55,
        "section55_proposed_emended_exact_match": emended55 == computed55,
        "section55_printed_discrepancies": {
            k: {"printed_but_not_valid": sorted(printed55[k] - computed55[k]),
                "valid_but_not_printed": sorted(computed55[k] - printed55[k])}
            for k in LETTERS if printed55[k] != computed55[k]
        },
        "section55_proposed_emendation": fixture["section55"]["proposed_emendation"],
        "section55_counterexample_to_printed_CH_entails_N": {
            **Model(48).as_dict(),
            "relation_triple": list(relation_triple(Model(48))),
            "N_P_G": Literal("N", "P", "G").holds(Model(48)),
        },
        "section55_pair_counts": {k: len(computed55[k]) for k in LETTERS},
        "section58_exact_match": expected58 == actual58,
        "sections63_64_representatives_exact_match": all(
            fixture["sections63_64"][key] == [m.id for m in values]
            for key, values in (("fourteen", FOURTEEN), ("eleven", ELEVEN), ("six", SIX))),
    }


def create_results(out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    all_records = [mood_record(m) for m in candidates()]
    valid = valid_moods()
    invalid = [record for record in all_records if not record["valid"]]
    triples = sorted({relation_triple(m) for m in models()})
    dump_json(out / "models_109.json", [m.as_dict() for m in models()])
    dump_json(out / "moods_256.json", all_records)
    dump_json(out / "invalid_countermodels_232.json", invalid)
    dump_csv(out / "relations_54.csv", ["M_G", "P_M", "P_G", "witness_mask"], [
        dict(zip(("M_G", "P_M", "P_G", "witness_mask"), (*triple,
             next(m.mask for m in models() if relation_triple(m) == triple))))
        for triple in triples
    ])
    composition = []
    for r1, r2 in ((a, b) for a in RELATIONS for b in RELATIONS):
        relevant = [m for m in models() if relation_triple(m)[:2] == (r1, r2)]
        composition.append({
            "M_G": r1, "P_M": r2,
            "possible_P_G": " ".join(r for r in RELATIONS
                                      if any(relation_triple(m)[2] == r for m in relevant)),
            "entailed_kinds": " ".join(k for k in LETTERS
                                        if all(Literal(k, "P", "G").holds(m) for m in relevant)),
            "pattern_count": len(relevant),
        })
    dump_csv(out / "relation_composition_25.csv", list(composition[0]), composition)
    dump_json(out / "reductions.json", reductions_record())
    examples = {
        "section51": example_record(2, "A", "N"),
        "section52": example_record(4, "A", "N"),
        "source_note": "§51: apply the volume erratum IG→IH; D is the modern alias for reversed C.",
        "direction_note": "The displayed original examples have N(M,P), not its equivalent simple converse N(P,M). They are original figures II and IV.",
        "source_transcription": json.loads((Path(__file__).parent / "source_tables.json").read_text(encoding="utf-8"))["sections51_52"],
    }
    dump_json(out / "original_examples.json", examples)
    empty_valid = valid_moods(False)
    lost = sorted(set(valid) - set(empty_valid))
    empty_boundary = {
        "model_patterns": len(models(False)),
        "five_way_relations_applicable": False,
        "valid_mood_count": len(empty_valid),
        "valid_mood_ids": [m.id for m in empty_valid],
        "lost_nine_moods_with_witnesses": [mood_record(m, False) for m in lost],
        "conversions": {k: conversion_targets(k, False) for k in LETTERS},
        "opposition": opposition_record(False),
        "note": "Modern boundary experiment only. Universals are vacuous on an empty subject; the original five relations are not applied here.",
    }
    dump_json(out / "empty_term_boundary.json", empty_boundary)
    summary = {
        "source": {"author": "J. D. Gergonne", "title": "Essai de dialectique rationnelle",
                   "issue_date": "1817-01-01", "printed_pages": "189–228",
                   "url": "https://www.numdam.org/item/AMPA_1816-1817__7__189_0/"},
        "implementation": "Original modern teaching reconstruction, Python standard library only",
        "nonempty_term_semantics": {
            "candidate_atom_patterns": 128,
            "admissible_patterns": len(models()),
            "distinct_relation_triples": len(triples),
            "triple_coordinate_order": ["M_G", "P_M", "P_G"],
            "candidate_moods": len(candidates()),
            "valid_moods": len(valid),
            "invalid_moods_with_countermodels": len(invalid),
            "valid_per_original_figure": dict(sorted(Counter(m.figure for m in valid).items())),
            "valid_by_conclusion_kind": {k: sum(m.conclusion == k for m in valid) for k in LETTERS},
            "max_minimal_countermodel_size": max(r["countermodel"]["size"] for r in invalid),
            "all_premise_pairs_satisfiable": all(r["premise_model_count"] > 0 for r in all_records),
            "rule59_semantics_disagreements": [r["id"] for r in all_records
                                              if r["valid"] != (not r["rule59_violations"])],
            "conversion_targets": {k: conversion_targets(k) for k in LETTERS},
            "opposition": opposition_record(),
        },
        "original_to_modern_figure": MODERN_FIGURE,
        "reductions": reductions_record()["counts"],
        "empty_term_semantics_valid_moods": len(empty_valid),
        "historical_table_crosscheck": source_table_crosscheck(),
        "execution_scope": "Finite extensional fragment only; not a replication of all philosophical claims or a software artifact from 1817.",
    }
    dump_json(out / "summary.json", summary)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("results"))
    args = parser.parse_args()
    summary = create_results(args.out)
    core = summary["nonempty_term_semantics"]
    print("Gergonne (1817): finite extensional teaching reconstruction")
    print(f"Patterns: {core['admissible_patterns']}/128; relation triples: {core['distinct_relation_triples']}")
    print(f"Valid moods: {core['valid_moods']}/256; countermodels: {core['invalid_moods_with_countermodels']}")
    print("Per original figure:", core["valid_per_original_figure"])
    print("Conclusion A/N/a/n:", core["valid_by_conclusion_kind"])
    print("§59 mismatches:", len(core["rule59_semantics_disagreements"]))
    print("Reductions:", " -> ".join(map(str, summary["reductions"])))
    print("Empty-term boundary valid moods:", summary["empty_term_semantics_valid_moods"])
    print("Results:", args.out)


if __name__ == "__main__":
    main()
