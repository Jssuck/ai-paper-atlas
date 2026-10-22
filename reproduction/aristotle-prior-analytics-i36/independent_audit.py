"""Independent review: integer-bit oracle, two relations, nested projections.

This is bounded testing, not a completeness or historical-interpretation proof.
Run: python3 independent_audit.py
"""
import itertools
import json
from model import Model, Invalid, check, infer


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def run():
    count = {'models': 0, 'semantic_comparisons': 0, 'true_rule_instances': 0,
             'general_claim_instances': 0, 'rejected_inputs': 0}
    # Each binary relation is an independent n*n bit matrix, ordered source,target.
    for n in (1, 2):
        names = tuple('ab'[:n]); full = (1 << n) - 1
        for pm, qm, rm, sm in itertools.product(range(1<<n), range(1<<n), range(1<<(n*n)), range(1<<(n*n))):
            atoms = {'P': pm, 'Q': qm}; matrices = {'r': rm, 's': sm}
            P = ('atom', 'P'); Q = ('atom', 'Q')
            exprs = (P, Q, ('some','r',P), ('some','s',Q), ('some','s',('some','r',P)))
            def mask(e):
                if e[0] == 'atom': return atoms[e[1]]
                m = mask(e[2]); result = 0; edges = matrices[e[1]]
                for a in range(n):
                    if (m>>a)&1:
                        for b in range(n):
                            if (edges>>(a*n+b))&1: result |= 1<<b
                return result
            def truth(f):
                if f[0] == 'edge':
                    return bool((matrices[f[1]]>>(names.index(f[2])*n+names.index(f[3])))&1)
                a = mask(f[1]); k = f[0]
                if k in ('member','notmember'):
                    yes = bool((a>>names.index(f[2]))&1)
                    return yes if k=='member' else not yes
                b = mask(f[2])
                if k=='subset': return a & (full^b) == 0
                if k=='disjoint': return a & b == 0
                if k=='not_subset': return a & (full^b) != 0
                raise RuntimeError('bad oracle fact')
            m = Model(frozenset(names),
                      {p:frozenset(names[i] for i in range(n) if bits>>i&1) for p,bits in atoms.items()},
                      {r:frozenset((names[i],names[j]) for i in range(n) for j in range(n) if bits>>(i*n+j)&1) for r,bits in matrices.items()})
            count['models'] += 1
            fs = [(k,e,x) for k in ('member','notmember') for e in exprs for x in names]
            fs += [(k,e,f) for k in ('subset','disjoint','not_subset') for e in exprs for f in exprs]
            fs += [('edge',r,x,y) for r in matrices for x in names for y in names]
            for f in fs:
                require(m.true(f)==truth(f), ('semantic',f)); count['semantic_comparisons'] += 1
            def rule(r, a, b):
                if truth(a) and truth(b):
                    out=infer(r,(a,b)); require(truth(out),('unsound',r,a,b,out)); count['true_rule_instances'] += 1
            for e in exprs:
                for r,x,y in itertools.product(matrices,names,names): rule('project',('member',e,x),('edge',r,x,y))
                for f in exprs:
                    for x in names:
                        rule('instantiate',('subset',e,f),('member',e,x))
                        rule('exclude',('disjoint',e,f),('member',e,x))
                        rule('difference',('member',e,x),('notmember',f,x))
                    for g in exprs: rule('transitive',('subset',e,f),('subset',f,g))
            # Two general statements checked only on this finite domain.
            def image(bits, edges):
                out=0
                for i in range(n):
                    for j in range(n):
                        if bits>>i&1 and edges>>(i*n+j)&1:out |= 1<<j
                return out
            for edges in matrices.values():
                if pm & (full^qm)==0:
                    require(image(pm,edges)&(full^image(qm,edges))==0,'monotonicity')
                    count['general_claim_instances'] += 1
                require(image(pm&qm,edges)&(full^(image(pm,edges)&image(qm,edges)))==0,'intersection direction')
                count['general_claim_instances'] += 1
    P=('atom','P'); Q=('atom','Q'); E=('some','r',P)
    premises=(('member',P,'a'),('edge','r','a','b'))
    good={'rule':'project','refs':(0,1),'conclusion':('member',E,'b')}
    attacks=[]
    for refs in ((-1,1),(0,2),(True,1),(0,False),(0.0,1),(0,),[0,1],(0,1,1)):
        attacks.append(lambda refs=refs:check(premises,({**good,'refs':refs},)))
    for conclusion in (('member',P,'b'),('member',('some','s',P),'b'),('member',E,'a'),('notmember',E,'b')):
        attacks.append(lambda conclusion=conclusion:check(premises,({**good,'conclusion':conclusion},)))
    for step in ({**good,'extra':0},{k:v for k,v in good.items() if k!='refs'},['project',(0,1)],{**good,'rule':False}):
        attacks.append(lambda step=step:check(premises,(step,)))
    attacks += [lambda:check(list(premises),(good,)),lambda:check(premises,[good]),
                lambda:infer('project',(('member',P,'b'),('edge','r','a','b'))),
                lambda:infer('difference',(('member',P,'a'),('notmember',Q,'b'))),
                lambda:Model(frozenset(),{},{}),
                lambda:Model(frozenset({'a'}),{'P':frozenset({'b'})},{}),
                lambda:Model(frozenset({'a'}),{}, {'r':frozenset({('a','b')})}),
                lambda:Model(frozenset({'a'}),{},{}).true(('member',P,'a'))]
    for operation in attacks:
        try: operation()
        except Invalid: count['rejected_inputs'] += 1
        else: raise RuntimeError('bad input accepted')
    # Explicit independent countermodels, no model implementation calls.
    p={0}; rel={(0,1)}; universe={0,1}
    proj=lambda a,r:{y for x,y in r if x in a}
    counterexamples={
       'projection_not_identity':1 in proj(p,rel) and 1 not in p,
       'relation_not_symmetric':(0,1) in rel and (1,0) not in rel,
       'separate_not_common_witness':all(any((u,x) in {(0,0),(1,1)} for u in universe) for x in universe) and not any(all((u,x) in {(0,0),(1,1)} for x in universe) for u in universe),
       'noninclusion_not_disjoint':bool(universe-{1}) and bool(universe&{1}),
       'having_genus_not_being_genus':1 in proj({0},{(0,1)}) and 1 not in {0},
       'irreflexive_not_class_exclusion':all((x,x) not in rel for x in universe) and 1 in proj(universe,rel) and 1 in universe,
       'projection_intersection_converse_fails':bool(proj({0},{(0,2),(1,2)}) & proj({1},{(0,2),(1,2)})) and not proj({0}&{1},{(0,2),(1,2)}),
       'monotonicity_converse_fails':proj({0},set())<=proj(set(),set()) and not {0}<=set()
    }
    require(all(counterexamples.values()),counterexamples)
    count['countermodels']=counterexamples
    print(json.dumps(count,indent=2,sort_keys=True))

if __name__=='__main__':run()
