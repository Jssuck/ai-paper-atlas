"""Original finite-set teaching reconstruction of Prior Analytics II.26.

No historical factual premises are certified. Empty classes are allowed, and
existential commitments are explicit. Bit masks represent subsets of range(n).
"""
import argparse
import json

ROUTES = ('upper_negative', 'lower_negative', 'upper_positive',
          'lower_positive', 'second_negative', 'first_particular')


def validate(n, *masks):
    if type(n) is not int or not 0 <= n <= 8:
        raise ValueError('n must be an integer between 0 and 8')
    if any(type(x) is not int or x < 0 or x >= 1 << n for x in masks):
        raise ValueError('each mask must be an integer subset of range(n)')


def subset(x, y):
    return x & ~y == 0


def propositions(n, a, b):
    """A/E/I/O, with B as subject and A as predicate."""
    validate(n, a, b)
    return {'A': subset(b, a), 'E': not bool(b & a),
            'I': bool(b & a), 'O': bool(b & ~a)}


def certificate(n, a, b, c, route):
    """Return premises, conclusion, and genuine rejection of target A/E.

    A route with false premises is not accepted, even if its conclusion happens
    to be true. Upper routes can conclude a universal without rejecting its
    opposite if B is empty. This distinction is part of the returned certificate.
    """
    validate(n, a, b, c)
    if route not in ROUTES:
        raise ValueError('unknown route')
    if route == 'upper_negative':
        premises, conclusion, target = [subset(b,c), not bool(c&a)], 'E', 'A'
    elif route == 'lower_negative':
        premises, conclusion, target = [subset(c,b), not bool(c&a), bool(c)], 'O', 'A'
    elif route == 'upper_positive':
        premises, conclusion, target = [subset(b,c), subset(c,a)], 'A', 'E'
    elif route == 'lower_positive':
        premises, conclusion, target = [subset(c,b), subset(c,a), bool(c)], 'I', 'E'
    elif route == 'second_negative':
        premises, conclusion, target = [subset(a,c), not bool(b&c)], 'E', 'A'
    else:
        premises, conclusion, target = [bool(b&c), subset(c,a)], 'I', 'E'
    truth = propositions(n,a,b)
    accepted = all(premises)
    return {'route':route, 'premises':premises, 'accepted':accepted,
            'conclusion':conclusion, 'conclusion_true':truth[conclusion],
            'target':target, 'target_true':truth[target],
            'rejects_target':accepted and not truth[target],
            'subject_nonempty':bool(b)}


def enumerate_models(max_n=4):
    validate(max_n)
    counts = {r:{'premises_hold':0, 'conclusion_failures':0,
                 'genuine_rejections':0, 'empty_subject_nonrejections':0}
              for r in ROUTES}
    worlds = 0
    square_failures = 0
    for n in range(max_n+1):
        for a in range(1 << n):
            for b in range(1 << n):
                p = propositions(n,a,b)
                for c in range(1 << n):
                    worlds += 1
                    if p['A'] == p['O'] or p['E'] == p['I']:
                        square_failures += 1
                    for r in ROUTES:
                        q = certificate(n,a,b,c,r)
                        if q['accepted']:
                            counts[r]['premises_hold'] += 1
                            if not q['conclusion_true']:
                                counts[r]['conclusion_failures'] += 1
                            if q['rejects_target']:
                                counts[r]['genuine_rejections'] += 1
                            elif not b:
                                counts[r]['empty_subject_nonrejections'] += 1
                            else:
                                raise RuntimeError('nonempty accepted route did not reject')
    if square_failures or any(x['conclusion_failures'] for x in counts.values()):
        raise RuntimeError('a semantic invariant failed')
    return {'model':'finite labeled sets; empty classes and empty domain allowed',
            'max_domain_size':max_n, 'worlds':worlds,
            'square_contradiction_failures':square_failures, 'routes':counts}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-n',type=int,default=4)
    args=parser.parse_args()
    print(json.dumps(enumerate_models(args.max_n),ensure_ascii=False,indent=2,sort_keys=True))
