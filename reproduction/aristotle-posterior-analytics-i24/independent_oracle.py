"""Independent bit-mask and truth-model checks, not a general philosophical proof."""
import itertools
import json
from model import restriction_census, closure


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def bit_census(nmax):
    total = premises = bad = converse = nonempty = 0
    for n in range(nmax + 1):
        for s, g, p in itertools.product(range(1 << n), repeat=3):
            total += 1
            sg = not (s & ~g)
            gp = not (g & ~p)
            sp = not (s & ~p)
            if sg and gp:
                premises += 1
                bad += not sp
            if sg and sp and not gp:
                converse += 1
                nonempty += s != 0
    return {'assignments': total, 'forward_premise_cases': premises,
            'forward_violations': bad, 'converse_counterexamples': converse,
            'converse_nonempty_counterexamples': nonempty}


def model_intersection(facts, rules, atoms):
    # Enumerate truth assignments, retain classical models, intersect true atoms.
    models = []
    for bits in range(1 << len(atoms)):
        true = {a for i, a in enumerate(atoms) if bits & (1 << i)}
        if not facts <= true:
            continue
        if all(not set(body) <= true or head in true for body, head in rules):
            models.append(true)
    require(bool(models), 'positive Horn theory unexpectedly inconsistent')
    return frozenset.intersection(*(frozenset(m) for m in models))


def run():
    nmax = 5
    expected = bit_census(nmax)
    actual = restriction_census(nmax)
    require(all(actual[k] == v for k, v in expected.items()), 'set census mismatch')
    atoms = ('a', 'b', 'c')
    # 12 candidate rules: empty, singleton (excluding tautological heads),
    # and two-premise conjunction of the other two atoms for each head.
    candidates = []
    for head in atoms:
        other = [a for a in atoms if a != head]
        for body in ((), (other[0],), (other[1],), tuple(other)):
            candidates.append((body, head))
    theories = checks = 0
    for chosen in range(1 << len(candidates)):
        rules = [r for i, r in enumerate(candidates) if chosen & (1 << i)]
        theories += 1
        for bits in range(1 << len(atoms)):
            facts = {a for i, a in enumerate(atoms) if bits & (1 << i)}
            got = closure(facts, rules)
            want = model_intersection(facts, rules, atoms)
            require(got == want, 'Horn closure disagrees with truth-model entailment')
            checks += 1
    return {'set_census_universe_sizes': '0..5', 'set_census': expected,
            'horn_atoms': len(atoms), 'horn_candidate_rules': len(candidates),
            'horn_theories': theories, 'horn_initial_fact_sets_per_theory': 8,
            'horn_truth_model_checks': checks, 'differences': 0,
            'scope': 'finite implementation check; no causal, epistemic or universal-theorem certification'}


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
