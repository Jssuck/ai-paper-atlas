"""Original finite teaching models for Posterior Analytics I.21; Python stdlib only.
All(P,S) means S is a subset of P, E(P,S) disjoint, O(P,S) S minus P nonempty.
Ranking states are an abstract backward-proof skeleton, not set truth certificates.
"""
from itertools import product
from functools import lru_cache


def All(predicate, subject):
    return subject & ~predicate == 0


def E(predicate, subject):
    return predicate & subject == 0


def O(predicate, subject):
    return subject & ~predicate != 0


def semantic_results(max_universe=4):
    if not isinstance(max_universe, int) or not 0 <= max_universe <= 6:
        raise ValueError('universe bound must be an integer between 0 and 6')
    counts = {name: {'premise_cases': 0, 'counterexamples': 0}
              for name in ['first_EAE', 'second_AEE', 'third_AOO']}
    assignments = 0
    weak_cases = weak_fail = 0
    for n in range(max_universe + 1):
        for a, b, c in product(range(1 << n), repeat=3):
            assignments += 1
            cases = [(E(a,b) and All(b,c), E(a,c)),
                     (All(b,a) and E(b,c), E(a,c)),
                     (All(a,b) and O(c,b), O(c,a))]
            for name, (premise, conclusion) in zip(counts, cases):
                if premise:
                    counts[name]['premise_cases'] += 1
                    counts[name]['counterexamples'] += int(not conclusion)
        for p, s in product(range(1 << n), repeat=2):
            if E(p,s) and s != 0:
                weak_cases += 1
                weak_fail += int(not O(p,s))
    return {'universe_sizes': list(range(max_universe+1)),
            'assignments': assignments, 'rules': counts,
            'E_to_O_with_nonempty_subject': {'premise_cases':weak_cases,'counterexamples':weak_fail},
            'empty_subject_example': {'P':1,'S':0,'E':E(1,0),'O':O(1,0)},
            'O_not_E_example': {'P':1,'S':3,'O':O(1,3),'E':E(1,3)},
            'third_figure_conclusion_not_universal': {'A':3,'B':1,'C':2,
              'premises': All(3,1) and O(2,1),'O_C_A':O(2,3),'E_C_A':E(2,3)}}


def validate(state, height):
    if not isinstance(height,int) or height < 0:
        raise ValueError('height must be a nonnegative integer')
    q,p,s = state
    if q not in ('E','O') or not all(isinstance(x,int) and 0<=x<=height for x in (p,s)):
        raise ValueError('invalid state')


def measure(state, height):
    validate(state,height)
    q,p,s=state
    if q == 'E':
        return (height-p)+(height-s)
    return 2*height+1+(height-p)+s


def successors(state, height, nonempty_subject=False):
    """Backward goal -> premise candidates. Strict changes only, no conversion loop.

    E goal: raise either endpoint. O goal: raise predicate or lower subject.
    O -> E at the same endpoints needs separate nonempty-subject evidence.
    These ranks only encode progress; semantic/causal admissibility is not checked.
    """
    validate(state,height)
    q,p,s=state
    result=[('raise_predicate',(q,x,s)) for x in range(p+1,height+1)]
    if q=='E':
        result += [('raise_subject',('E',p,x)) for x in range(s+1,height+1)]
    else:
        result += [('lower_subject',('O',p,x)) for x in range(s)]
        if nonempty_subject:
            result += [('existential_weakening_backwards',('E',p,s))]
    return result


def ranking_results(height=4):
    states=[(q,p,s) for q in ('E','O') for p in range(height+1) for s in range(height+1)]
    edges=[(s,label,t) for s in states for label,t in successors(s,height,True)]
    violations=[(s,l,t) for s,l,t in edges if measure(t,height)>=measure(s,height)]
    @lru_cache(None)
    def longest(s):
        children=successors(s,height,True)
        return max((1+longest(t) for _,t in children), default=0)
    return {'height':height,'states':len(states),'edges':len(edges),
            'strict_decrease_violations':len(violations),
            'max_initial_measure':max(measure(s,height) for s in states),
            'max_backward_steps':max(longest(s) for s in states),
            'O_to_E_requires_nonempty_evidence': not any(t[0]=='E' for _,t in successors(('O',0,height),height,False)),
            'same_state_or_equivalence_moves_included':False}


def has_cycle(edges):
    vertices=set(x for edge in edges for x in edge)
    outgoing={x:[] for x in vertices}
    for x,y in edges: outgoing[x].append(y)
    active,done=set(),set()
    def visit(x):
        if x in active:return True
        if x in done:return False
        active.add(x)
        if any(visit(y) for y in outgoing[x]):return True
        active.remove(x);done.add(x)
        return False
    return any(visit(x) for x in vertices)


def switching_example():
    r=[('u','v')]; s=[('v','u')]
    return {'R':r,'S':s,'R_has_cycle':has_cycle(r),'S_has_cycle':has_cycle(s),
            'union_has_cycle':has_cycle(r+s),'alternating_prefix':['u','v','u','v','u']}


def results():
    return {'semantics':semantic_results(),'ranking':ranking_results(),
            'switching_counterexample':switching_example(),
            'scope':'Finite teaching semantics and declared backward-rule skeleton only; no proof of Aristotle\'s full infinite claim.'}

if __name__=='__main__':
    import json
    print(json.dumps(results(),ensure_ascii=False,indent=2))
