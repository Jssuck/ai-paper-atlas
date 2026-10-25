"""Independent I.21 check: actual sets and all-pairs graph/Kahn algorithm.

The expected semantics/edge relation below do not call model.py. The implementation
is imported only for comparison after expectations are independently computed.
Finite checks do not establish the general infinite termination claim.
"""
from collections import deque
from itertools import product
import json
import model


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def subsets(n):
    return [frozenset(i for i, flag in enumerate(flags) if flag)
            for flags in product((False, True), repeat=n)]


def semantic_oracle(bound):
    counts = [[0,0] for _ in range(3)]
    assignments = weak = weak_fail = 0
    for n in range(bound + 1):
        sets = subsets(n)
        for a,b,c in product(sets, repeat=3):
            assignments += 1
            cases = [(not a.intersection(b) and c.issubset(b), not a.intersection(c)),
                     (a.issubset(b) and not b.intersection(c), not a.intersection(c)),
                     (b.issubset(a) and bool(b.difference(c)), bool(a.difference(c)))]
            for i,(premise, conclusion) in enumerate(cases):
                if premise:
                    counts[i][0] += 1
                    counts[i][1] += int(not conclusion)
        for p,s in product(sets, repeat=2):
            if s and not s.intersection(p):
                weak += 1
                weak_fail += int(not s.difference(p))
    expected = {'assignments': assignments, 'premise_counts':[x[0] for x in counts],
                'counterexamples':[x[1] for x in counts], 'weakening_cases':weak,
                'weakening_counterexamples':weak_fail}
    actual = model.semantic_results(bound)
    check(actual['assignments']==assignments, 'assignment mismatch')
    for row, tally in zip(actual['rules'].values(), counts):
        check([row['premise_cases'],row['counterexamples']]==tally, 'rule count mismatch')
    check(actual['E_to_O_with_nonempty_subject']=={'premise_cases':weak,'counterexamples':weak_fail}, 'weakening count mismatch')
    return expected


def allowed(s,t,evidence):
    q,p,x = s
    r,j,y = t
    if q == r == 'E':
        return (j>p and x==y) or (p==j and y>x)
    if q == r == 'O':
        return (j>p and x==y) or (p==j and y<x)
    return evidence and q=='O' and r=='E' and p==j and x==y


def graph_oracle(h,evidence):
    states=list(product(('E','O'),range(h+1),range(h+1)))
    edges={(s,t) for s,t in product(states, repeat=2) if allowed(s,t,evidence)}
    actual={(s,t) for s in states for _,t in model.successors(s,h,evidence)}
    check(edges==actual, 'edge mismatch')
    indegree={s:0 for s in states}
    outgoing={s:[] for s in states}
    longest={s:0 for s in states}
    for s,t in edges:
        indegree[t]+=1
        outgoing[s].append(t)
        check(model.measure(t,h)<model.measure(s,h), 'nondecreasing measure')
    queue=deque(s for s in states if indegree[s]==0)
    processed=0
    while queue:
        s=queue.popleft();processed+=1
        for t in outgoing[s]:
            longest[t]=max(longest[t],longest[s]+1)
            indegree[t]-=1
            if indegree[t]==0:queue.append(t)
    check(processed==len(states), 'cycle found')
    steps=max(longest.values())
    if evidence:
        actual_report=model.ranking_results(h)
        check(actual_report['states']==len(states) and actual_report['edges']==len(edges), 'graph counts mismatch')
        check(actual_report['max_backward_steps']==steps, 'longest path mismatch')
    return {'height':h,'evidence':evidence,'states':len(states),'edges':len(edges),'longest_steps':steps,'acyclic':True}


def main():
    semantic=[{'bound':b,**semantic_oracle(b)} for b in (4,5)]
    graphs=[graph_oracle(h,e) for h in range(9) for e in (False,True)]
    check(not model.has_cycle([('u','v')]),'R should terminate')
    check(not model.has_cycle([('v','u')]),'S should terminate')
    check(model.has_cycle([('u','v'),('v','u')]),'union must cycle')
    return {'semantic_checks':semantic,'graph_checks':graphs,'mismatches':0,
            'scope':'Independent finite set enumeration through n=5 and pairwise/Kahn graphs H=0..8; not a proof of the general infinite claim.'}

if __name__=='__main__':
    print(json.dumps(main(),ensure_ascii=False,indent=2))
