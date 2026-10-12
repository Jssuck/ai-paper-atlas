"""Print deterministic exact results for three modern educational models."""
import json
from fractions import Fraction
from model import Tree, RepresentationDomain, Judgment, copy_judgment, distinct_origins, diffuse


def tree_spec():
    return {
        "domain": ["a", "b", "c", "d"], "root": "r",
        "predicates": {
            "round": {"a": False, "b": False, "c": True, "d": True},
            "bright": {"a": False, "b": True, "c": False, "d": True},
        },
        "nodes": {
            "r": {"predicate": "round", "false": "n", "true": "s"},
            "s": {"predicate": "bright", "false": "u", "true": "y"},
            "n": {"label": "drop"}, "u": {"label": "drop"}, "y": {"label": "keep"},
        },
    }


def article_examples():
    objects = ["00", "01", "10", "11"]
    spec = {
        "domain": objects, "root": "r",
        "predicates": {"first": {x: x[0] == "1" for x in objects},
                       "second": {x: x[1] == "1" for x in objects}},
        "nodes": {
            "r": {"predicate": "first", "false": "left", "true": "right"},
            "left": {"predicate": "second", "false": "00", "true": "01"},
            "right": {"predicate": "second", "false": "10", "true": "11"},
            "00": {"label": "0"}, "01": {"label": "1"},
            "10": {"label": "1"}, "11": {"label": "0"},
        },
    }
    correct = Tree(spec)
    spec["nodes"]["11"]["label"] = "1"
    wrong = Tree(spec)
    correct_table, wrong_table = correct.compile(), wrong.compile()
    truth = {x: str(int(x[0] != x[1])) for x in objects}
    codes = {x: x[0] for x in objects}
    source = RepresentationDomain({"objects": objects, "codes": codes, "labels": codes})
    target = RepresentationDomain({"objects": objects, "codes": codes,
                                   "labels": {x: x[1] for x in objects}})
    decoder = {"0": "0", "1": "1"}
    refined = RepresentationDomain({"objects": objects, "codes": {x: x for x in objects},
                                    "labels": {x: x[1] for x in objects}})
    tied_spec = {"objects": ["v0", "v1", "v2"],
                 "codes": {"v0": "same", "v1": "same", "v2": "same"},
                 "labels": {"v0": "0", "v1": "0", "v2": "1"},
                 "weights": {"v0": 2, "v1": 1, "v2": 3}}
    tied = RepresentationDomain(tied_spec)
    tied_spec["codes"] = {"v0": "group0", "v1": "group0", "v2": "group1"}
    tied_refined = RepresentationDomain(tied_spec)
    return {
        "xor": {
            "inputs": objects,
            "true_labels": [truth[x] for x in objects],
            "tree_labels": [correct.evaluate(x).label for x in objects],
            "compiled_labels": [correct_table.evaluate(x).label for x in objects],
            "predicate_tests_per_query": [correct.evaluate(x).predicate_tests for x in objects],
            "compilation_predicate_tests": sum(correct.evaluate(x).predicate_tests for x in objects),
            "stored_labels": len(correct_table.table),
            "wrong_tree_labels": [wrong.evaluate(x).label for x in objects],
            "wrong_compiled_labels": [wrong_table.evaluate(x).label for x in objects],
            "wrong_tree_risk": str(Fraction(sum(wrong.evaluate(x).label != truth[x] for x in objects), len(objects))),
            "wrong_compiled_risk": str(Fraction(sum(wrong_table.evaluate(x).label != truth[x] for x in objects), len(objects))),
        },
        "first_bit_transfer": {
            "source_risk": str(source.risk(decoder)),
            "target_risk": str(target.risk(decoder)),
            "target_structurally_sufficient": target.sufficient(),
            "minimum_target_risk": str(target.best_decoder().risk),
            "refined_minimum_target_risk": str(refined.best_decoder().risk),
        },
        "weighted_tie_and_refinement": {
            "total_mass": str(tied.total_mass),
            "minimum_risk": str(tied.best_decoder().risk),
            "deterministic_decoder": dict(tied.best_decoder().decoder),
            "refined_minimum_risk": str(tied_refined.best_decoder().risk),
        },
    }


def results():
    tree = Tree(tree_spec())
    compiled = tree.compile()
    truth = {"a": "drop", "b": "drop", "c": "keep", "d": "keep"}
    rows = [{"input": item, "tree_label": tree.evaluate(item).label,
             "predicate_tests": tree.evaluate(item).predicate_tests,
             "compiled_label": compiled.evaluate(item).label,
             "abstract_lookups": compiled.evaluate(item).abstract_lookups,
             "true_label": truth[item]} for item in tree.domain]
    source = RepresentationDomain({"objects": ["sA", "sB"],
        "codes": {"sA": "A", "sB": "B"}, "labels": {"sA": "keep", "sB": "drop"}})
    decoder = {"A": "keep", "B": "drop"}
    target = RepresentationDomain({"objects": ["t0", "t1", "t2", "t3"],
        "codes": {"t0": "A", "t1": "A", "t2": "B", "t3": "B"},
        "labels": {"t0": "keep", "t1": "drop", "t2": "drop", "t3": "keep"},
        "weights": {"t0": 3, "t1": 1, "t2": 2, "t3": 2}})
    shifted = RepresentationDomain({"objects": ["uA", "uB"],
        "codes": {"uA": "A", "uB": "B"}, "labels": {"uA": "drop", "uB": "keep"}})
    zero = RepresentationDomain({"objects": ["z0", "z1", "z2", "z3"],
        "codes": {"z0": "A", "z1": "A", "z2": "Z", "z3": "Z"},
        "labels": {"z0": "keep", "z1": "drop", "z2": "keep", "z3": "drop"},
        "weights": {"z0": "2/3", "z1": 0, "z2": 0, "z3": 0}})
    best = target.best_decoder()
    graph = {"nodes": ["A", "B", "C", "D", "isolated"],
             "edges": [["A", "B"], ["B", "C"], ["C", "D"]]}
    faster = {"nodes": graph["nodes"], "edges": graph["edges"] + [["A", "C"], ["A", "D"]]}
    false_claim = Judgment("2 + 2 = 5", "one-original-judgment")
    slow = diffuse(graph, ["A"], false_claim)
    fast = diffuse(faster, ["A"], false_claim)
    truthful = diffuse(faster, ["A"], Judgment("2 + 2 = 4", "one-original-judgment"))
    return {
        "scope": "Modern finite illustration; not Condillac's mathematics or historical/psychological evidence.",
        "article_examples": article_examples(),
        "A_compilation": {
            "rows": rows, "stored_labels": len(compiled.table),
            "uniform_tree_error": str(Fraction(sum(row["tree_label"] != row["true_label"] for row in rows), len(rows))),
            "uniform_compiled_error": str(Fraction(sum(row["compiled_label"] != row["true_label"] for row in rows), len(rows))),
            "fast_wrong_input": "c", "training_only_keys": sorted(tree.train_lookup(["b", "d"]).table),
            "unseen_inputs_without_guarantee": ["a", "c"],
            "root_leaf_predicate_tests": Tree({"domain": ["x"], "root": "r", "nodes": {"r": {"label": "keep"}}, "predicates": {}}).evaluate("x").predicate_tests,
        },
        "B_representation": {
            "source_risk": str(source.risk(decoder)), "target_risk": str(target.risk(decoder)),
            "target_total_mass": str(target.total_mass), "target_structurally_sufficient": target.sufficient(),
            "optimal_decoder": dict(best.decoder), "minimum_error_mass": str(best.error_mass), "minimum_target_risk": str(best.risk),
            "shifted_target_structurally_sufficient": shifted.sufficient(), "shifted_transferred_risk": str(shifted.risk(decoder)),
            "shifted_minimum_risk": str(shifted.best_decoder().risk),
            "zero_weight_structurally_sufficient": zero.sufficient(), "zero_weight_support_sufficient": zero.sufficient(True),
            "zero_weight_minimum_risk": str(zero.best_decoder().risk), "zero_weight_decoder": dict(zero.best_decoder().decoder),
        },
        "B_copies_and_diffusion": {
            "copies": 100, "distinct_recorded_origins": len(distinct_origins(copy_judgment(false_claim, 100))),
            "false_claim": false_claim.claim,
            "chain_snapshots": [sorted(snapshot) for snapshot in slow.snapshots],
            "shortcut_snapshots": [sorted(snapshot) for snapshot in fast.snapshots],
            "chain_first_arrival": dict(slow.first_arrival), "shortcut_first_arrival": dict(fast.first_arrival),
            "same_eventual_reach": slow.holders == fast.holders,
            "truthful_and_false_claim_same_spread": truthful.snapshots == fast.snapshots,
        },
    }


if __name__ == "__main__":
    print(json.dumps(results(), ensure_ascii=False, indent=2, sort_keys=True))
