"""Independent I.22 set-theoretic checks; no import of author's code."""
from itertools import product
import json, platform, sys

def require(value, label):
    if not value:
        raise RuntimeError(label)

def interpret(n, worlds):
    u=set(range(n))
    rows=tuple(tuple({x for x in u if mask & (1<<x)} for mask in row) for row in worlds)
    def always(t): return {x for x in u if all(x in row[t] for row in rows)}
    def never(t): return {x for x in u if all(x not in row[t] for row in rows)}
    def varying(t): return u-always(t)-never(t)
    return rows, always, never, varying

names=('nonempty_necessity_transfer','universal_particular_transfer','particular_universal_transfer','positive_overlap_bridge','negative_overlap_bridge','necessary_implies_actual','contingent_implies_weak_negative','necessary_negative_implies_actual')
counts={name:0 for name in names}
configurations=checks=0
for n,nw in ((1,1),(1,2),(1,3),(2,1),(2,2),(2,3)):
    for masks in product(range(1<<n),repeat=3*nw):
        worlds=tuple(tuple(masks[3*w:3*w+3]) for w in range(nw))
        rows,always,never,varying=interpret(n,worlds)
        a,b,c=rows[0]
        cases=(
            (bool(c) and c<=varying(0) and c<=always(1), bool(b&varying(0))),
            (c<=varying(0) and bool(c&always(1)), bool(b&varying(0))),
            (bool(c&varying(0)) and c<=always(1), bool(b&varying(0))),
            (bool(b&c) and c<=always(0), bool(b&always(0))),
            (bool(b&c) and c<=never(0), bool(b&never(0))),
            (c<=always(1), c<=b),
            (bool(b&varying(0)), bool(b-always(0))),
            (bool(b&never(0)), bool(b-a)),
        )
        for name,(premise,conclusion) in zip(names,cases):
            checks+=1
            if premise:
                counts[name]+=1
                require(conclusion,name+repr(worlds))
        configurations+=1

examples={}
def record(label,n,worlds,criterion):
    rows,always,never,varying=interpret(n,worlds)
    require(criterion(rows,always,never,varying),label)
    examples[label]={'n':n,'worlds':worlds,'passed':True}

record('affirmative_no_unconditional_weak_conclusion',2,((1,2,1),(1,3,1)),lambda r,al,ne,v: r[0][2]<=al(0) and r[0][2]<=v(1) and not (r[0][1]-ne(0)))
record('negative_no_unconditional_actual_conclusion',2,((2,2,1),(2,3,1)),lambda r,al,ne,v: r[0][2]<=ne(0) and r[0][2]<=v(1) and not (r[0][1]-r[0][0]))
record('box_negative_actual_not_anchored_necessary',3,((2,1,1),(3,2,4)),lambda r,al,ne,v: all(all(s for s in row) for row in r) and all(not row[0]&row[2] for row in r) and r[0][2]<=v(1) and bool(r[0][1]-r[0][0]) and not r[0][1]&ne(0))
record('empty_middle',1,((1,0,0),(1,0,0)),lambda r,al,ne,v: r[0][2]<=v(0) and r[0][2]<=al(1) and not r[0][1]&v(0))
record('distinct_particular_witnesses',2,((1,2,3),(0,2,3)),lambda r,al,ne,v: bool(r[0][2]&v(0)) and bool(r[0][2]&al(1)) and not r[0][1]&v(0))
record('sleeping_horse',3,((2,2,1),(3,2,1)),lambda r,al,ne,v: r[0][2]<=v(0) and r[0][2]<=ne(1) and r[0][1]<=al(0) and all(all(s for s in row) for row in r))
record('waking_horse',3,((4,2,1),(5,2,1)),lambda r,al,ne,v: r[0][2]<=v(0) and r[0][2]<=ne(1) and r[0][1]<=ne(0) and all(all(s for s in row) for row in r))
record('contingent_not_actual',2,((2,1,1),(3,1,1)),lambda r,al,ne,v: r[0][2]<=v(0) and r[0][2]<=al(1) and bool(r[0][1]&v(0)) and not r[0][0]&r[0][1])
record('necessity_conversion_failure',2,((1,1,1),(1,1,0)),lambda r,al,ne,v: r[0][2]<=al(1) and bool(r[0][2]) and not r[0][1]&al(2))
record('contingency_conversion_failure',2,((1,2,1),(1,3,1)),lambda r,al,ne,v: r[0][2]<=v(1) and not r[0][1]&v(2))
record('weak_not_two_sided',1,((0,1,1),(0,1,1)),lambda r,al,ne,v: bool(r[0][1]-al(0)) and not r[0][1]&v(0))
record('prose_sleeping_horse_n2',2,((2,2,1),(3,2,1)),lambda r,al,ne,v: r[0][2]<=v(0) and r[0][2]<=ne(1) and r[0][1]<=al(0) and all(all(s for s in row) for row in r))
record('prose_distinct_particular_witnesses',2,((2,2,3),(3,2,3)),lambda r,al,ne,v: bool(r[0][2]&v(0)) and bool(r[0][2]&al(1)) and not r[0][1]&v(0))
print(json.dumps({'python':platform.python_version(),'optimization':sys.flags.optimize,'configurations':configurations,'rule_checks':checks,'rule_premise_hits':counts,'independent_examples':examples,'scope':'Finite implementation checks supplement the general set proofs; no claim of unique ancient semantics.'},ensure_ascii=False,indent=2))
