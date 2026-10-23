import json
from math import gcd
from model import Space, Formula, Assumption, ReductioCertificate, verify_reductio, entails, counterexample, is_even_square_equivalent


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    space = Space(('P', 'S'))
    p, s = space.atom('P'), space.atom('S')
    formulas = [Formula(space, {r for r in range(4) if mask & (1 << r)}) for mask in range(16)]
    valid_pairs = 0
    certificates = 0
    accepted = 0
    for gamma in formulas:
        for h in formulas:
            inconsistent_inner = not (gamma.true_rows & h.true_rows)
            require(inconsistent_inner == entails((gamma,), h.negated()), 'discharge equivalence')
            valid_pairs += inconsistent_inner
            for c in formulas:
                cert = ReductioCertificate((Assumption('background', gamma),), Assumption('temporary', h), c)
                observed = verify_reductio(cert)
                expected = inconsistent_inner and c == h.negated()
                require(observed == expected, 'certificate rule mismatch')
                certificates += 1
                accepted += observed
    parity_checks = 0
    for n in range(-256, 257):
        require(is_even_square_equivalent(n), 'parity mismatch')
        parity_checks += 1
    pairs = coprime_pairs = solutions = 0
    for numerator in range(1, 65):
        for denominator in range(1, 65):
            pairs += 1
            if gcd(numerator, denominator) == 1:
                coprime_pairs += 1
                solutions += numerator * numerator == 2 * denominator * denominator
    require(solutions == 0, 'unexpected bounded rational solution')
    require(entails((s.implies(p), p.negated()), s.negated()), 'bridge result')
    result = {
        'truth_assignments': space.rows,
        'truth_set_formulas': len(formulas),
        'background_hypothesis_pairs': len(formulas) ** 2,
        'inconsistent_inner_pairs': valid_pairs,
        'certificate_checks': certificates,
        'accepted_certificates': accepted,
        'missing_bridge_counterexample': counterexample((p.negated(),), s.negated()),
        'reverse_bridge_counterexample': counterexample((p.implies(s), p.negated()), s.negated()),
        'integer_parity_checks': parity_checks,
        'positive_fraction_pairs': pairs,
        'coprime_fraction_pairs': coprime_pairs,
        'bounded_sqrt2_solutions': solutions,
        'scope': 'Finite implementation checks only; not proof of general theorems or unique ancient semantics.'
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
