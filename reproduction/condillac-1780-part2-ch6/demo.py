"""Deterministic, inspectable examples; stdout is JSON, not historical evidence."""
import json
import condillac_model as m


def main():
    system = m.DefinitionSystem(("p", "q"), (
        m.Definition("both", m.And(m.Var("p"), m.Var("q"))),
        m.Definition("not_both", m.Not(m.Var("both"))),
    ))
    worlds = system.worlds()
    hidden = m.analyze_observations(m.enumerate_worlds(("p", "q")), (m.Var("p"),), m.Var("q"))
    represented = m.analyze_observations(m.enumerate_worlds(("p", "q")),
                                       (m.Var("p"), m.Var("q")), m.And(m.Var("p"), m.Var("q")))
    no_features = m.analyze_observations(m.enumerate_worlds(("p",)), (), m.Var("p"))
    rules = (m.Rule(frozenset(("sense",)), "compare"), m.Rule(frozenset(("compare",)), "name"))
    plan = m.plan_learning(("sense",), rules)
    backward = m.verify_order(("sense",), rules, reversed(plan))
    cycle = (m.Rule(frozenset(("a",)), "b"), m.Rule(frozenset(("b",)), "a"))
    output = {
        "label": "Original modern teaching model, not a historical reconstruction or psychological experiment",
        "definition_expansions": worlds,
        "old_worlds_before_evidence": len(worlds),
        "after_evidence_both": m.filter_evidence(worlds, m.Var("both")),
        "cyclic_no_solution": m.satisfying_extensions({}, (m.Definition("d", m.Not(m.Var("d"))),)),
        "cyclic_two_solutions": m.satisfying_extensions({}, (m.Definition("d", m.Var("d")),)),
        "old_name_reuse_rejects_p_false": m.satisfying_extensions({"p": False}, (m.Definition("p", m.Const(True)),)),
        "hidden_q": {"definable": hidden.definable, "witness": hidden.witness},
        "both_from_p_and_q": {"definable": represented.definable, "table": represented.table},
        "empty_observation_nonconstant_target": {"definable": no_features.definable, "witness": no_features.witness},
        "learning": {"plan": plan, "forward_valid": m.verify_order(("sense",), rules, plan).valid,
                     "reverse_valid": backward.valid, "reverse_failure_index": backward.failure_index,
                     "reverse_missing_alternatives": [sorted(x) for x in backward.missing_alternatives],
                     "closure": sorted(m.forward_closure(("sense",), rules))},
        "cycle_without_seed": sorted(m.forward_closure((), cycle)),
        "cycle_with_a_seed": sorted(m.forward_closure(("a",), cycle)),
        "scope": "These results concern the declared finite semantics and rules only.",
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
