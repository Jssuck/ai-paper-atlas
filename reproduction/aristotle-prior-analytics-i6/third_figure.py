"""Modern finite-support semantics for the third figure; standard library only."""
from itertools import combinations, product
from functools import lru_cache
import json

TERMS = ('P', 'S', 'M')
BITS = {'P': 4, 'S': 2, 'M': 1}
QUANTIFIERS = ('A', 'E', 'I', 'O')
POLICIES = ('allow-empty', 'middle-nonempty', 'all-nonempty')
MOODS = {'Darapti': ('A','A','I'), 'Felapton': ('E','A','O'),
         'Disamis': ('I','A','I'), 'Datisi': ('A','I','I'),
         'Bocardo': ('O','A','O'), 'Ferison': ('E','I','O')}


def checked_support(support):
    if not isinstance(support, (tuple, list, set, frozenset)):
        raise TypeError('support must be a finite collection')
    if not support:
        raise ValueError('the domain must be nonempty')
    if any(type(t) is not int for t in support):
        raise TypeError('types must be integers, not booleans')
    if any(t < 0 or t > 7 for t in support):
        raise ValueError('types range from 0 to 7')
    if len(set(support)) != len(support):
        raise ValueError('a support must not duplicate types')
    return tuple(sorted(support))


def checked_q(q):
    if not isinstance(q, str):
        raise TypeError('quantifier must be a string')
    if q not in QUANTIFIERS:
        raise ValueError('quantifier must be A, E, I or O')
    return q


def checked_term(t):
    if not isinstance(t, str):
        raise TypeError('term must be a string')
    if t not in TERMS:
        raise ValueError('term must be P, S or M')
    return t


def checked_policy(policy):
    if not isinstance(policy, str):
        raise TypeError('policy must be a string')
    if policy not in POLICIES:
        raise ValueError('unknown existence policy')
    return policy


def _truth(q, x, y, support):
    common = any(t & BITS[x] and t & BITS[y] for t in support)
    outside = any(t & BITS[x] and not t & BITS[y] for t in support)
    return {'A': not outside, 'E': not common, 'I': common, 'O': outside}[q]


def truth(q, x, y, support):
    return _truth(checked_q(q), checked_term(x), checked_term(y), checked_support(support))


def _admissible(support, policy):
    required = () if policy == 'allow-empty' else ('M',) if policy == 'middle-nonempty' else TERMS
    return all(any(t & BITS[x] for t in support) for x in required)


def admissible(support, policy='allow-empty'):
    return _admissible(checked_support(support), checked_policy(policy))


@lru_cache(None)
def supports(policy='allow-empty'):
    checked_policy(policy)
    return tuple(s for n in range(1, 9) for s in combinations(range(8), n)
                 if _admissible(s, policy))


def premises(q, r, support):
    s = checked_support(support)
    return _truth(checked_q(q), 'M', 'P', s) and _truth(checked_q(r), 'M', 'S', s)


@lru_cache(None)
def countermodel(q, r, conclusion, policy='allow-empty'):
    checked_q(q); checked_q(r); checked_q(conclusion); checked_policy(policy)
    for s in supports(policy):
        if _truth(q, 'M', 'P', s) and _truth(r, 'M', 'S', s) and not _truth(conclusion, 'S', 'P', s):
            return s
    return None


def entails(q, r, conclusion, policy='allow-empty'):
    return countermodel(q, r, conclusion, policy) is None


def compress(objects):
    """Compress a nonempty sequence of (P, S, M) Boolean membership tuples."""
    if not isinstance(objects, (list, tuple)):
        raise TypeError('objects must be a sequence')
    if not objects:
        raise ValueError('the domain must be nonempty')
    out = set()
    for row in objects:
        if not isinstance(row, (list, tuple)) or len(row) != 3:
            raise ValueError('each row must contain P, S, M')
        if any(type(b) is not bool for b in row):
            raise TypeError('membership entries must be booleans')
        out.add(sum(BITS[x] for x, b in zip(TERMS, row) if b))
    return tuple(sorted(out))


def expand(support):
    return tuple(tuple(bool(t & BITS[x]) for x in TERMS) for t in checked_support(support))


def proof_witness(name, support):
    """Return a shared witness's membership type, not a general proof certificate."""
    if not isinstance(name, str):
        raise TypeError('mood name must be a string')
    if name not in MOODS:
        raise ValueError('unknown mood')
    s = checked_support(support)
    q, r, conclusion = MOODS[name]
    if not premises(q, r, s):
        raise ValueError('premises are not satisfied')
    if name in ('Darapti','Felapton') and not _admissible(s, 'middle-nonempty'):
        raise ValueError('this route needs a member of M')
    for t in s:
        if not t & BITS['M']:
            continue
        if name == 'Disamis' and not t & BITS['P']:
            continue
        if name in ('Datisi','Ferison') and not t & BITS['S']:
            continue
        if name == 'Bocardo' and t & BITS['P']:
            continue
        # The chosen member is carried through both premises, not reselected.
        if t & BITS['S'] and (bool(t & BITS['P']) == (conclusion == 'I')):
            return t
    raise RuntimeError('a valid route failed to produce its shared witness')


def report():
    policies = {}
    for policy in POLICIES:
        rows = []
        for q, r in product(QUANTIFIERS, repeat=2):
            valid = [c for c in QUANTIFIERS if entails(q, r, c, policy)]
            rows.append({'major': q, 'minor': r, 'valid_conclusions': valid,
                         'minimal_countermodels': {c: countermodel(q,r,c,policy) for c in QUANTIFIERS if c not in valid}})
        policies[policy] = {'support_count': len(supports(policy)), 'premise_pairs': rows}
    return {'semantics': 'major Q(M,P), minor R(M,S), conclusion C(S,P)',
            'type_bits': BITS, 'nonempty_domain': True,
            'scope': 'modern extensional AEIO fragment only; finite execution is not a general proof',
            'policies': policies}

if __name__ == '__main__':
    print(json.dumps(report(), ensure_ascii=False, indent=2))
