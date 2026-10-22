"""Independent finite checks of stated teaching claims, not ancient completeness."""
from itertools import product
import json, platform, sys

def ensure(v, message):
    if not v: raise RuntimeError(message)

def flip(x): return x[0] ^ x[1]
def ca(x,y): return not (y[0] & ~flip(x))
def ci(x,y): return bool(y[0] & flip(x))
def na(x,y): return not (y[0] & ~(x[0] & x[1]))
def ne(x,y): return not (y[0] & (x[0] | x[1]))
def boxa(x,y): return all(not (yw & ~xw) for xw,yw in zip(x,y))
def boxe(x,y): return all(not (yw & xw) for xw,yw in zip(x,y))

def oracle_flip(x,n): return {i for i in range(n) if any((w>>i)&1 for w in x) and any(not ((w>>i)&1) for w in x)}

def main():
    counts={'models':0,'oracle_comparisons':0,'universal_bridge_cases':0,'particular_bridge_cases':0,'strong_particular_bridge_cases':0,'swap_failures_nonempty':0,'third_figure_failures_nonempty':0}
    for n in (1,2,3):
        terms=list(product(range(1<<n),repeat=2))
        for a,b,c in product(terms,repeat=3):
            counts['models']+=1
            for x,y in ((a,b),(b,c),(a,c)):
                ys={i for i in range(n) if (y[0]>>i)&1}; fs=oracle_flip(x,n)
                ensure(ca(x,y)==(ys<=fs),'all oracle')
                ensure(ci(x,y)==bool(ys&fs),'some oracle')
                counts['oracle_comparisons']+=2
            if ca(a,c) and (c[0]&b[0]):
                ensure(ci(a,b),'universal bridge'); counts['universal_bridge_cases']+=1
            if ci(a,c) and ((c[0]&flip(a))&~b[0])==0:
                ensure(ci(a,b),'all existing A witnesses in B'); counts['particular_bridge_cases']+=1
            if ci(a,c) and not(c[0]&~b[0]):
                ensure(ci(a,b),'strong inclusion bridge'); counts['strong_particular_bridge_cases']+=1
            nonempty=all(w for t in (a,b,c) for w in t)
            if nonempty and ca(b,c) and not ci(c,b): counts['swap_failures_nonempty']+=1
            if nonempty and ca(a,c) and ca(b,c) and not ci(a,b): counts['third_figure_failures_nonempty']+=1
    examples={
      'double_all': {'A':(2,3),'B':(2,3),'C':(1,1)},
      'partial_wrong_witness': {'A':(4,5),'B':(6,5),'C':(3,3)},
      'natural_inclusion': {'A':(15,11),'B':(2,3),'C':(5,5)},
      'natural_exclusion': {'A':(12,8),'B':(2,3),'C':(5,5)},
      'bridge_success': {'A':(0,1),'B':(1,0),'C':(1,1)},
      'empty_middle': {'A':(1,1),'B':(1,1),'C':(0,0)},
    }
    a,b,c=examples['double_all'].values(); ensure(ca(a,c) and ca(b,c) and not ci(a,b) and not ci(c,b),'doubleall')
    a,b,c=examples['partial_wrong_witness'].values(); ensure(ci(a,c) and ca(b,c) and c[0]&b[0] and not ci(a,b),'wrong witness')
    for label,pred in [('natural_inclusion',na),('natural_exclusion',ne)]:
        a,b,c=examples[label].values(); ensure(ci(a,c) and ci(b,c) and pred(a,b) and not ci(a,b),label)
        ensure((c[0]&flip(a))&(c[0]&flip(b))==0,'disjoint witnesses')
        ensure((boxa if pred is na else boxe)(a,b),'worldwise natural background')
    a,b,c=examples['bridge_success'].values(); ensure(ca(a,c) and ca(b,c) and ci(a,b),'bridge example')
    a,b,c=examples['empty_middle'].values(); ensure(ca(a,c) and ca(b,c) and not ci(a,b),'empty universal')
    article_checks = [
      ('section8_1', (2,3),(3,0),(1,0), lambda a,b,c: ca(a,c) and bool(c[0]&b[0]) and ci(a,b)),
      ('section8_2', (2,3),(2,1),(3,3), lambda a,b,c: ci(a,c) and ca(b,c) and bool(c[0]&b[0]) and not ci(a,b)),
      ('section11_inclusion', (1,3),(1,2),(3,3), lambda a,b,c: ci(a,c) and ci(b,c) and na(a,b) and not ci(a,b)),
      ('section11_exclusion', (2,0),(1,2),(3,3), lambda a,b,c: ci(a,c) and ci(b,c) and ne(a,b) and not ci(a,b)),
      ('section11_nonempty_extension', (6,4),(1,2),(3,3), lambda a,b,c: ci(a,c) and ci(b,c) and ne(a,b) and not ci(a,b) and all(w for t in (a,b,c) for w in t)),
    ]
    for name,a,b,c,test in article_checks: ensure(test(a,b,c),name)
    counts['article_explicit_configurations']=len(article_checks)
    out={'python':platform.python_version(),'optimization':sys.flags.optimize,'scope':'all 1–3 object, two-world A/B/C valuations; actual world 0; independent bitmask oracle with explicit pointwise cross-check','counts':counts,'examples':examples,'result':'PASS','limits':'Finite implementation checks do not prove general results or endorse a unique interpretation of Aristotle.'}
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
