"""Independent reviewer checks; matrix and direct finite-state oracles.
Run from reproduction root: python3 code-review/check_independent.py
"""
import sys, json, itertools
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import model

def require(condition, message):
    if not condition: raise RuntimeError(message)

def warshall(edges, labels):
    # No identity initialization: this is positive-length reachability.
    m=[[int((a,b) in edges) for b in labels] for a in labels]
    for k in range(len(labels)):
        for i in range(len(labels)):
            for j in range(len(labels)):
                m[i][j] = m[i][j] or (m[i][k] and m[k][j])
    return {(a,b) for i,a in enumerate(labels) for j,b in enumerate(labels) if m[i][j]}

def proof_state(edges, steps):
    # Oracle is integer bit state over the nine possible ordered pairs.
    def bit(a,b): return 1 << (3*'ABC'.index(a)+'ABC'.index(b))
    known=sum(bit(a,b) for a,b in set(edges)); produced=0
    for a,m,b in steps:
        if not (known & bit(a,m) and known & bit(m,b)): return None
        known |= bit(a,b); produced |= bit(a,b)
    return {(a,b) for a,b in itertools.product('ABC',repeat=2) if produced & bit(a,b)}

def malformed(call):
    try: call()
    except ValueError: return
    raise RuntimeError('malformed input accepted')

def shapes(k):
    if k==0: yield None
    else:
        for i in range(k):
            for a in shapes(i):
                for b in shapes(k-1-i): yield (a,b)

def materialize(shape, counter):
    if shape is None:
        a=next(counter);return ('given',str(a),str(a+1)),a,a+1
    l,a,m=materialize(shape[0],counter)
    r,m2,b=materialize(shape[1],counter)
    require(m==m2,'reviewer tree construction')
    return ('via',l,r),a,b

def run():
    graph_cases=0
    pairs=list(itertools.product('ABCD',repeat=2))
    for mask in range(1<<16):
        edges={e for i,e in enumerate(pairs) if mask>>i&1}
        require(model.closure(edges)==warshall(edges,'ABCD'),f'graph {mask}')
        graph_cases+=1
    triples=list(itertools.product('ABC',repeat=3)); targets=list(itertools.product('ABC',repeat=2))
    pairs3=targets; checks=0
    for mask in range(1<<9):
        edges={e for i,e in enumerate(pairs3) if mask>>i&1}
        for step in triples:
            expected=proof_state(edges,[step])
            for target in targets:
                require(model.verify_certificate(edges,[step],target)==(expected is not None and target in expected),'one-step certificate')
                checks+=1
    # All loop-free 3-label inputs and ordered pairs of steps.
    pairs6=[(a,b) for a,b in targets if a!=b]; two=0
    for mask in range(1<<6):
        edges={e for i,e in enumerate(pairs6) if mask>>i&1}
        for s1,s2 in itertools.product(triples,repeat=2):
            expected=proof_state(edges,[s1,s2])
            for target in targets:
                require(model.verify_certificate(edges,[s1,s2],target)==(expected is not None and target in expected),'two-step certificate')
                two+=1
    chain_cases=0
    for n in range(2,24):
        names=[f'x{i}' for i in range(n)]
        got=model.chain_report(names)
        wanted={(names[i],names[j]) for i in range(n) for j in range(i+2,n)}
        require(set(got['conclusions'])==wanted,'chain set')
        require(got['conclusion_count']==len(wanted),'chain count')
        require(set(got['premises'])==set(zip(names,names[1:])),'chain edges')
        chain_cases+=1
    trees=0
    for k in range(7):
        for shape in shapes(k):
            tree,a,b=materialize(shape,iter(range(k+1)))
            got=model.proof_tree_stats(tree)
            require(got=={'conclusion':(str(a),str(b)), 'inferences':k,'leaf_occurrences':k+1,'premise_slots':2*k,'node_occurrences':2*k+1},'tree shape')
            trees+=1
    shared=('via',('given','A','B'),('given','B','A'))
    require(model.proof_tree_stats(('via',shared,shared))['node_occurrences']==7,'shared occurrence unfolding')
    require(model.verify_certificate([('A','B')],[],('A','B')) is False,'input-only target')
    require(model.verify_certificate([('A','B'),('B','C')],[('A','B','C'),('C','A','B')],('A','C')) is False,'reject invalid suffix after target')
    bad=[lambda:model.closure(None),lambda:model.closure('AB'),lambda:model.closure([('A',False)]),lambda:model.closure([('A',)]),lambda:model.chain_report(['A','A']),lambda:model.chain_report('AB'),lambda:model.chain_report([' A','B']),lambda:model.verify_certificate([],['ABC'],('A','C')),lambda:model.verify_certificate([],[],('A',)),lambda:model.proof_tree_stats(('bad','A','B')),lambda:model.proof_tree_stats(('via',('given','A','B'),('given','C','D')))]
    for call in bad:malformed(call)
    tree=('given','A','A')
    for _ in range(202):tree=('via',tree,('given','A','A'))
    malformed(lambda:model.proof_tree_stats(tree))
    return {'status':'passed','four_label_graphs':graph_cases,'single_step_target_checks':checks,'two_step_target_checks':two,'chain_sizes':chain_cases,'tree_shapes':trees,'malformed_cases':len(bad)+1,'extra_checks':['shared tree occurrences','input-only target','invalid suffix after target'],'limitations':'Finite input sets; no proof of all programs, historical semantics, or resource bounds.'}
if __name__=='__main__': print(json.dumps(run(),indent=2,ensure_ascii=False))
