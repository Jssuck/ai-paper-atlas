"""Finite, exact teaching models for De Morgan's second memoir (1851).

Original source: printed pp.79–127, read 25 February 1850. These are modern
set/relation/probability representations, not a claim to formalize the paper.
Probability channels are stored [actual event][reported event], transposed
from De Morgan's report-first p_q notation (p.120). Only stdlib is required.
"""
from dataclasses import dataclass
from fractions import Fraction
from itertools import product


@dataclass(frozen=True)
class Proposition:
    """A normalized pair of parentheses with a parity bit for negative dots."""
    left: str
    right: str
    negative: bool = False

    def __post_init__(self):
        if self.left not in ('(', ')') or self.right not in ('(', ')'):
            raise ValueError('Parentheses must be ( or )')
        if type(self.negative) is not bool:
            raise TypeError('negative must be bool')

    @classmethod
    def parse(cls, text):
        if not isinstance(text, str) or len(text) < 2:
            raise ValueError('Expected a pair of parentheses separated only by dots')
        if any(c != '.' for c in text[1:-1]):
            raise ValueError('Only dots may separate the parentheses')
        return cls(text[0], text[-1], bool(len(text[1:-1]) % 2))

    def __str__(self):
        return self.left + ('.' if self.negative else '') + self.right

    @property
    def universal(self):
        return (self.left == self.right) != self.negative

    def contrary_term(self, side):
        """p.92: complement this term, reverse its parenthesis, toggle dot."""
        if side not in ('left', 'right'):
            raise ValueError('side must be left or right')
        opposite = {'(': ')', ')': '('}
        return Proposition(opposite[self.left] if side == 'left' else self.left,
                           opposite[self.right] if side == 'right' else self.right,
                           not self.negative)

    def contradictory(self):
        """Reverse both quantities and toggle copula, pp.92–93."""
        opposite = {'(': ')', ')': '('}
        return Proposition(opposite[self.left], opposite[self.right], not self.negative)

    def holds(self, universe, x, y):
        universe, x, y = frozenset(universe), frozenset(x), frozenset(y)
        if not x <= universe or not y <= universe:
            raise ValueError('Terms must be contained in the universe')
        return {
            '))': x <= y, '((': y <= x,
            ').(': not (x & y), '(.)': x | y == universe,
            '()': bool(x & y), ')(': bool(universe - x - y),
            '(.(': bool(x - y), ').)': bool(y - x),
        }[str(self)]


FORMS = tuple(Proposition.parse(s) for s in ('))', '((', ').(', '(.)', '()', ')(', '(.(', ').)'))


def symbolic_inference(first, second):
    """p.94 canonical conclusion, assuming nonempty proper X,Y,Z.

    Returns None when the printed canon licenses no conclusion. No semantic
    checks on concrete terms are done here. The existential strengthened cases
    require the documented domain assumption and fail on degenerate terms.
    """
    same_middle = first.right == second.left
    valid = ((first.universal or second.universal) if same_middle
             else (first.universal and second.universal))
    return (Proposition(first.left, second.right, first.negative != second.negative)
            if valid else None)


def atom_models(proper=True):
    """One representative per 3-term atomic-region occupancy pattern.

    All 256 subsets of the eight membership vectors are used. This is complete
    for emptiness-only finite set semantics, but discards sizes and probabilities.
    """
    for mask in range(256):
        universe = frozenset(i for i in range(8) if mask & (1 << i))
        terms = tuple(frozenset(i for i in universe if i & (1 << bit)) for bit in range(3))
        if not proper or all(term and term != universe for term in terms):
            yield universe, *terms


def compose(first, second):
    """R ; S = {(x,z): exists y, R(x,y) and S(y,z)}; first R, then S."""
    return frozenset((x, z) for x, y in first for middle, z in second if y == middle)


def converse(relation):
    return frozenset((y, x) for x, y in relation)


def transitive(relation):
    return compose(relation, relation) <= frozenset(relation)


def symmetric(relation):
    return converse(relation) == frozenset(relation)


def relational_term(relation, objects):
    """Objects related to something in objects; modern reading of 'head of'."""
    objects = frozenset(objects)
    return frozenset(x for x, y in relation if y in objects)


def all_some(relation, subjects, predicates):
    return all(any((x, y) in relation for y in predicates) for x in subjects)


def all_all(relation, subjects, predicates):
    return all((x, y) in relation for x in subjects for y in predicates)


def common_target_lower_bound(source_count, target_count, edge_count):
    """p.112 edge-count bound for targets related to ALL source instances.

    Non-common targets have at most source_count-1 incoming edges; this gives
    max(0, edge_count - (source_count-1)*target_count). Integers only.
    """
    for v in (source_count, target_count, edge_count):
        if type(v) is not int:
            raise TypeError('Counts must be integers')
    if source_count < 1 or target_count < 0 or not 0 <= edge_count <= source_count * target_count:
        raise ValueError('Invalid bipartite counts')
    return max(0, edge_count - (source_count - 1) * target_count)


def _probability(value):
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError('Use exact int or Fraction probabilities; floats are rejected')
    value = Fraction(value)
    if not 0 <= value <= 1:
        raise ValueError('Probability must be between zero and one')
    return value


def distribution(values):
    values = tuple(_probability(v) for v in values)
    if not values or sum(values) != 1:
        raise ValueError('A nonempty probability vector must sum to one')
    return values


def channel(rows):
    """Validate finite row-stochastic channel, actual state first."""
    rows = tuple(distribution(row) for row in rows)
    if not rows or any(len(row) != len(rows[0]) for row in rows):
        raise ValueError('Channel must be a nonempty rectangular matrix')
    return rows


def _index(index, size):
    if type(index) is not int or not 0 <= index < size:
        raise ValueError('Index out of range')


def condition(prior, likelihood):
    """Exact Bayes normalization; no zero-evidence default is invented."""
    prior = distribution(prior)
    likelihood = tuple(_probability(x) for x in likelihood)
    if len(prior) != len(likelihood):
        raise ValueError('Prior and likelihood dimensions differ')
    masses = tuple(v * l for v, l in zip(prior, likelihood))
    evidence = sum(masses)
    if not evidence:
        raise ValueError('Observed evidence has zero model probability')
    return tuple(m / evidence for m in masses)


def report_distribution(prior, reports):
    prior, reports = distribution(prior), channel(reports)
    if len(prior) != len(reports):
        raise ValueError('Prior and channel dimensions differ')
    return tuple(sum(v * row[k] for v, row in zip(prior, reports))
                 for k in range(len(reports[0])))


def posterior(prior, reports, reported):
    """p.120: return the FULL posterior, not merely credibility at index k."""
    reports = channel(reports)
    _index(reported, len(reports[0]))
    return condition(prior, (row[reported] for row in reports))


def denial_posterior(prior, reports, denied):
    """p.123 complement-report model: observe that the report is NOT k.

    This likelihood 1-C[event][k] is an assumption about the reporting protocol,
    not a general model of an independently elicited verbal denial.
    """
    reports = channel(reports)
    _index(denied, len(reports[0]))
    return condition(prior, (1 - row[denied] for row in reports))


def general_credibility(prior, reports):
    prior, reports = distribution(prior), channel(reports)
    if len(prior) != len(reports) or len(reports[0]) != len(prior):
        raise ValueError('Matching square state/report alphabet required')
    return sum(v * reports[i][i] for i, v in enumerate(prior))


def symmetric_channel(n, accuracy):
    """p.121: same accuracy; error is uniform over the OTHER n-1 labels."""
    if type(n) is not int or n < 2:
        raise ValueError('At least two event labels required')
    accuracy = _probability(accuracy)
    return channel(tuple(tuple(accuracy if actual == report else (1 - accuracy) / (n - 1)
                               for report in range(n)) for actual in range(n)))


def symmetric_credibility(v, n, accuracy):
    """p.121 closed expression for one event's prior mass v."""
    if type(n) is not int or n < 2:
        raise ValueError('At least two event labels required')
    v, accuracy = _probability(v), _probability(accuracy)
    numerator = v * accuracy
    denominator = numerator + (1 - v) * (1 - accuracy) / (n - 1)
    if not denominator:
        raise ValueError('Observed evidence has zero model probability')
    return numerator / denominator


def biased_channel(beliefs, accuracies):
    """pp.123–124: distribute mistakes proportional to witness beliefs lambda.

    C[q][p]=lambda[p]*(1-accuracy[q])/(1-lambda[q]) for p != q.
    A belief of one cannot distribute a positive error mass and is rejected.
    """
    beliefs = distribution(beliefs)
    accuracies = tuple(_probability(x) for x in accuracies)
    if len(beliefs) < 2 or len(beliefs) != len(accuracies):
        raise ValueError('Matching vectors with at least two states required')
    rows = []
    for q, a in enumerate(accuracies):
        if beliefs[q] == 1 and a != 1:
            raise ValueError('All alternative belief masses are zero')
        rows.append(tuple(a if p == q else (Fraction(0) if a == 1 else
                          beliefs[p] * (1 - a) / (1 - beliefs[q]))
                          for p in range(len(beliefs))))
    return channel(rows)


def compose_channels(judgment, statement):
    """p.124: actual -> believed -> reported; Markov conditional assumption."""
    judgment, statement = channel(judgment), channel(statement)
    if len(judgment[0]) != len(statement):
        raise ValueError('Intermediate dimensions differ')
    return channel(tuple(tuple(sum(judgment[a][b] * statement[b][r]
                                    for b in range(len(statement)))
                               for r in range(len(statement[0])))
                         for a in range(len(judgment))))


def targeted_statement_channel(n, target, bias):
    """p.125: preserve target belief; other beliefs report target with bias kappa."""
    if type(n) is not int or n < 2:
        raise ValueError('At least two event labels required')
    _index(target, n)
    bias = _probability(bias)
    return channel(tuple(tuple(Fraction(int(r == target)) if a == target else
                               (bias if r == target else 1 - bias if r == a else Fraction(0))
                               for r in range(n)) for a in range(n)))


def multiple_witnesses(prior, reports, observations):
    """p.125 product: witnesses CONDITIONALLY INDEPENDENT given actual state.

    Shared copying, collusion, common evidence, etc. require a joint likelihood.
    Empty observations return the prior. No independence is inferred from data.
    """
    prior = distribution(prior)
    reports, observations = tuple(reports), tuple(observations)
    if len(reports) != len(observations):
        raise ValueError('One observation per witness required')
    likelihood = [Fraction(1)] * len(prior)
    for c, observation in zip(reports, observations):
        c = channel(c)
        if len(c) != len(prior):
            raise ValueError('Witness state dimensions differ')
        _index(observation, len(c[0]))
        for actual in range(len(prior)):
            likelihood[actual] *= c[actual][observation]
    return condition(prior, likelihood)


def aggregate_model(prior, reports, state_groups, report_groups):
    """Modern audit: coarsen the SAME joint model, rather than reset accuracy.

    Every original state/report must occur exactly once. Positive group prior
    is required because a zero-mass group's conditional row is undetermined.
    """
    prior, reports = distribution(prior), channel(reports)
    if len(prior) != len(reports):
        raise ValueError('Prior and channel dimensions differ')
    groups = []
    for spec, size in ((state_groups, len(prior)), (report_groups, len(reports[0]))):
        spec = tuple(tuple(g) for g in spec)
        flat = [i for g in spec for i in g]
        if not spec or any(not g for g in spec) or any(type(i) is not int for i in flat):
            raise ValueError('Groups must be nonempty and contain integer indices')
        if sorted(flat) != list(range(size)):
            raise ValueError('Groups must partition the alphabet exactly once')
        groups.append(spec)
    states, outputs = groups
    grouped_prior = tuple(sum(prior[i] for i in g) for g in states)
    if any(not v for v in grouped_prior):
        raise ValueError('Cannot identify channel row of a zero-prior group')
    grouped_channel = channel(tuple(tuple(sum(prior[i] * reports[i][j]
                                  for i in g for j in h) / mass
                                  for h in outputs)
                                  for g, mass in zip(states, grouped_prior)))
    return grouped_prior, grouped_channel


def exemplar_holds(proposition, x, y, relation=None):
    """pp.100–102/112: explicitly selected exemplar reading.

    Default copula is identity. Affirmative mixed quantities mean forall-exists,
    with the universal term selected first even if printed on the right.
    Negative forms are the exact duals: exists-forall. This is NOT naive
    left-to-right quantification. For arbitrary relations the full inference
    canon additionally needs suitable copular laws; we do not assume them here.
    Empty terms use modern vacuous quantification, unlike the nonempty domain
    of the historical 36-case test.
    """
    x, y = tuple(x), tuple(y)
    if proposition.negative:
        return not exemplar_holds(proposition.contradictory(), x, y, relation)
    related = (lambda a, b: a == b) if relation is None else (lambda a, b: (a,b) in relation)
    form = str(proposition)
    if form == ')(':
        return all(related(a,b) for a in x for b in y)
    if form == '))':
        return all(any(related(a,b) for b in y) for a in x)
    if form == '((':
        return all(any(related(a,b) for a in x) for b in y)
    if form == '()':
        return any(related(a,b) for a in x for b in y)
    raise AssertionError('Unexpected affirmative form')


def exemplar_inference(first, second):
    """pp.101–102: one affirmative premise and one universal middle term.

    This is syntax, not an unrestricted theorem for arbitrary relations.
    Tested with identity and nonempty X,Y,Z; pp.106–113 distinguish laws needed
    when identity is replaced by another copula.
    """
    valid = ((not first.negative or not second.negative) and
             (first.right == '(' or second.left == ')'))
    return (Proposition(first.left, second.right, first.negative != second.negative)
            if valid else None)
