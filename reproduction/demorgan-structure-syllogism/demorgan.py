"""Original educational reconstruction of selected De Morgan (1847) arguments.

Python standard library only. Sets are finite; probabilities are exact rational
numbers. Product weights are an explicitly chosen pre-conditioning model, not a
rule that reconstructs an arbitrary joint law from its marginals.
"""
from fractions import Fraction
from itertools import combinations, product
from math import prod

PROPOSITIONS = ('A', 'O', 'a', 'o', 'E', 'I', 'e', 'i')
RELATIONS = ('D_sub', 'D', 'D_super', 'C_sub', 'C', 'C_super', 'P')


def subsets(universe):
    """Yield every subset once; element multiplicity is not retained."""
    items = tuple(sorted(frozenset(universe)))
    for mask in range(1 << len(items)):
        yield frozenset(x for i, x in enumerate(items) if mask & (1 << i))


def _sets(universe, x, y):
    u, x, y = map(frozenset, (universe, x, y))
    if not (x <= u and y <= u):
        raise ValueError('Terms must be subsets of the stated universe')
    return u, x, y


def propositions(universe, x, y):
    """p.381-382 in modern set semantics; empty terms ARE allowed here.

    Existential import is an additional domain restriction, not hidden in A/E.
    Lowercase a/e/i/o means complementing BOTH terms, not negating a sentence.
    """
    u, x, y = _sets(universe, x, y)
    return {'A': x <= y, 'O': bool(x - y),
            'a': y <= x, 'o': bool(y - x),
            'E': not bool(x & y), 'I': bool(x & y),
            'e': x | y == u, 'i': bool(u - (x | y))}


def proper_terms(universe, *terms):
    u = frozenset(universe)
    frozen = tuple(map(frozenset, terms))
    return all(t < u and bool(t) for t in frozen)


def relation_matches(universe, x, y):
    """p.408 definitions, without silently enforcing the nondegenerate domain."""
    p = propositions(universe, x, y)
    return {'D': p['A'] and p['a'], 'D_sub': p['A'] and p['o'],
            'D_super': p['a'] and p['O'], 'C': p['E'] and p['e'],
            'C_sub': p['E'] and p['i'], 'C_super': p['e'] and p['I'],
            'P': p['I'] and p['O'] and p['i'] and p['o']}


def relation(universe, x, y):
    """Classify two nonempty, proper terms into the seven p.408 relations."""
    u, x, y = _sets(universe, x, y)
    if not proper_terms(u, x, y):
        raise ValueError('Seven-way classification requires nonempty proper terms')
    matches = [name for name, holds in relation_matches(u, x, y).items() if holds]
    if len(matches) != 1:
        raise AssertionError('Seven-way classification is not unique')
    return matches[0]


def atom_models():
    """All 256 occupancy patterns of the eight X/Y/Z membership atoms.

    One representative per occupied atom; not an enumeration of all cardinalities
    or of all infinite models. Useful for predicates depending only on emptiness.
    """
    for occupied in subsets(range(8)):
        yield (occupied,
               frozenset(i for i in occupied if i & 4),
               frozenset(i for i in occupied if i & 2),
               frozenset(i for i in occupied if i & 1))


def composition_from_atoms():
    """Possibilities for X:Z, with premises X:Y and Z:Y (p.408 orientation)."""
    result = {(r, s): set() for r in RELATIONS for s in RELATIONS}
    count = 0
    for u, x, y, z in atom_models():
        if proper_terms(u, x, y, z):
            result[relation(u, x, y), relation(u, z, y)].add(relation(u, x, z))
            count += 1
    return {k: frozenset(v) for k, v in result.items()}, count


def overlap_lower_bound(m, n):
    """p.384: fraction of common middle-term individuals, clipped at zero."""
    m, n = probability(m), probability(n)
    return max(Fraction(0), m + n - 1)


def count_overlap_lower_bound(total, first, second):
    """p.406 effective-number principle; cardinalities, not mappings with repeats."""
    if any(type(v) is not int for v in (total, first, second)):
        raise TypeError('Counts must be integers')
    if total < 0 or not (0 <= first <= total and 0 <= second <= total):
        raise ValueError('Invalid population or selected counts')
    return max(0, first + second - total)


def probability(value):
    if not isinstance(value, (int, Fraction)):
        raise TypeError('Use an int or Fraction; binary floats are intentionally rejected')
    value = Fraction(value)
    if not 0 <= value <= 1:
        raise ValueError('Probability must lie in [0,1]')
    return value


def normalize(weights):
    """Normalize a finite nonnegative exact-rational measure, rejecting zero mass."""
    converted = {}
    for key, value in weights.items():
        if not isinstance(value, (int, Fraction)):
            raise TypeError('Weights must be exact rational numbers')
        value = Fraction(value)
        if value < 0:
            raise ValueError('Negative weight')
        converted[key] = value
    total = sum(converted.values(), Fraction(0))
    if total == 0:
        raise ValueError('Conditioning event has zero mass')
    return {key: value / total for key, value in converted.items()}


def conditional_product(factors, allowed):
    """p.405 as conditioning a chosen independent product law on allowed states.

    allowed receives an outcome tuple. Returned marginal probabilities generally
    differ from input factor probabilities. Structural zeros alone do not justify
    the product model. An empty list of factors has one empty outcome of mass 1.
    """
    fs = []
    for factor in factors:
        f = {key: probability(value) for key, value in factor.items()}
        if sum(f.values(), Fraction(0)) != 1:
            raise ValueError('Every factor must sum to one')
        fs.append(f)
    weights = {state: prod((f[key] for f, key in zip(fs, state)), start=Fraction(1))
               for state in product(*(tuple(f) for f in fs)) if allowed(state)}
    return normalize(weights)


def bernoulli(p):
    p = probability(p)
    return {False: 1 - p, True: p}


def joint_testimony(probabilities):
    """pp.394-395: condition independent testimony flags on unanimous agreement.

    No testimonies returns 1/2 by an explicit neutral empty-product convention,
    not as a uniquely inferred conditional probability of an empty truth flag.
    """
    ps = tuple(map(probability, probabilities))
    return normalize({'true': prod(ps, start=Fraction(1)),
                      'false': prod((1-p for p in ps), start=Fraction(1))})['true']


def authority(testimony):
    """p.393 signed authority, in [-1,1], rather than a probability."""
    return 2 * probability(testimony) - 1


def biased_testimony(mu, mu_prime, lam):
    """p.396 first expression: an explicit mixture; lambda is an extra input."""
    mu, mu_prime, lam = map(probability, (mu, mu_prime, lam))
    if lam == 1:  # The unused independent branch need not be defined.
        return mu
    return lam * mu + (1-lam) * joint_testimony((mu, mu_prime))


def printed_biased_authority(mu, mu_prime, lam):
    """Literal p.396 SECOND expression, retained solely to audit its mismatch.

    Do not use this as a corrected formula. Its displayed numerator is
    a + a' - 2 lambda a' (1-a), rather than a + a' - lambda a' (1-a*a).
    """
    mu, mu_prime, lam = map(probability, (mu, mu_prime, lam))
    a, ap = authority(mu), authority(mu_prime)
    if 1 + a * ap == 0:
        raise ValueError('Printed denominator is zero')
    return (a + ap - 2 * lam * ap * (1-a)) / (1 + a * ap)


def independent_any(validities):
    """p.396: probability at least one succeeds, under independence."""
    ps = tuple(map(probability, validities))
    return 1 - prod((1-p for p in ps), start=Fraction(1))


def opposing_arguments(a, b):
    """p.397: product law conditioned on not both arguments proving opposites."""
    a, b = map(probability, (a, b))
    return normalize({'for': a * (1-b), 'against': b * (1-a),
                      'inconclusive': (1-a) * (1-b)})


def conclusion_probability(a, b, mu):
    """p.398: authority-weighted conclusion under the same compatibility model."""
    a, b, mu = map(probability, (a, b, mu))
    return normalize({'true': (1-b) * mu,
                      'false': (1-a) * (1-mu)})['true']


def hypothesis_weights(validities, testimonies):
    """pp.403-404 one-horn probabilities using unsimplified product weights.

    This avoids artificial division by zero in the odds/exponent expression at
    probability 0 or 1. An actually zero total remains an error.
    """
    aa, mm = tuple(map(probability, validities)), tuple(map(probability, testimonies))
    if len(aa) != len(mm) or not aa:
        raise ValueError('Need matching, nonempty lists')
    return normalize({i: mm[i] * prod(((1-aa[j])*(1-mm[j])
                                     for j in range(len(aa)) if j != i),
                                    start=Fraction(1)) for i in range(len(aa))})


def exactly_k(exponents, k):
    """p.404: normalize products over k-element subsets of finite weights."""
    es = tuple(exponents)
    if type(k) is not int or not 0 <= k <= len(es):
        raise ValueError('k must be an integer between zero and the number of cases')
    if any(not isinstance(e, (int, Fraction)) or e < 0 for e in es):
        raise ValueError('Exponents must be nonnegative exact rational weights')
    return normalize({s: prod((Fraction(es[i]) for i in s), start=Fraction(1))
                      for s in combinations(range(len(es)), k)})


def urn_example(factors=None):
    """p.405 original five allowed color combinations, with modern numeric inputs."""
    if factors is None:
        factors = ({'W': Fraction(1, 2), 'B': Fraction(1, 6), 'R': Fraction(1, 3)},
                   {'W': Fraction(2, 3), 'B': Fraction(1, 3)},
                   {'W': Fraction(3, 4), 'B': Fraction(1, 4)})
    allowed = {('W', 'W', 'B'), ('W', 'B', 'W'), ('W', 'B', 'B'),
               ('R', 'B', 'W'), ('R', 'W', 'B')}
    return conditional_product(factors, lambda state: state in allowed)


def random_subset_disjoint(total, first, second):
    """p.385: independent uniform subsets of fixed sizes; hypergeometric zero overlap."""
    from math import comb
    count_overlap_lower_bound(total, first, second)  # Validate integer counts.
    if first + second > total:
        return Fraction(0)
    return Fraction(comb(total-first, second), comb(total, second))


def interval_overlap_cdf(first, second, threshold=Fraction(0)):
    """pp.386-387: independent uniformly positioned intervals in [0,1].

    Returns P(overlap <= threshold); for 0<threshold<min(lengths), this also
    equals the strict CDF. At max overlap there can be an atom (containment).
    Nondegenerate lengths 0<first,second<1 avoid a zero-area placement domain.
    """
    first, second, threshold = map(probability, (first, second, threshold))
    if not (0 < first < 1 and 0 < second < 1):
        raise ValueError('Lengths must be strictly between zero and one')
    if threshold >= min(first, second):
        return Fraction(1)
    gap = max(Fraction(0), 1-first-second+threshold)
    return gap * gap / ((1-first)*(1-second))


def averaged_authority(r, prior='uniform'):
    """p.401 average of r*mu/(r*mu+1-mu), returned as a float.

    Closed forms are evaluated with 100-digit stdlib Decimal intermediates to
    avoid near-one cancellation and large-r float overflow. This is numerical,
    unlike the exact-rational core. r=1 uses the continuous limit. The chosen
    density averages normalized answers, not necessarily a generative hyperprior.
    """
    from decimal import Decimal, localcontext
    from math import isfinite
    r = float(r)
    if not isfinite(r) or r <= 0:
        raise ValueError('Relative argument testimony r must be positive and finite')
    if prior not in ('uniform', 'beta22'):
        raise ValueError('Unknown prior')
    if r == 1:
        return 0.5
    with localcontext() as ctx:
        ctx.prec = 100
        q = Decimal(str(r))
        if prior == 'uniform':
            value = q/(q-1) * (1-q.ln()/(q-1))
        else:
            value = q/(q-1)**4 * (6*q*q.ln()+2+3*q-6*q*q+q**3)
        return float(value)


def averaged_authority_quadrature(r, prior='uniform', panels=20000):
    """Independent composite Simpson oracle, with fsum; no symbolic dependency.

    Used only for moderate r in tests (0.1 to 10). Fixed panels do NOT certify
    precision for extreme r, whose integrands can have very thin boundary layers.
    """
    from math import fsum, isfinite
    r = float(r)
    if not isfinite(r) or r <= 0 or prior not in ('uniform', 'beta22'):
        raise ValueError('Need positive finite r and a supported prior')
    if type(panels) is not int or panels <= 0 or panels % 2:
        raise ValueError('Simpson panels must be a positive even integer')
    def f(mu):
        density = 1 if prior == 'uniform' else 6*mu*(1-mu)
        return density * r*mu/(r*mu+1-mu)
    return (f(0)+f(1)+fsum((4 if i % 2 else 2)*f(i/panels)
                          for i in range(1, panels))) / (3*panels)


def syllogism_census():
    """pp.387-392 finite atom audit: XY, ZY premises; XZ conclusion.

    Select strongest single proposition(s), then remove premise pairs for which
    one premise can be strictly weakened without losing that conclusion. This is
    a model audit, not a machine-checked proof of the paper's full system.
    """
    rows = [(propositions(u, x, y), propositions(u, z, y), propositions(u, x, z))
            for u, x, y, z in atom_models() if proper_terms(u, x, y, z)]
    pair_truths = [p for p, _, _ in rows]
    implies = {(p, q): all(not row[p] or row[q] for row in pair_truths)
               for p in PROPOSITIONS for q in PROPOSITIONS}
    strongest = {}
    for p, q in product(PROPOSITIONS, repeat=2):
        models = [r for a, b, r in rows if a[p] and b[q]]
        if not models:
            raise AssertionError('Unexpected inconsistent premise pair')
        conclusions = {c for c in PROPOSITIONS if all(r[c] for r in models)}
        strongest[p, q] = frozenset(c for c in conclusions
                                    if not any(d != c and implies[d, c]
                                               for d in conclusions))
    valid = {pair: cs for pair, cs in strongest.items() if cs}
    redundant = set()
    for (p, q), cs in valid.items():
        for w in PROPOSITIONS:
            if w != p and implies[p, w] and not implies[w, p] and strongest[w, q] == cs:
                redundant.add((p, q))
            if w != q and implies[q, w] and not implies[w, q] and strongest[p, w] == cs:
                redundant.add((p, q))
    minimal = {pair: cs for pair, cs in valid.items() if pair not in redundant}
    # Swapping X and Z exchanges the premise slots (and reverses the conclusion).
    counterpart_classes = {tuple(sorted((pair, pair[::-1]))) for pair in minimal}
    return {'premise_pairs': 64, 'concluding_pairs': len(valid),
            'redundant_pairs': sorted(''.join(p) for p in redundant),
            'minimal_directed': len(minimal), 'counterpart_classes': len(counterpart_classes),
            'strongest': {''.join(k): sorted(v) for k, v in valid.items()}}
