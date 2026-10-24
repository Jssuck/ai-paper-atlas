"""Independent propositional-cell and closed-count checks for II.21 teaching code.

Does not import the production world generator or premise evaluator for its oracle.
Production methods are called only for comparisons and public-interface checks.
"""
import itertools
import json
import pathlib
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import epistemic_routes as target


def equal(actual, expected, label):
    if actual != expected:
        raise RuntimeError(f'{label}: {actual!r} != {expected!r}')


def rejected(call, label):
    try:
        call()
    except ValueError:
        return
    raise RuntimeError(f'{label}: invalid input was accepted')


def main():
    summaries = []
    # Per-object Boolean cells: B -> A; D -> B; C -> not A; D -> C.
    cells = list(itertools.product((False, True), repeat=4))
    flags = [(not b or a, not d or b, not c or not a, not d or c)
             for a,b,c,d in cells]
    equal(sum(all(p) for p in flags), 4, 'allowed full cells')
    equal(sum(all(p[:3]) for p in flags), 5, 'allowed three-premise cells')
    equal(sum(p[0] and p[1] for p in flags), 8, 'positive cells')
    equal(sum(p[2] and p[3] for p in flags), 8, 'negative cells')
    for n in (1,2,3):
        compared = 0
        for sequence in itertools.product(range(16), repeat=n):
            truth = tuple(all(flags[k][j] for k in sequence) for j in range(4))
            w = {term: frozenset(i for i,k in enumerate(sequence) if cells[k][j])
                 for j,term in enumerate('ABCD')}
            equal(target.premises(w), truth, 'per-object truth')
            compared += 1
        expected = dict(worlds=16**n, full_nonempty_D=0,
                        full_empty_D=4**n, missing_p4_nonempty_D=5**n-4**n,
                        positive_route=8**n-6**n, negative_route=8**n-6**n)
        report = target.census(n)
        equal(report['counts'], expected, 'closed counts')
        witness = report['missing_p4_witness']
        # Direct quantified membership validation, independent of production premises.
        a,b,c,d = (witness[t] for t in 'ABCD')
        equal((all(x in a for x in b), all(x in b for x in d),
               all(x not in a for x in c), all(x in c for x in d)),
              (True,True,True,False), 'returned witness')
        if not d:
            raise RuntimeError('witness D must be nonempty')
        summaries.append(dict(n=n, compared_worlds=compared, closed_counts=expected))
    checked_states = 0
    accepted_states = 0
    for u,r,o,e in itertools.product((False,True), repeat=4):
        checked_states += 1
        if e and not (u and r):
            rejected(lambda: target.RecognitionState(u,r,o,e), 'invalid exercise')
            continue
        s = target.RecognitionState(u,r,o,e)
        accepted_states += 1
        equal(s.available, (u,r)==(True,True), 'availability')
        equal(s.explicit_conflict, (e,o)==(True,True), 'explicit conflict')
        if not (u and r):
            rejected(s.exercise, 'missing premise')
        else:
            after = s.exercise()
            equal(after.exercised, True, 'exercise transition')
            equal(after.negative_opinion, o, 'opinion retained')
            equal(s.exercised, e, 'immutable original')
            equal(after.exercise(), after, 'idempotent exercise')
    valid = {t:frozenset([0]) for t in 'ABCD'}
    invalid_worlds = [None, [], {}, {**valid,'E':frozenset()},
                      {**valid,'A':set()}, {**valid,'A':frozenset([True])},
                      {**valid,'A':frozenset([-1])}, {**valid,'A':frozenset(['0'])}]
    for w in invalid_worlds:
        rejected(lambda: target.premises(w), 'malformed world')
    for value in (0,4,True,False,1.0,'2',None):
        rejected(lambda: list(target.worlds(value)), 'bad census bound')
    for p,i in [('Z',0),('A',1),('A',True),('A',-1),('A',0.0),(None,0)]:
        rejected(lambda: target.acquire_verified(valid,p,i), 'invalid recognition')
    equal(target.acquire_verified(valid,'A',0), ('A',0), 'verified recognition')
    for value in (0,1,None,'True'):
        rejected(lambda: target.RecognitionState(value,True,False), 'nonbool flag')
    print(json.dumps(dict(set_checks=summaries, state_combinations=checked_states,
                          accepted_states=accepted_states, rejected_states=16-accepted_states,
                          malformed_worlds=len(invalid_worlds), verdict='PASS'),
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
