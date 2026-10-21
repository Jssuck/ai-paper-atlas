"""Independent bounded oracle: bit-mask implementation checked via Python sets."""
import json,sys,itertools
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from model import Model, Proposition, Step, derive, verify
count={k:0 for k in ('models','pointwise_quantifiers','bridge_implications','shape_checks','certificate_rejections')}
def check(ok):
    if not ok: raise RuntimeError('independent check failed')
expected={('a','a'):'a',('a','e'):'a',('a','i'):'i',('a','o'):'i',('e','a'):'e',('e','e'):'e',('e','i'):'o',('e','o'):'o'}
for x,y in itertools.product('aeio',repeat=2):
    p,q=Proposition(x,'A','B'),Proposition(y,'B','C'); d=derive(p,q)
    check((d is not None)==((x,y) in expected));count['shape_checks']+=1
    if d:
        check(d[-1].formula==Proposition(expected[x,y],'A','C'));check(verify(p,q,d))
        wrong=d+(Step('quality',p.quality(),(0,)),)
        check(not verify(p,q,wrong));count['certificate_rejections']+=1
        for step in (Step('premise',p),Step('quality',p.quality(),(len(d),)),Step('base',d[-1].formula,(True,1))):
            check(not verify(p,q,d+(step,)));count['certificate_rejections']+=1
for n,ws in ((1,1),(1,2),(1,3),(2,1),(2,2)):
    D=set(range(n))
    subsets=[{x for x in D if mask&(1<<x)} for mask in range(2**n)]
    for masks in itertools.product(range(2**n),repeat=3*ws):
        worlds=tuple(tuple(masks[3*w:3*w+3]) for w in range(ws))
        sets=[[subsets[v] for v in world] for world in worlds]
        for actual in range(ws):
            m=Model(n,worlds,actual);count['models']+=1
            possibles=[];contingents=[]
            for k,t in enumerate('ABC'):
                possible=set.union(*(s[k] for s in sets));necessary=set.intersection(*(s[k] for s in sets));contingent=possible-necessary
                possibles.append(possible);contingents.append(contingent)
                check(m.possible_set(t)==sum(1<<x for x in possible))
                check(m.contingent_set(t)==sum(1<<x for x in contingent))
                for mask,S in enumerate(subsets):
                    for mode in 'aeio':
                        oracle=S<=contingent if mode in 'ae' else bool(S&contingent)
                        check(m.quantify(mode,mask,t)==oracle);count['pointwise_quantifiers']+=1
            C=sets[actual][2]
            # Independently check all T supersets, not just T=possible(B).
            for T in subsets:
                if possibles[1]<=T and T<=contingents[0]:
                    for universal in (True,False):
                        premise=C<=contingents[1] if universal else bool(C&contingents[1])
                        if premise:
                            conclusion=C<=contingents[0] if universal else bool(C&contingents[0])
                            check(conclusion);count['bridge_implications']+=1
print(json.dumps({'status':'pass','coverage':count,'scope':'finite labelled models; multiple actual-world indices; not an infinite-model proof'},indent=2))
