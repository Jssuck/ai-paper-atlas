"""Deterministic, small, synthetic examples plus bounded finite checks."""

import json
from dataclasses import asdict
from itertools import product

from finite_checks import run_all
from model import (DeterministicPolicy, Multiset, descend_relation, descend_unary,
                   enumerate_policies, version_space)


def examples():
    objects = ("white_1", "white_2", "blue_3")
    color = {"white_1": "white", "white_2": "white", "blue_3": "blue"}
    rank = {"white_1": 1, "white_2": 2, "blue_3": 3}
    is_white = {obj: color[obj] == "white" for obj in objects}
    below = {(left, right): rank[left] < rank[right] for left, right in product(objects, repeat=2)}
    same_color = {(left, right): color[left] == color[right] for left, right in product(objects, repeat=2)}
    order_result = descend_relation(objects, color, below)
    same_result = descend_relation(objects, color, same_color)

    unit = Multiset.from_pairs(("unit",), (("unit", 1),))
    dozen = unit.scale(12)
    mixed = Multiset.from_pairs(("red", "blue"), (("red", 2), ("blue", 1)))
    other_mix = Multiset.from_pairs(("red", "blue"), (("red", 1), ("blue", 2)))
    erase_color = {"red": "token", "blue": "token"}
    hidden_extra = Multiset.from_pairs(("red", "blue"), (("red", 2), ("blue", 7)))

    stimuli = ("white_circle", "white_square", "blue_circle", "blue_square")
    stimulus_colors = dict(zip(stimuli, ("white", "white", "blue", "blue")))
    actions = ("0", "1")
    observed = (("white_circle", "1"), ("blue_circle", "0"))
    rule = DeterministicPolicy("color_rule", stimuli,
                               tuple("1" if stimulus_colors[s] == "white" else "0" for s in stimuli))
    lookup = DeterministicPolicy("observed_lookup_default_0", stimuli,
                                 tuple(dict(observed).get(s, "0") for s in stimuli))
    all_tables = enumerate_policies(stimuli, actions)
    space = version_space(stimuli, actions, all_tables, observed)
    restricted = version_space(stimuli, actions, (rule,), observed)
    after_holdout = version_space(stimuli, actions, (rule, lookup), observed + (("white_square", "1"),))
    return {
        "scope": "Synthetic finite teaching reconstruction; no claim to recreate a mind or establish incapacity.",
        "relation_descent": {
            "objects": list(objects), "color_representation": color, "rank": rank,
            "unary_is_white_quotient": descend_unary(objects, color, is_white).quotient,
            "same_color_descends": same_result.descends,
            "same_color_quotient": [{"pair": list(pair), "value": value}
                                    for pair, value in same_result.quotient.items()],
            "strict_rank_order_descends": order_result.descends,
            "strict_rank_order_conflicts": [asdict(conflict) for conflict in order_result.conflicts],
            "empty_domain_quotient": descend_relation((), {}, {}).quotient,
        },
        "composition": {
            "one_unit": unit.as_dict(), "dozen_units": dozen.as_dict(),
            "dozen_total": dozen.total, "ordinary_set_cardinality": len(set(["unit"] * 12)),
            "duplicate_entries_add": Multiset.from_pairs(("unit",), (("unit", 5), ("unit", 7))).as_dict(),
            "renaming_loss": {"different_inputs": [mixed.as_dict(), other_mix.as_dict()],
                              "same_output": mixed.rename(("token",), erase_color).as_dict(),
                              "outputs_equal": mixed.rename(("token",), erase_color) == other_mix.rename(("token",), erase_color)},
            "projection_loss": {"different_inputs": [mixed.as_dict(), hidden_extra.as_dict()],
                                "same_output": mixed.project(("red",)).as_dict(),
                                "outputs_equal": mixed.project(("red",)) == hidden_extra.project(("red",))},
        },
        "finite_observations": {
            "named_stimuli_colors": stimulus_colors, "observations": [list(pair) for pair in observed],
            "rule_table": dict(zip(stimuli, rule.responses)),
            "lookup_table": dict(zip(stimuli, lookup.responses)),
            "admissible_total_tables": len(all_tables), "survivors": len(space.survivors),
            "held_out": "white_square", "held_out_possible_actions": list(space.possible_actions("white_square")),
            "held_out_status": space.status("white_square"),
            "restricted_rule_only_status": restricted.status("white_square"),
            "restricted_rule_only_prediction": restricted.unanimous("white_square"),
            "two_candidate_survivors_after_positive_holdout": [p.name for p in after_holdout.survivors],
            "warning": "Unanimity depends on the admitted policies; behavioral tables do not identify an internal mechanism.",
        },
        "finite_checks": run_all(),
    }


if __name__ == "__main__":
    print(json.dumps(examples(), indent=2, sort_keys=True, ensure_ascii=False))
