"""Independent finite diagnostics for I.23. No author implementation imported.
General proofs are in the article and audit; these runs do not prove them.
"""
import itertools
import json
import sys

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def holds(q, subject, predicate):
    if q == 'a': return subject <= predicate
    if q == 'e': return not subject & predicate
    if q == 'i': return bool(subject & predicate)
    if q == 'o': return bool(subject - predicate)
    raise ValueError('Unknown quantifier')

def types_model(k, mask):
    universe = frozenset(i for i in range(2**k) if mask & (1 << i))
    return universe, tuple(frozenset(i for i in universe if (i >> j) & 1) for j in range(k))

def main():
    count3 = all_nonempty = barbara = darapti = empty_failure = 0
    swaps = 0
    for mask in range(1,256):
        u,(a,b,m) = types_model(3,mask)
        count3 += 1
        all_nonempty += bool(a and b and m)
        if b <= m and m <= a:
            require(b <= a,'Barbara failed')
            barbara += 1
        if m <= a and m <= b and m:
            require(bool(a & b),'Witness bridge failed')
            darapti += 1
        if m <= a and m <= b and not (a & b):
            require(not m,'Missing witness counterexample not empty')
            empty_failure += 1
        for x,y in itertools.product((a,b,m),repeat=2):
            require(holds('e',x,y)==holds('e',y,x),'E symmetry')
            require(holds('i',x,y)==holds('i',y,x),'I symmetry')
            require(holds('a',x,y)!=holds('o',x,y),'A/O complement')
            require(holds('e',x,y)!=holds('i',x,y),'E/I complement')
            swaps += 4
    require(count3==255 and all_nonempty==218,'Three-term cardinality')
    # All three-term profiles, but independently choose concrete singletons
    # for the two possible interpretations of the absent B predicate.
    free = 0
    for n in range(2,6):
        u=frozenset(range(n))
        for amask in range(1,(1<<n)-1):
            a=frozenset(i for i in u if amask & (1<<i))
            for x,y in itertools.product(a,u-a):
                bx,by=frozenset((x,)),frozenset((y,))
                require([holds(q,bx,a) for q in 'aeio']==[True,False,True,False],'B inside')
                require([holds(q,by,a) for q in 'aeio']==[False,True,False,True],'B outside')
                free+=1
    chain_models=chain_satisfiers=0
    for mask in range(1,65536):
        _,(b,c1,c2,a)=types_model(4,mask)
        chain_models+=1
        if b<=c1 and c1<=c2 and c2<=a:
            require(b<=c2 and b<=a,'Four-term chain')
            chain_satisfiers+=1
    require(chain_satisfiers==31,'Chain satisfiers')
    # Explicit nonempty countermodels and nonempty domain with empty terms.
    u=frozenset((0,1)); a=frozenset((0,)); b=frozenset((1,)); m=u
    require(a<=m and b<=m and not b<=a and not a&b,'Common-predicate example')
    require(holds('i',a,m) and holds('i',m,b) and not holds('i',a,b),'Different witnesses')
    a=b=frozenset((0,))
    require(a<=m and b<=m and not holds('e',b,a) and not holds('o',b,a),'Opposite example')
    a=b=m=frozenset()
    require(holds('a',m,a) and holds('a',m,b) and not holds('i',b,a),'Empty middle')
    require(holds('e',a,a) and holds('e',u,a),'Absent term exception')
    # The four orientations classified only by middle's subject/predicate roles.
    role_patterns=list(itertools.product(('subject','predicate'),repeat=2))
    role_classes={tuple(sorted(p)) for p in role_patterns}
    require(len(role_patterns)==4 and len(role_classes)==3,'Role classes')
    # Finite parity identity diagnostic, not the irrationality theorem.
    parity_cases=0
    for t in range(-100,101):
        value=(2*t+1)**2
        require(value==2*(2*t*t+2*t)+1 and value%2==1,'Parity identity')
        parity_cases+=1
    result={'three_term_models':count3,'all_terms_nonempty':all_nonempty,
            'barbara_satisfiers':barbara,'darapti_nonempty_satisfiers':darapti,
            'missing_witness_countermodels':empty_failure,
            'symmetry_complement_checks':swaps,'free_B_singleton_pairs':free,
            'four_term_models':chain_models,'chain_satisfiers':chain_satisfiers,
            'explicit_examples':5,'orientations':4,'middle_role_classes':3,
            'parity_identity_cases':parity_cases,
            'scope':'Finite diagnostics only; no author imports; no RAA proof-checker claim.',
            'status':'passed'}
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
