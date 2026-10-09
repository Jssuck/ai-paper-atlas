"""Worked examples. Run with: python -B run_demo.py"""
from curry import (
    Atom, B, I, app, parse, pretty, normalize, normal, sequence, dot,
    AXIOM_ARITIES, BW_P521_LITERAL, saturated_axiom_check,
    check, certify_run, axiom, cbi_identity_proof, right_identity_proof,
    distribution_proof, associativity_proof, axiom_names_used, proof_nodes,
)


def show_trace(source, fuel=30, detect_cycles=True):
    term = parse(source)
    run = normalize(term, fuel, detect_cycles)
    print(f"start: {source}  [expanded: {pretty(term)}]")
    for i, s in enumerate(run.steps, 1):
        where = "root" if not s.path else ".".join(map(str, s.path))
        print(f"  {i:02d}. {s.rule}@{where}: {pretty(s.after)}")
    print(f"status={run.status}; contractions={len(run.steps)}")
    if run.cycle_length is not None:
        print(f"cycle_start={run.cycle_start}; cycle_length={run.cycle_length}")
    assert check(certify_run(run)) == (term, run.end)
    return run


def show_axiom_actions():
    print("16 finite axioms: symbolic saturated actions (not derivations of bare axioms)")
    for name, arity in AXIOM_ARITIES.items():
        a, b = saturated_axiom_check(name, arity)
        print(f"  Ax.{name:<3} args={arity}; steps L/R={len(a.steps)}/{len(b.steps)}; {pretty(a.end)}")


def show_certificate(label, proof):
    lhs, rhs = check(proof)
    print(f"{label}: {pretty(lhs)} = {pretty(rhs)}")
    print(f"  checked nodes={proof_nodes(proof)}; finite axioms={','.join(sorted(axiom_names_used(proof))) or '(none)'}")


def main():
    print("Curry 1930 Teil I, pp.509–536 — standard-library reproduction")
    print("Two layers: four-rule contextual reduction; separately checked equational certificates.")
    print("No claim of full Q/Π/P/Λ formalization, consistency, completeness, or Part II reproduction.\n")
    print("1. Identity is the defined term W K, not a primitive")
    show_trace("I x")
    print("\n2. Context reduction and discarded nontermination")
    show_trace("f (I x)")
    show_trace("K x (W W W)")
    print("\n3. W W W contracts to itself; a step is not a normal form")
    show_trace("W W W")
    show_trace("W W W", fuel=4, detect_cycles=False)
    print("Fuel exhaustion alone does not prove nonnormalization.\n")
    print("4. Indexed sequences (definitions pp.529, 531–532)")
    for kind, source in (("B", "f g x1 x2 x3"), ("C", "x0 x1 x2 x3 x4"),
                         ("W", "x0 x1 x2 x3"), ("K", "x0 x1 x2 x3")):
        args = tuple(Atom(s) for s in source.split())
        term = app(sequence(kind, 3), *args)
        print(f"{kind}_3 {source} -> {pretty(normal(term))}")
    print("\n5. Finite axioms checked after enough fresh symbolic arguments")
    show_axiom_actions()
    print("\n6. Source-critical Ax.(BW) case")
    lhs, literal = BW_P521_LITERAL
    xs = tuple(Atom(f"x{i}") for i in range(3))
    print("p.521 literal-looking reading:")
    print("  left :", pretty(normal(app(lhs, *xs))))
    print("  right:", pretty(normal(app(literal, *xs))))
    print("The implemented BW premise follows the unambiguous left-associated p.534 product.")
    print("This is an observed discrepancy, not a claim to have found an official erratum.")
    print("\n7. BI=I: different four-rule normal forms, explicit extra axiom")
    print("normal(B I) =", pretty(normal(app(B, I))))
    print("normal(I)   =", pretty(normal(I)))
    x, y, z, u = map(Atom, "xyzu")
    print("with x,y appended:", pretty(normal(app(B, I, x, y))), "=", pretty(normal(app(I, x, y))))
    show_certificate("BI=I", axiom("I2"))
    show_certificate("CBI=I", cbi_identity_proof())
    show_certificate("B x I=x", right_identity_proof(x))
    print("\n8. Composition associativity needs an equational proof before application")
    lhs, rhs = dot(dot(x, y), z), dot(x, dot(y, z))
    print("bare left NF :", pretty(normal(lhs)))
    print("bare right NF:", pretty(normal(rhs)))
    print("applied to u :", pretty(normal(app(lhs, u))), "=", pretty(normal(app(rhs, u))))
    show_certificate("B distributes over dot", distribution_proof(x, y))
    show_certificate("dot associativity", associativity_proof(x, y, z))
    omega = parse("W W W")
    p = associativity_proof(omega, omega, omega)
    check(p)
    print("Finite associativity certificate also checked with all arguments W W W (no argument evaluation).")
    print("\nPASS: all worked checks completed. See tests and README for limits.")


if __name__ == "__main__":
    main()
