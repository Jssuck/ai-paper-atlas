"""Small explicit examples. All universes are teaching assumptions."""
from itertools import product
import condillac_model as m


def chips(bound=10):
    if type(bound) is not int or bound < 1:
        raise ValueError('bound must be an exact positive integer')
    u = m.Universe(('x', 'y'), tuple(product(range(bound + 1), repeat=2)))
    target = m.table(u, '(x,y)', lambda w: w)
    feasible = m.constraint(u, 'both hypothetical transfers have a token to give', lambda w: w[0] >= 1 and w[1] >= 1)
    original = m.Problem(u, target, (feasible,
        m.constraint(u, 'x-1=y+1', lambda w: w[0]-1 == w[1]+1),
        m.constraint(u, 'x+1=2(y-1)', lambda w: w[0]+1 == 2*(w[1]-1))))
    expanded = m.Problem(u, target, (feasible,
        m.constraint(u, 'x-y=2', lambda w: w[0]-w[1] == 2),
        m.constraint(u, 'x-2y=-3', lambda w: w[0]-2*w[1] == -3)))
    eliminated = m.Problem(u, target, (feasible,
        m.constraint(u, 'x=y+2', lambda w: w[0] == w[1]+2),
        m.constraint(u, 'y=5', lambda w: w[1] == 5)))
    solved = m.Problem(u, target, (feasible,
        m.constraint(u, 'x=7 and y=5', lambda w: w == (7,5))))
    insufficient = m.Problem(u, target, original.constraints[:2])
    return original, expanded, eliminated, solved, insufficient


def query_example():
    u = m.Universe(('x', 'tag'), ((0,'A'), (0,'B'), (1,'A'), (1,'B')))
    target = m.table(u, 'x', lambda w: w[0])
    full = m.Problem(u, target)
    known_x = m.add_evidence(full, m.constraint(u, 'x=0', lambda w: w[0] == 0))
    narrower = m.add_evidence(known_x, m.constraint(u, 'tag=A', lambda w: w[1] == 'A'))
    return full, known_x, narrower


def selector():
    u = m.Universe(('s', 'a', 'b'), tuple(product((0,1), repeat=3)))
    p = m.Problem(u, m.table(u, 'a if s=0 else b', lambda w: w[1] if w[0] == 0 else w[2]))
    qs = tuple(m.table(u, name, lambda w, i=i: w[i]) for i, name in enumerate(u.fields))
    return p, qs


def causal_run(model, u, do_s=None):
    """Two stipulated structural models, returning (S,A); no empirical claim.

    M1: S := U; A := S. M2: A := U; S := A.
    do_s replaces only the equation for S, while holding U fixed.
    """
    if type(model) is not str or model not in ('M1', 'M2'):
        raise ValueError('model must be M1 or M2')
    if type(u) is not int or u not in (0,1):
        raise ValueError('u must be exact integer 0 or 1')
    if do_s is not None and (type(do_s) is not int or do_s not in (0,1)):
        raise ValueError('do_s must be None or exact integer 0 or 1')
    if model == 'M1':
        s = u if do_s is None else do_s
        a = s
    else:
        a = u
        s = a if do_s is None else do_s
    return s,a


def causal_toy():
    u = m.Universe(('model',), (('M1',), ('M2',)))
    p = m.Problem(u, m.table(u, 'causal model', lambda w: w[0]))
    qs = (m.table(u, 'natural (S,A) at U=0 and U=1',
                  lambda w: tuple(causal_run(w[0], exogenous) for exogenous in (0,1))),)
    return p, qs
