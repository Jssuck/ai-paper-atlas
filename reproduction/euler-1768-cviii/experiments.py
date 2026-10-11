"""Deterministic experiments keyed to Letter CVIII, pp. 139-144."""
from logic import Theory, evaluate


def run():
    p, q = "p", "q"
    implication = ("implies", p, q)
    unrestricted = Theory([p, q])
    cases = {}

    def add(name, theory, premises, conclusion):
        cases[name] = theory.check(premises, conclusion)

    add("modus_ponens", unrestricted, [implication, p], q)
    add("modus_tollens", unrestricted, [implication, ("not", q)], ("not", p))
    add("denying_antecedent", unrestricted, [implication, ("not", p)], ("not", q))
    add("affirming_consequent", unrestricted, [implication, q], p)
    for name, conclusion in [("p", p), ("q", q),
                             ("not_p", ("not", p)), ("not_q", ("not", q))]:
        add("conditional_alone_not_" + name, unrestricted, [implication], conclusion)

    # A world where the material conditional is true does not establish a law.
    actual = {p: False, q: True}
    constrained = Theory([p, q], [implication])
    add("unrestricted_p_entails_q", unrestricted, [p], q)
    add("constrained_p_entails_q", constrained, [p], q)
    explicit = Theory([p, q], allowed_worlds=[
        {p: False, q: False}, {p: False, q: True}, {p: True, q: True}])
    add("explicit_worlds_p_entails_q", explicit, [p], q)

    body, spirit = "body", "spirit"
    exhaustive = ("or", body, spirit)
    exclusive = ("not", ("and", body, spirit))
    for label, constraints in [("neither", []), ("exhaustive", [exhaustive]),
                               ("exclusive", [exclusive]),
                               ("both", [exhaustive, exclusive])]:
        theory = Theory([body, spirit], constraints)
        add(label + "_not_body_to_spirit", theory, [("not", body)], spirit)
        add(label + "_body_to_not_spirit", theory, [body], ("not", spirit))

    add("inconsistent_premises", unrestricted, [p, ("not", p)], q)
    add("empty_theory", Theory([p, q], [p, ("not", p)]), [], q)
    return {
        "scope": "modern finite classical teaching model, not Euler's formal system",
        "single_assignment": {"world": actual,
                              "material_implication_true": evaluate(implication, actual)},
        "cases": cases,
    }
