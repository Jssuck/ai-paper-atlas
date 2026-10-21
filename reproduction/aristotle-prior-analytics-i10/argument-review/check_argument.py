"""Independent set-based checks of the article, without importing author code.
Finite execution supplements rather than proves the general set arguments.
"""
import itertools
import json

checks = 0

def require(value, label):
    global checks
    checks += 1
    if not value:
        raise RuntimeError(label)

def properties(w):
    actual = w[0]
    unions = tuple(w[0][i] | w[1][i] for i in range(3))
    cores = tuple(w[0][i] & w[1][i] for i in range(3))
    def ta(s,p): return actual[s] <= actual[p]
    def te(s,p): return not (actual[s] & actual[p])
    def ti(s,p): return bool(actual[s] & actual[p])
    def to(s,p): return bool(actual[s] - actual[p])
    def ne(s,p): return not (actual[s] & unions[p])
    def no(s,p): return bool(actual[s] - unions[p])
    def na(s,p): return actual[s] <= cores[p]
    def se(s,p): return not (unions[s] & unions[p])
    def be(s,p): return all(not (v[s] & v[p]) for v in w)
    return actual,unions,cores,ta,te,ti,to,ne,no,na,se,be

def run():
    global checks
    checks=0
    subsets=[frozenset(x for x in range(2) if mask & (1<<x)) for mask in range(4)]
    true_counts={name:0 for name in ['cesare_local','camestres_local','festino_local','cesare_bridge','camestres_bridge','ordinary_cesare','ordinary_camestres','ordinary_festino','ordinary_baroco']}
    false_counts={name:0 for name in ['anchored_conversion','cesare_strong','camestres_reverse','necessary_A_E','necessary_A_O','necessary_O','boxed_strong']}
    models=0
    for flat in itertools.product(subsets,repeat=6):
        models+=1
        w=(flat[:3],flat[3:])
        a,u,k,ta,te,ti,to,ne,no,na,se,be=properties(w)
        routes=[
            ('cesare_local',se(1,0) and ta(2,0),ne(2,1)),
            ('camestres_local',se(2,0) and ta(1,0),ne(1,2)),
            ('festino_local',se(1,0) and ti(2,0),no(2,1)),
            ('cesare_bridge',se(1,0) and ta(2,0) and u[2]<=u[0],se(2,1)),
            ('camestres_bridge',se(2,0) and ta(1,0) and u[1]<=u[0],se(2,1)),
            ('ordinary_cesare',te(1,0) and ta(2,0),te(2,1)),
            ('ordinary_camestres',ta(1,0) and te(2,0),te(2,1)),
            ('ordinary_festino',te(1,0) and ti(2,0),to(2,1)),
            ('ordinary_baroco',ta(1,0) and to(2,0),to(2,1))]
        for name,premise,conclusion in routes:
            true_counts[name]+=int(premise)
            require(not premise or conclusion,name)
        wrong=[
            ('anchored_conversion',ne(1,0),ne(0,1)),
            ('cesare_strong',se(1,0) and ta(2,0),se(2,1)),
            ('camestres_reverse',se(2,0) and ta(1,0),ne(2,1)),
            ('necessary_A_E',na(1,0) and te(2,0),ne(2,1)),
            ('necessary_A_O',na(1,0) and to(2,0),no(2,1)),
            ('necessary_O',ta(1,0) and no(2,0),no(2,1)),
            ('boxed_strong',be(0,1),se(0,1))]
        for name,premise,conclusion in wrong:
            false_counts[name]+=int(premise and not conclusion)
        for s,p in itertools.product(range(3),repeat=2):
            require(not se(s,p) or (ne(s,p) and ne(p,s) and be(s,p)),'strong implications')
            require(be(s,p)==be(p,s),'boxed symmetry')
    for name,n in true_counts.items(): require(n>0,'vacuous route '+name)
    for name,n in false_counts.items(): require(n>0,'missing counterexample '+name)
    x,y=frozenset([0]),frozenset([1]);both=x|y;empty=frozenset()
    # Exact four tables, with C empty when the article leaves it unused.
    q=properties(((y,x,empty),(y,both,empty)))
    require(q[7](1,0) and not q[7](0,1),'article 8.1')
    q=properties(((x,y,x),(x,y,both)))
    require(q[10](1,0) and q[3](2,0) and q[7](2,1) and not q[10](2,1),'article 8.2')
    q=properties(((x,x,y),(x,both,y)))
    require(q[10](2,0) and q[3](1,0) and q[7](1,2) and not q[7](2,1),'article 8.3')
    require(q[9](1,0) and q[4](2,0) and q[4](2,1) and not q[7](2,1),'article 8.4 universal')
    require(q[8](2,0) and q[3](1,0) and q[9](1,0) and not q[8](2,1) and q[6](2,1),'article 8.4 particular')
    q=properties(((x,empty,empty),(empty,x,empty)))
    require(q[11](0,1) and not q[10](0,1),'article section6 one-object counterexample')
    require(models==4096,'model count')
    return dict(status='PASS',models=models,checks=checks,true_route_premise_counts=true_counts,invalid_extension_counterexample_counts=false_counts,scope='Independent finite set checks; not a general proof or historical semantics certification.')

if __name__=='__main__':
    print(json.dumps(run(),ensure_ascii=False,indent=2,sort_keys=True))
