"""Finite independent direct-quantifier oracle and deliberate countermodels."""
import itertools, json
from model import Model, infer
U=('a','b')
E=tuple(('atom',p) for p in ('P','Q','G'))
E=E+tuple(('some','of',p) for p in E)

def powers(items):
    return tuple(frozenset(x for i,x in enumerate(items) if mask>>i&1) for mask in range(1<<len(items)))

def truth(f, atoms, rel):
    def holds(e,x):
        if e[0]=='atom':return x in atoms[e[1]]
        return any(holds(e[2],y) and (y,x) in rel for y in U)
    k=f[0]
    if k=='edge':return (f[2],f[3]) in rel
    if k=='member':return holds(f[1],f[2])
    if k=='notmember':return not holds(f[1],f[2])
    if k=='subset':return all(not holds(f[1],x) or holds(f[2],x) for x in U)
    if k=='disjoint':return all(not(holds(f[1],x) and holds(f[2],x)) for x in U)
    if k=='not_subset':return any(holds(f[1],x) and not holds(f[2],x) for x in U)
    raise RuntimeError(k)

def run():
    counts={'models':0,'semantic_comparisons':0,'true_premise_rule_instances':{r:0 for r in ('project','instantiate','transitive','exclude','difference')}}
    for sets in itertools.product(powers(U),repeat=3):
      atoms=dict(zip(('P','Q','G'),sets))
      for rel in powers(tuple(itertools.product(U,repeat=2))):
        counts['models']+=1
        m=Model(frozenset(U),atoms,{'of':rel})
        fs=[(k,p,x) for k in ('member','notmember') for p in E for x in U]
        fs += [(k,p,q) for k in ('subset','disjoint','not_subset') for p in E for q in E]
        fs += [('edge','of',s,t) for s in U for t in U]
        for f in fs:
            if m.true(f)!=truth(f,atoms,rel):raise RuntimeError(('semantic mismatch',f))
            counts['semantic_comparisons']+=1
        def verify(rule,a,b):
            if truth(a,atoms,rel) and truth(b,atoms,rel):
                out=infer(rule,(a,b))
                if not truth(out,atoms,rel):raise RuntimeError(('unsound instance',rule,a,b,out))
                counts['true_premise_rule_instances'][rule]+=1
        for p in E:
          for x,y in itertools.product(U,repeat=2): verify('project',('member',p,x),('edge','of',x,y))
          for q in E:
            for x in U:
              verify('instantiate',('subset',p,q),('member',p,x))
              verify('exclude',('disjoint',p,q),('member',p,x))
              verify('difference',('member',p,x),('notmember',q,x))
            for r in E:verify('transitive',('subset',p,q),('subset',q,r))
    # Countermodels are original teaching examples, not historical facts.
    p=('atom','P'); ep=('some','of',p)
    m=Model(frozenset(U),{'P':frozenset({'a'})},{'of':frozenset({('a','b')})})
    checks={
      'projection_not_identity':m.true(('member',ep,'b')) and not m.true(('member',p,'b')),
      'relation_not_symmetric':m.true(('edge','of','a','b')) and not m.true(('edge','of','b','a')),
      'forall_exists_not_exists_forall':all(any((y,x) in {('a','a'),('b','b')} for y in U) for x in U) and not any(all((y,x) in {('a','a'),('b','b')} for x in U) for y in U),
      'difference_not_disjoint':not frozenset(U)<=frozenset({'b'}) and bool(frozenset(U)&frozenset({'b'})),
      'having_genus_not_being_genus':Model(frozenset(U),{'G':frozenset({'a'})},{'of':frozenset({('a','b')})}).true(('member',('some','of',('atom','G')),'b')) and 'b' not in {'a'},
    }
    if not all(checks.values()):raise RuntimeError(checks)
    counts['countermodels']=checks
    print(json.dumps(counts,indent=2,sort_keys=True))
if __name__=='__main__':run()
