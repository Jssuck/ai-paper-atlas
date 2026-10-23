"""Exhaustive finite checks; failures raise even under python -O or -OO."""
import itertools
import json
from model import scope_square, complement_inclusion, quantifiers, joint_denial, abilities, subsets

def require(condition, label):
    if not condition:
        raise RuntimeError('check failed: '+label)


def main():
    stats={'scope_models':0,'scope_gap_models':0,'inclusion_models':0,
           'strict_inclusion_models':0,'quantifier_models':0,
           'not_all_vs_all_not_disagreements':0,'joint_denial_models':0,
           'false_excluded_middle_models':0,'accessibility_models':0,
           'ability_scope_disagreements':0}
    for n in range(6):
        u=frozenset(f'x{i}' for i in range(n))
        for t in subsets(u):
            for p in subsets(t):
                q=scope_square(u,t,p)
                require(q.A|q.B==u and not q.A&q.B,'A/B partition')
                require(q.C|q.D==u and not q.C&q.D,'C/D partition')
                require(q.C<=q.B and q.A<=q.D,'scope implications')
                require(not q.A&q.C and q.B&q.D==u-t,'overlap')
                require((q.C==q.B)==(t==u),'first gap characterization')
                require((q.A==q.D)==(t==u),'second gap characterization')
                stats['scope_models']+=1
                stats['scope_gap_models']+=int(t!=u)
        for a in subsets(u):
            b=u-a
            f=joint_denial(u,a,b)
            require(not f,'joint denial of exhaustive pair empty')
            require((f==b)==(a==u),'joint/single denial equality boundary')
            stats['joint_denial_models']+=1
            stats['false_excluded_middle_models']+=int(a|f!=u)
            for c in subsets(a):
                q=complement_inclusion(u,c,a)
                require(q['B']<=q['D'],'contrapositive direction')
                require(q['A']&q['D']==a-c,'strictness witness')
                require(not q['B']&q['C'],'incompatible pair')
                require((q['B']<q['D'])==(c<a),'strictness equivalence')
                stats['inclusion_models']+=1
                stats['strict_inclusion_models']+=int(c<a)
            for s in subsets(u):
                q=quantifiers(u,s,a)
                require(q['not_all']==q['some_not'],'quantifier negation')
                stats['quantifier_models']+=1
                stats['not_all_vs_all_not_disagreements']+=int(q['not_all']!=q['all_not'])
    for n in range(5):
        for values in itertools.product([False,True],repeat=n):
            q=abilities(values)
            require(q['not_can_walk']==all(not x for x in values),'possibility negation')
            stats['accessibility_models']+=1
            stats['ability_scope_disagreements']+=int(q['can_not_walk']!=q['not_can_walk'])
    print(json.dumps(stats,sort_keys=True,indent=2))
    print('PASS: all finite checks; no claim of a general theorem or unique historical semantics')

if __name__=='__main__': main()
