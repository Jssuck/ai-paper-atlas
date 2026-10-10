"""Independent, source-oriented audit; stdlib only, deterministic and read-only.

Run from any working directory. Expected values are built without production
truth evaluators, inference rules, probability constructors or model generators.
The historical report-first matrix is retained in the probability oracle.
This file emits a small JSON result, not host paths or environment variables.
"""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import demorgan as d

SYMBOLS = ('))', '((', ').(', '(.)', '()', ')(', '(.(', ').)')
RESULTS = {}


def ordinary(s, universe, x, y):
    """p.91 propositions, independently expressed as region counts."""
    counts = [0, 0, 0, 0]
    for a in universe:
        counts[2 * (a in x) + (a in y)] += 1
    neither, y_only, x_only, both = counts
    return {
        '))': x_only == 0, '((': y_only == 0,
        ').(': both == 0, '(.)': neither == 0,
        '()': both > 0, ')(': neither > 0,
        '(.(': x_only > 0, ').)': y_only > 0,
    }[s]


def exemplar(s, x, y, relation=None):
    """p.101 each statement directly; no recursive contradiction shortcut."""
    relates = (lambda a, b: a == b) if relation is None else (lambda a, b: (a, b) in relation)
    return {
        ')(': lambda: all(relates(a, b) for a in x for b in y),
        '(.)': lambda: any(not relates(a, b) for a in x for b in y),
        '))': lambda: all(any(relates(a, b) for b in y) for a in x),
        '(.(': lambda: any(all(not relates(a, b) for b in y) for a in x),
        '((': lambda: all(any(relates(a, b) for a in x) for b in y),
        ').)': lambda: any(all(not relates(a, b) for a in x) for b in y),
        ').(': lambda: all(not relates(a, b) for a in x for b in y),
        '()': lambda: any(relates(a, b) for a in x for b in y),
    }[s]()


def entailments(rows):
    """Find all conclusions supported by model truth, without a syntactic rule."""
    result = {}
    for i, j in product(range(8), repeat=2):
        candidates = set(range(8))
        compatible = 0
        for xy, yz, xz in rows:
            if xy[i] and yz[j]:
                compatible += 1
                candidates.intersection_update(k for k in candidates if xz[k])
        assert compatible, (i, j, 'premises have no model')
        result[SYMBOLS[i], SYMBOLS[j]] = {SYMBOLS[k] for k in candidates}
    return result


def check_symbols():
    ordinary_rows, proper_rows = [], []
    for occupancy in product((False, True), repeat=8):
        u = tuple(a for a in range(8) if occupancy[a])
        x, y, z = (frozenset(a for a in u if (a >> bit) & 1) for bit in range(3))
        rows = tuple(tuple(ordinary(s, u, a, b) for s in SYMBOLS)
                     for a, b in ((x, y), (y, z), (x, z)))
        ordinary_rows.append(rows)
        if all(a and len(a) < len(u) for a in (x, y, z)):
            proper_rows.append(rows)
        for s in SYMBOLS:
            p = d.Proposition.parse(s)
            expected = ordinary(s, u, x, y)
            assert p.holds(u, x, y) == expected
            assert p.contradictory().holds(u, x, y) != expected
            assert p.contrary_term('left').holds(u, set(u) - x, y) == expected
            assert p.contrary_term('right').holds(u, x, set(u) - y) == expected
    proper, unrestricted = entailments(proper_rows), entailments(ordinary_rows)
    assert len(proper_rows) == 193
    categories = {'universal': 0, 'particular': 0, 'strengthened': 0}
    valid_without_existence = 0
    for s, t in product(SYMBOLS, repeat=2):
        r = d.symbolic_inference(d.Proposition.parse(s), d.Proposition.parse(t))
        if r is None:
            assert not proper[s, t], (s, t, proper[s, t])
            continue
        assert str(r) in proper[s, t], (s, t, str(r))
        is_universal = lambda v: v in SYMBOLS[:4]
        kind = ('universal' if is_universal(str(r)) else 'strengthened'
                if is_universal(s) and is_universal(t) else 'particular')
        categories[kind] += 1
        valid_without_existence += str(r) in unrestricted[s, t]
    assert categories == {'universal': 8, 'particular': 16, 'strengthened': 8}
    assert valid_without_existence == 24

    # Source p.95 lower-right table prints '(.(' as conclusion; p.94 gives ').)'.
    # This model refutes that printed conclusion while all terms and complements exist.
    u, x, y, z = {0, 1, 2}, {0}, {0, 1}, {0, 2}
    assert ordinary('))', u, x, y) and ordinary('(.)', u, y, z)
    assert not ordinary('(.(', u, x, z)
    assert ordinary(').)', u, x, z)
    assert str(d.symbolic_inference(d.Proposition.parse('))'), d.Proposition.parse('(.)'))) == ').)'

    ex_rows = []
    for multiplicity in product(range(3), repeat=8):
        objects = [(a, k) for a in range(8) for k in range(multiplicity[a])]
        x, y, z = (frozenset(o for o in objects if (o[0] >> bit) & 1) for bit in range(3))
        if not all((x, y, z)):
            continue
        row = tuple(tuple(exemplar(s, a, b) for s in SYMBOLS)
                    for a, b in ((x, y), (y, z), (x, z)))
        ex_rows.append(row)
        for a, b in ((x, y), (y, z), (x, z)):
            for s in SYMBOLS:
                assert d.exemplar_holds(d.Proposition.parse(s), a, b) == exemplar(s, a, b)
    semantic = entailments(ex_rows)
    licensed = common = 0
    for s, t in product(SYMBOLS, repeat=2):
        p, q = d.Proposition.parse(s), d.Proposition.parse(t)
        r = d.exemplar_inference(p, q)
        if r is None:
            assert not semantic[s, t]
        else:
            assert str(r) in semantic[s, t]
            licensed += 1
            common += r == d.symbolic_inference(p, q)
    assert (len(ex_rows), licensed, common) == (6342, 36, 21)

    # Dependency controls: a selected X may depend on the universally selected Y.
    x, y = (0, 1), (2, 3)
    matching = {(0, 2), (1, 3)}
    assert exemplar('((', x, y, matching)
    assert not any(all((a, b) in matching for b in y) for a in x)
    assert not exemplar(').)', x, y, matching)
    assert all(any((a, b) not in matching for b in y) for a in x)
    for mask in range(16):
        r = {e for i, e in enumerate(product(x, y)) if mask & (1 << i)}
        for s in SYMBOLS:
            assert d.exemplar_holds(d.Proposition.parse(s), x, y, r) == exemplar(s, x, y, r)
    RESULTS['symbols'] = {'proper_occupancy_models': 193, 'all_occupancy_models': 256,
                          'contrary_rules': categories, 'valid_without_existence': 24,
                          'nonempty_exemplar_models': 6342, 'exemplar_rules': 36,
                          'shared_symbolic_schemas': 21, 'p95_print_counterexample': 'verified',
                          'mixed_quantifier_dependency_controls': 'passed'}


def relations(a, b):
    edges = tuple(product(range(a), range(b)))
    return [frozenset(e for k, e in enumerate(edges) if mask & (1 << k))
            for mask in range(1 << len(edges))]


def boolean_product(r, s, a, b, c):
    # Independent adjacency matrix multiplication with integer path counts.
    counts = [[sum(int((i, j) in r) * int((j, k) in s) for j in range(b))
               for k in range(c)] for i in range(a)]
    return frozenset((i, k) for i in range(a) for k in range(c) if counts[i][k])


def check_relations():
    pairs = 0
    for r, s in product(relations(2, 3), relations(3, 2)):
        expected = boolean_product(r, s, 2, 3, 2)
        assert d.compose(r, s) == expected
        assert d.converse(expected) == d.compose(d.converse(s), d.converse(r))
        pairs += 1
    for r in relations(3, 3):
        expected = boolean_product(r, r, 3, 3, 3) <= r
        assert d.transitive(r) == expected == d.transitive(d.converse(r))
        assert d.symmetric(r) == all(((i, j) in r) == ((j, i) in r)
                                     for i, j in product(range(3), repeat=2))
    rs = relations(2, 2)
    for r, s, t in product(rs, repeat=3):
        assert d.compose(d.compose(r, s), t) == d.compose(r, d.compose(s, t))
    bound_cases = degree_vectors = 0
    for a, b in product(range(1, 6), range(6)):
        minima = {}
        for incoming_degrees in product(range(a + 1), repeat=b):
            total = sum(incoming_degrees)
            common = incoming_degrees.count(a)
            minima[total] = min(minima.get(total, b + 1), common)
            degree_vectors += 1
        for edges, minimum in minima.items():
            assert d.common_target_lower_bound(a, b, edges) == minimum
            bound_cases += 1
    RESULTS['relations'] = {'rectangular_composition_pairs': pairs,
                            'three_object_relations': 512, 'associativity_triples': 4096,
                            'degree_vectors': degree_vectors, 'sharp_bound_cases': bound_cases}


def compositions(total, parts):
    if parts == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for rest in compositions(total - first, parts - 1):
                yield (first,) + rest


def require_rejection(call):
    try:
        call()
    except ValueError:
        return
    raise AssertionError('Expected undefined evidence to be rejected')


def check_testimony():
    # Source P[report][actual] has columns summing to one. Do not reset it as rows.
    priors = list(compositions(3, 3))
    source_columns = list(compositions(2, 3))
    posterior_checks = impossible_reports = 0
    for prior_counts in priors:
        prior = tuple(F(c, 3) for c in prior_counts)
        for columns in product(source_columns, repeat=3):
            P = tuple(tuple(F(columns[q][p], 2) for q in range(3)) for p in range(3))
            C = tuple(tuple(P[p][q] for p in range(3)) for q in range(3))
            # Integer joint counts have total mass 3*2, independent of Bayes code.
            joint_counts = [[prior_counts[q] * columns[q][p] for q in range(3)] for p in range(3)]
            assert d.report_distribution(prior, C) == tuple(F(sum(row), 6) for row in joint_counts)
            assert d.general_credibility(prior, C) == F(sum(joint_counts[k][k] for k in range(3)), 6)
            for report in range(3):
                total = sum(joint_counts[report])
                if total:
                    oracle = tuple(F(v, total) for v in joint_counts[report])
                    assert d.posterior(prior, C, report) == oracle
                    posterior_checks += 1
                else:
                    require_rejection(lambda: d.posterior(prior, C, report))
                    impossible_reports += 1
                denial = [sum(joint_counts[p][q] for p in range(3) if p != report) for q in range(3)]
                if sum(denial):
                    assert d.denial_posterior(prior, C, report) == tuple(F(v, sum(denial)) for v in denial)
                else:
                    require_rejection(lambda: d.denial_posterior(prior, C, report))

    # Every partition of a three-element alphabet, with independently coarsened joint mass.
    partitions = (((0, 1, 2),), ((0,), (1, 2)), ((1,), (0, 2)),
                  ((2,), (0, 1)), ((0,), (1,), (2,)))
    prior = (F(1, 6), F(1, 3), F(1, 2))
    C = ((F(1, 2), F(1, 3), F(1, 6)), (F(1, 5), F(7, 10), F(1, 10)),
         (F(3, 10), F(1, 10), F(3, 5)))
    joint = {(q, p): prior[q] * C[q][p] for q, p in product(range(3), repeat=2)}
    aggregate_checks = 0
    for states, reports in product(partitions, repeat=2):
        gp, gc = d.aggregate_model(prior, C, states, reports)
        for ri, group in enumerate(reports):
            masses = [sum(joint[q, p] for q in sg for p in group) for sg in states]
            assert d.posterior(gp, gc, ri) == tuple(v / sum(masses) for v in masses)
            aggregate_checks += 1
    # A nonsquare channel is supported; credibility alone requires matched alphabets.
    nonsquare = ((F(1, 2), F(1, 2)), (F(1), F(0)), (F(1, 4), F(3, 4)))
    assert d.posterior(prior, nonsquare, 0) == (F(2, 13), F(8, 13), F(3, 13))

    symmetric_checks = symmetric_impossible = 0
    for n, v, accuracy in product(range(2, 10), (F(0), F(1, 100), F(1, 10), F(1, 2), F(1)),
                                  (F(0), F(1, 4), F(1, 2), F(3, 4), F(1))):
        target_mass = v * accuracy
        other_mass = (1 - v) * (1 - accuracy) / (n - 1)
        if target_mass + other_mass:
            expected = target_mass / (target_mass + other_mass)
            assert d.symmetric_credibility(v, n, accuracy) == expected
            symmetric_checks += 1
        else:
            require_rejection(lambda: d.symmetric_credibility(v, n, accuracy))
            symmetric_impossible += 1

    # p.120 speaking-selection boundary: condition the prior consistently.
    fair = (F(1, 2),) * 2
    speaking = (F(1, 10), F(9, 10))
    given_speech = (fair, fair)
    # Labels: report 0, report 1, silence.
    with_silence = ((F(1, 20), F(1, 20), F(9, 10)),
                    (F(9, 20), F(9, 20), F(1, 10)))
    selected_prior = d.condition(fair, speaking)
    assert d.posterior(fair, with_silence, 0) == selected_prior
    assert d.posterior(selected_prior, given_speech, 0) == selected_prior
    assert d.posterior(fair, given_speech, 0) != selected_prior

    biased_valid = biased_rejected = 0
    for counts in compositions(4, 3):
        beliefs = tuple(F(c, 4) for c in counts)
        for accuracy in product((F(0), F(1, 2), F(1)), repeat=3):
            if any(beliefs[q] == 1 and accuracy[q] < 1 for q in range(3)):
                require_rejection(lambda: d.biased_channel(beliefs, accuracy))
                biased_rejected += 1
                continue
            expected_columns = []
            for q in range(3):
                residual = 1 - accuracy[q]
                expected_columns.append(tuple(accuracy[q] if p == q else F(0)
                    if residual == 0 else residual * beliefs[p] / sum(beliefs[j] for j in range(3) if j != q)
                    for p in range(3)))
            result = d.biased_channel(beliefs, accuracy)
            assert result == tuple(expected_columns)
            biased_valid += 1
        no_information = d.biased_channel(beliefs, beliefs)
        for k in range(3):
            if beliefs[k]:
                assert d.posterior(prior, no_information, k) == prior

    # Raw joint enumeration through a rectangular, two-stage latent model.
    J = ((F(1, 3), F(2, 3)), (F(3, 4), F(1, 4)), (F(1, 2), F(1, 2)))
    S = ((F(1, 2), F(1, 4), F(1, 4), F(0)), (F(0), F(1, 4), F(1, 4), F(1, 2)))
    composed = d.compose_channels(J, S)
    for k in range(4):
        paths = {(q, b): prior[q] * J[q][b] * S[b][k] for q in range(3) for b in range(2)}
        masses = [sum(paths[q, b] for b in range(2)) for q in range(3)]
        assert d.posterior(prior, composed, k) == tuple(v / sum(masses) for v in masses)
    # Outside the Markov model, T -> B -> R factorization need not hold.
    fair = (F(1, 2),) * 2
    uninformative = (fair, fair)
    assert d.posterior(fair, d.compose_channels(uninformative, uninformative), 0) == fair
    # Countermodel: B is a fair independent coin, but R=T deterministically.
    true_joint = {(t, b, t): F(1, 4) for t, b in product(range(2), repeat=2)}
    masses = [sum(v for (t, b, r), v in true_joint.items() if t == a and r == 0) for a in range(2)]
    assert tuple(v / sum(masses) for v in masses) == (F(1), F(0))

    # p.125 targeted statement with imperfect judgment, not just identity judgment.
    judgment = ((F(1, 2), F(1, 3), F(1, 6)), (F(1, 5), F(7, 10), F(1, 10)),
                (F(3, 10), F(1, 10), F(3, 5)))
    targeted_checks = 0
    for target, kappa in product(range(3), (F(0), F(1, 4), F(1, 2), F(1))):
        composed = d.compose_channels(judgment, d.targeted_statement_channel(3, target, kappa))
        likelihood = tuple(kappa + (1 - kappa) * judgment[q][target] for q in range(3))
        masses = [prior[q] * likelihood[q] for q in range(3)]
        expected = tuple(v / sum(masses) for v in masses)
        assert d.posterior(prior, composed, target) == expected
        baseline = prior[target] * judgment[target][target] / sum(prior[q] * judgment[q][target] for q in range(3))
        assert min(baseline, prior[target]) <= expected[target] <= max(baseline, prior[target])
        targeted_checks += 1

    # Different witness alphabets and likelihoods; enumerate full report pairs.
    witness_checks = 0
    for r1, r2 in product(range(3), range(2)):
        masses = [prior[q] * C[q][r1] * nonsquare[q][r2] for q in range(3)]
        assert d.multiple_witnesses(prior, (C, nonsquare), (r1, r2)) == tuple(v / sum(masses) for v in masses)
        witness_checks += 1
    accurate = ((F(9, 10), F(1, 10)), (F(1, 10), F(9, 10)))
    independent = d.multiple_witnesses(fair, (accurate, accurate), (0, 0))[0]
    copy_joint = {(t, r, r): fair[t] * accurate[t][r] for t, r in product(range(2), repeat=2)}
    masses = [sum(v for (t, r1, r2), v in copy_joint.items() if t == q and r1 == r2 == 0) for q in range(2)]
    copied = masses[0] / sum(masses)
    assert (independent, copied) == (F(81, 82), F(9, 10))
    RESULTS['testimony'] = {'source_orientation': 'report rows, actual-event columns; input explicitly transposed',
        'ternary_prior_channel_cases': len(priors) * len(source_columns) ** 3,
        'defined_ternary_posteriors': posterior_checks, 'zero_evidence_rejections': impossible_reports,
        'partition_posterior_checks': aggregate_checks, 'valid_bias_channels': biased_valid,
        'uniform_error_formula_checks': symmetric_checks,
        'uniform_error_zero_evidence_rejections': symmetric_impossible,
        'speaking_selection_countermodel': 'verified',
        'invalid_bias_channels_rejected': biased_rejected, 'rectangular_latent_reports': 4,
        'targeted_falsehood_checks': targeted_checks, 'mixed_alphabet_witness_reports': witness_checks,
        'markov_countermodel': 'verified', 'independent_witness_posterior': str(independent),
        'copied_witness_posterior': str(copied)}


def main():
    check_symbols()
    check_relations()
    check_testimony()
    RESULTS['status'] = 'PASS'
    RESULTS['scope'] = 'Specified finite teaching semantics; not a formalization of every historical claim.'
    print(json.dumps(RESULTS, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
