"""Finite pedagogical middle-term certificates, not an account of quick wit."""
from itertools import product


def subsets(universe):
    """Enumerate every subset of a finite, sortable set in a stable order."""
    items = sorted(universe)
    return [frozenset(x for x, included in zip(items, bits) if included)
            for bits in product((False, True), repeat=len(items))]


def verify_middle(universe, major, middle, minor):
    """Return separate extensional checks; no causal or psychological verdict.

    A=major, B=middle, C=minor. We require C nonempty for an explanatory
    certificate about an instantiated subject. This is our explicit policy,
    not a claim that modern universal implication has existential import.
    """
    u, a, b, c = map(frozenset, (universe, major, middle, minor))
    if not (a | b | c) <= u:
        raise ValueError('all predicates must be subsets of the declared universe')
    result = {'subject_exists': bool(c), 'minor_premise': c <= b,
              'major_premise': b <= a, 'conclusion': c <= a}
    result['certificate'] = (result['subject_exists'] and
                             result['minor_premise'] and result['major_premise'])
    return result


def eligible_middles(universe, major, minor, candidates):
    """Names passing verification in the supplied library, not all causes."""
    return [name for name, middle in candidates.items()
            if verify_middle(universe, major, middle, minor)['certificate']]


def exhaustive_counts(size=3):
    """A finite check of inclusion transitivity; not its general proof."""
    u = frozenset(range(size))
    sets = subsets(u)
    checked = accepted = failures = 0
    for a, b, c in product(sets, repeat=3):
        r = verify_middle(u, a, b, c)
        checked += 1
        accepted += r['certificate']
        failures += r['certificate'] and not r['conclusion']
    return {'universe_size': size, 'triples': checked,
            'certificates': accepted, 'soundness_failures': failures}


def examples():
    # Toy objects and stipulated extensions, not astronomical measurements.
    u = {'moon', 'panel', 'lamp'}
    a, c = {'moon', 'panel'}, {'moon'}
    library = {'sun_lit': {'moon', 'panel'}, 'singleton_fit': {'moon'},
               'empty': set(), 'wrong_subject': {'panel'},
               'too_wide': u}
    return u, a, c, library


def main():
    u, a, c, library = examples()
    print('Pedagogical finite model; no causal, knowledge, or speed certification.')
    print('eligible candidates:', eligible_middles(u, a, c, library))
    print('omitted-library result:', eligible_middles(u, a, c, {'empty': set()}))
    print('affirming-consequent counterexample:', verify_middle(u, a, {'panel'}, c))
    print('social counterexample: talking={visitor}, borrowing={} =>',
          verify_middle({'visitor'}, {'visitor'}, set(), {'visitor'}))
    print('enumeration:', exhaustive_counts())


if __name__ == '__main__':
    main()
