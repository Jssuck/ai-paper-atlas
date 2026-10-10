"""Write deterministic experiment results to standard output."""
import json
from itertools import product
from logic import class_case, formula_suite, powerset, truth_table, two_world_model
from oracle import exhaustive_small_frames


def finite_classes(max_domain=6):
    by_size = []
    for n in range(max_domain + 1):
        universe = frozenset(range(n))
        count = empty_a = both_true = both_false = 0
        for a, b in product(powerset(range(n)), repeat=2):
            result = class_case(universe, a, b)
            assert result["positive_counterexamples"] == result["contrapositive_counterexamples"]
            assert result["all_A_are_B"] == result["all_not_B_are_not_A"]
            assert result["all_A_are_B"] == (not result["positive_counterexamples"])
            count += 1
            empty_a += not a
            both_true += result["all_A_are_B"]
            both_false += not result["all_A_are_B"]
        assert count == 4 ** n
        assert both_true == 3 ** n
        by_size.append({"domain_size": n, "class_pairs": count,
                        "empty_A_cases": empty_a, "both_true": both_true,
                        "both_false": both_false})
    return {"maximum_domain_size": max_domain, "by_size": by_size,
            "total_class_pairs": sum(x["class_pairs"] for x in by_size),
            "mismatches": 0}


def results():
    model = two_world_model()
    return {
        "schema_version": 1,
        "scope": "Original modern teaching reconstruction; not historical software or proof search",
        "classical_truth_table": truth_table(),
        "finite_class_enumeration": finite_classes(),
        "converse_counterexample": {
            "domain": [0, 1], "A": [0], "B": [0, 1],
            **{key: sorted(value) if isinstance(value, frozenset) else value
               for key, value in class_case({0, 1}, {0}, {0, 1}).items()}},
        "two_world_countermodel": {
            "worlds": [0, 1], "relation": [list(e) for e in sorted(model.frame.relation)],
            "valuation": {name: sorted(worlds) for name, worlds in model.valuation},
            "forcing": [{"world": w, **{name: model.force(w, f)
                         for name, f in formula_suite().items()}} for w in range(2)]},
        "small_frame_oracle": exhaustive_small_frames(),
    }


if __name__ == "__main__":
    print(json.dumps(results(), indent=2, ensure_ascii=False, sort_keys=True))
