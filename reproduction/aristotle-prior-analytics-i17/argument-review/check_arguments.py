"""Independent theorem-oriented finite checks; no author demo/model import.

Set intersections/unions encode predicate truth profiles. These checks supplement
manual arbitrary-domain proofs; they do not prove historical modal syllogistic.
"""
from itertools import product
import json


def require(value, label):
    if not value:
        raise RuntimeError(label)


def subsets(n):
    d = tuple(range(n))
    return tuple(frozenset(d[i] for i in range(n) if bits & (1 << i))
                 for bits in range(2 ** n))


def classify(worlds, subject, form, mode, actual=0):
    domain = set().union(*worlds, subject)
    positive = form in ('A', 'I')
    signed = worlds if positive else tuple(domain - x for x in worlds)
    if mode == 'actual':
        eligible = signed[actual]
    elif mode == 'necessary':
        eligible = set.intersection(*(set(x) for x in signed))
    elif mode == 'possible':
        eligible = set().union(*signed)
    elif mode == 'contingent':
        eligible = set().union(*signed) - set.intersection(*(set(x) for x in signed))
    else:
        raise ValueError(mode)
    return subject <= eligible if form in ('A', 'E') else bool(subject & eligible)


def profiles():
    counts = {'configurations': 0, 'checks': 0, 'both_existential_branches': 0,
              'objectwise_without_common_positive_world': 0,
              'empty_subject_configurations': 0}
    for n, w in product(range(1, 4), repeat=2):
        d = frozenset(range(n))
        for worlds in product(subsets(n), repeat=w):
            necessary = set.intersection(*(set(x) for x in worlds))
            impossible = d - set().union(*worlds)
            contingent = d - necessary - impossible
            for s in subsets(n):
                for actual in range(w):
                    counts['configurations'] += 1
                    def check(value, label):
                        require(value, label)
                        counts['checks'] += 1
                    check(not (necessary & impossible), 'same object cannot be fixed both ways')
                    check(necessary | impossible | contingent == d, 'profile trichotomy covers domain')
                    check(not (s <= contingent) == bool(s & necessary or s & impossible), 'not all contingent splits existentially')
                    check(not bool(s & contingent) == (s <= (necessary | impossible)), 'not some contingent is all fixed')
                    for a, b in [('A', 'E'), ('I', 'O')]:
                        check(classify(worlds, s, a, 'contingent', actual) == classify(worlds, s, b, 'contingent', actual), 'quality equality')
                    for f in 'AEIO':
                        k = classify(worlds, s, f, 'contingent', actual)
                        m = classify(worlds, s, f, 'possible', actual)
                        t = classify(worlds, s, f, 'actual', actual)
                        nn = classify(worlds, s, f, 'necessary', actual)
                        check(not nn or t, 'necessary entails actual')
                        check(not t or m, 'actual entails possible')
                        check(not k or m, 'contingent entails signed possible')
                    if s:
                        check(not (s <= contingent) or bool(s & contingent), 'nonempty all to some')
                    else:
                        counts['empty_subject_configurations'] += 1
                        check(s <= contingent and not bool(s & contingent), 'empty all and no some')
                    if s & necessary and s & impossible:
                        counts['both_existential_branches'] += 1
                    if s <= contingent and not any(s <= world for world in worlds):
                        counts['objectwise_without_common_positive_world'] += 1
    return counts


def unconstrained_endpoints():
    """For any nonempty rigid B,C, toggle A to meet every premise quality."""
    counts = {'rigid_endpoint_pairs': 0, 'premise_checks': 0, 'candidate_refutations': 0}
    for n in range(1, 5):
        d = frozenset(range(n))
        for b, c in product(subsets(n)[1:], repeat=2):
            counts['rigid_endpoint_pairs'] += 1
            a = (b | c, frozenset())
            for f in 'AEIO':
                require(classify(a, b, f, 'contingent'), 'free B premise')
                require(classify(a, c, f, 'contingent'), 'free C premise')
                counts['premise_checks'] += 2
    b, c = frozenset({0}), frozenset({1})
    families = ((b, c), (c, c))
    ledger = []
    for f, g in product('AEIO', repeat=2):
        for mode, conclusion in product(('actual', 'necessary', 'possible', 'contingent'), 'AEIO'):
            failures = []
            for index, (b, c) in enumerate(families):
                a = (b | c, frozenset())
                require(classify(a, b, f, 'contingent') and classify(a, c, g, 'contingent'), 'ledger premise')
                if not classify((b, b), c, conclusion, mode):
                    failures.append(('D', 'S')[index])
            require(failures, 'every candidate has explicit countermodel')
            counts['candidate_refutations'] += 1
            ledger.append([f, g, mode, conclusion, failures])
    return counts, ledger


def hand_cases():
    h, s = 0, 1
    b = (frozenset({h}),) * 2
    a = (frozenset({h, s}), frozenset({s}))
    require(classify(a, b[0], 'E', 'contingent'), 'section5 forward')
    require(not classify(b, a[0], 'E', 'contingent'), 'section5 reverse failure')
    reverse_subject = frozenset({s})
    a_negative_only = (reverse_subject, frozenset({h, s}))
    require(classify(a_negative_only, b[0], 'E', 'contingent'), 'negative-only forward')
    require(not classify(b, reverse_subject, 'I', 'necessary'), 'necessary positive branch absent')
    require(classify(b, reverse_subject, 'O', 'necessary'), 'necessary negative branch present')
    alternating = (frozenset({0}), frozenset({1}))
    full = frozenset({0, 1})
    require(classify(alternating, full, 'A', 'contingent'), 'each object contingent')
    require(not any(full <= w for w in alternating), 'no common positive witness')
    require(not any(full.isdisjoint(w) for w in alternating), 'no common negative witness')
    mixed = (frozenset({0}),) * 2
    require(not classify(mixed, full, 'I', 'contingent'), 'no contingent individual')
    require(not classify(mixed, full, 'A', 'necessary'), 'not all fixed positive')
    require(not classify(mixed, full, 'E', 'necessary'), 'not all fixed negative')
    return {'checks': 11, 'purpose': 'sections4.5/5/8.1 and exercises5/7-11/18'}


if __name__ == '__main__':
    counts, ledger = unconstrained_endpoints()
    print(json.dumps({'scope': 'independent finite set reconstruction; arbitrary-domain proof manually reviewed separately',
                      'profiles': profiles(), 'unconstrained_endpoints': counts,
                      'endpoint_ledger': ledger, 'hand_cases': hand_cases()}, ensure_ascii=False, indent=2))
