"""Finite extensional teaching model, not a causal or acoustic inference engine."""
from fractions import Fraction
from itertools import product


def powerset(universe):
    """Enumerate subsets of a finite iterable without duplicate elements."""
    items = tuple(sorted(set(universe)))
    return tuple(frozenset(x for x, yes in zip(items, bits) if yes)
                 for bits in product((False, True), repeat=len(items)))


def checked(universe, *extensions):
    u = frozenset(universe)
    values = tuple(frozenset(s) for s in extensions)
    if any(not s <= u for s in values):
        raise ValueError('extension outside declared universe')
    return u, values


def chain(universe, subject, middle, predicate):
    """C <= M <= A: sound extensional certificate; allows empty C."""
    _, (c, m, a) = checked(universe, subject, middle, predicate)
    return c <= m <= a


def candidates(universe, subject, predicate):
    """Search the entire finite powerset, not natural scientific explanations."""
    u, (c, a) = checked(universe, subject, predicate)
    return tuple(m for m in powerset(u) if chain(u, c, m, a))


def candidate_count(universe, subject, predicate):
    """Closed form, independently compared with exhaustive search."""
    _, (c, a) = checked(universe, subject, predicate)
    return 2 ** len(a - c) if c <= a else 0


def completions(universe, observed, middle_positive, predicate_positive):
    """All full extensions matching complete binary labels on observed points.

    Absence outside observed is unknown, not false. Labels within observed are
    complete; observed negatives are encoded by absence from positive sets.
    """
    u, (o, mp, ap) = checked(universe, observed, middle_positive, predicate_positive)
    if not mp <= o or not ap <= o:
        raise ValueError('positive label outside observed sample')
    return tuple((m, a) for m in powerset(u) for a in powerset(u)
                 if m & o == mp and a & o == ap)


TEACHING_PALETTE = frozenset((Fraction(2), Fraction(3, 2), Fraction(4, 3)))


def ratio_in_palette(high, low, palette=TEACHING_PALETTE):
    """An explicitly stipulated palette; not a law of consonance or perception."""
    if type(high) is not int or type(low) is not int:
        raise TypeError('positive integer inputs required')
    if low <= 0 or high <= 0 or high < low:
        raise ValueError('require high >= low > 0')
    ratio = Fraction(high, low)
    return ratio, ratio in palette


def exhaustive_summary(n=3):
    if type(n) is not int or n < 0 or n > 5:
        raise ValueError('demo supports integer domain sizes 0..5')
    u = frozenset(range(n))
    subsets = powerset(u)
    triples = valid = nonempty = soundness_failures = count_failures = 0
    for c, m, a in product(subsets, repeat=3):
        triples += 1
        if chain(u, c, m, a):
            valid += 1
            nonempty += bool(c)
            soundness_failures += not c <= a
    for c, a in product(subsets, repeat=2):
        count_failures += len(candidates(u, c, a)) != candidate_count(u, c, a)
    return dict(domain_size=n, triples=triples, valid_chains=valid,
                nonempty_subject_chains=nonempty,
                soundness_failures=soundness_failures,
                candidate_count_checks=len(subsets)**2,
                candidate_count_failures=count_failures)


def demo():
    import json
    u = frozenset(range(3))
    ms = candidates(u, {0}, {0, 1})
    print('C={0}; A={0,1}; candidate extensions:', [sorted(m) for m in ms])
    print('Existence of candidates:', bool(ms), '; unique extension:', len(ms) == 1)
    print('Causal status: NOT EVALUATED; distinct descriptions may share an extension.')
    worlds = completions(u, {0}, {0}, {0})
    good = sum(m <= a for m, a in worlds)
    counter = next((m, a) for m, a in worlds if not m <= a)
    print('One observed point: completions=', len(worlds), 'universal_true=', good,
          'universal_false=', len(worlds)-good)
    print('Countercompletion M,A:', sorted(counter[0]), sorted(counter[1]))
    for h, l in ((440, 220), (330, 220), (221, 220)):
        ratio, accepted = ratio_in_palette(h, l)
        print(f'Teaching palette only: {h}/{l} = {ratio}; member={accepted}')
    print(json.dumps(exhaustive_summary(), sort_keys=True))


if __name__ == '__main__':
    demo()
