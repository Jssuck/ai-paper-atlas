"""Independent fixed-point oracle; exhaustive three-name rule-input subsets.
Not a general proof and not a claim of semantic completeness.
"""
import itertools,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from model import KnowledgeBase,Inclusion,Exclusion

def require(ok,msg):
    if not ok:raise RuntimeError(msg)

def sublists(edges):
    for bits in range(1<<len(edges)):
        yield [e for i,e in enumerate(edges) if bits&(1<<i)]

def fixedpoint(names,inc,exc):
    a=set(inc)|{(x,x) for x in names}; e=set(exc)|{(y,x) for x,y in exc}
    while True:
        na=a|{(x,z) for x,y in a for yy,z in a if y==yy}
        ne=e|{(x,z) for x,y in na for yy,z in e if y==yy}
        ne|={(z,x) for x,z in ne}
        if na==a and ne==e:return a,e
        a,e=na,ne

def exhaustive_rule_inputs():
    names=('a','b','c'); pos=list(itertools.product(names,repeat=2))
    neg=list(itertools.combinations_with_replacement(names,2))
    count=queries=certificates=0
    for inc in sublists(pos):
        for exc in sublists(neg):
            k=KnowledgeBase(names,inc,exc); a,e=fixedpoint(names,inc,exc);count+=1
            for x,y in pos:
                for fn,expected in ((k.inclusion,a),(k.exclusion,e)):
                    p=fn(x,y);queries+=1
                    require((p is not None)==((x,y) in expected),'fixedpoint mismatch')
                    if p is not None:
                        require(k.verify(x,y,p),'certificate rejected');certificates+=1
    return {'knowledge_bases':count,'queries':queries,'certificates':certificates}

def finite_semantics():
    names=('a','b'); pos=list(itertools.product(names,repeat=2)); neg=list(itertools.combinations_with_replacement(names,2))
    subsets=[set(i for i in range(2) if bits&(1<<i)) for bits in range(4)]
    count=checks=0
    for inc in sublists(pos):
        for exc in sublists(neg):
            k=KnowledgeBase(names,inc,exc)
            for values in itertools.product(subsets,repeat=2):
                ext=dict(zip(names,values))
                if not all(ext[x]<=ext[y] for x,y in inc) or not all(not (ext[x]&ext[y]) for x,y in exc):continue
                count+=1
                for x,y in pos:
                    if k.inclusion(x,y) is not None:
                        require(ext[x]<=ext[y],'unsound inclusion');checks+=1
                    if k.exclusion(x,y) is not None:
                        require(not (ext[x]&ext[y]),'unsound exclusion');checks+=1
    return {'satisfying_kb_interpretation_pairs':count,'semantic_checks':checks}

def malformed_and_boundaries():
    k=KnowledgeBase(('a','b','c'),(('a','b'),('b','a')),(('b','c'),))
    forged=[Inclusion(('a','c')),Inclusion(('b','a')),Inclusion(('a',)),Inclusion(('a','b',[])),Inclusion('ab'),Exclusion(('a','b'),('c',),('c','b')),Exclusion(('a','b'),('a',),('b','c')),Exclusion(('a',),('c',),('b','c')),object()]
    for p in forged: require(not k.verify('a','c',p),'forged/malformed accepted')
    # Repeated edges yield a valid path certificate even if not BFS-shortest.
    require(k.verify('a','b',Inclusion(('a','b','a','b'))),'valid cyclic certificate')
    empty=KnowledgeBase(('a','b'),(),(('a','a'),))
    require(empty.inclusion('a','b') is None,'unexpected semantic completion')
    require(empty.exclusion('a','a') is not None,'missing self-disjoint')
    return {'rejected_certificates':len(forged),'additional_boundary_checks':3}

print(json.dumps({'rule_inputs':exhaustive_rule_inputs(),'two_element_semantics':finite_semantics(),'boundaries':malformed_and_boundaries()},sort_keys=True))
