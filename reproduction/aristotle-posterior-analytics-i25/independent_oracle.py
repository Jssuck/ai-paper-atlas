"""Independent audit: preorder enumeration and elementwise quantifiers.
Run in this directory. Standard library only. Not a scientific-cause verifier.
"""
import itertools, json, math
from pathlib import Path
import model

def check(condition, message):
    if not condition: raise RuntimeError(message)

def tree_oracle():
    rows=[]
    for n in range(7):
        a=e=shapes=patterns=0
        # Enumerate strings of internal(1)/leaf(0) tokens by positions,
        # not the implementation's recursive Cartesian shape builder.
        for positions in itertools.combinations(range(2*n+1), n):
            selected=set(positions)
            word=[int(i in selected) for i in range(2*n+1)]
            slots=1; valid=True
            for bit in word:
                if slots==0: valid=False; break
                slots += 1 if bit else -1
            if not valid or slots: continue
            shapes+=1
            for leaves in itertools.product((0,1),repeat=n+1):
                patterns+=1
                # Reverse-prefix stack parser; 0=A and 1=E.
                stack=[]; cursor=n; permitted=True
                for token in reversed(word):
                    if token==0:
                        stack.append((leaves[cursor],leaves[cursor],1));cursor-=1
                    else:
                        left=stack.pop();right=stack.pop()
                        if left[0]+right[0]>1: permitted=False;break
                        stack.append((left[0]+right[0],left[1]+right[1],left[2]+right[2]))
                if not permitted: continue
                check(len(stack)==1,'parser root')
                polarity,negative,total=stack[0]
                check(total==n+1 and negative==polarity,'leaf invariant')
                if polarity: e+=1
                else:a+=1
        actual=model.tree_experiment(n)[-1]
        check((shapes,a,e)==(actual['shapes'],actual['affirmative_proofs'],actual['negative_proofs']),'tree count disagreement')
        check(shapes==math.comb(2*n,n)//(n+1),'Catalan formula')
        rows.append(dict(internal_nodes=n,shapes=shapes,leaf_labelings_checked=patterns,affirmative=a,negative=e))
    return rows

def sets(nmax,arity,expanded):
    assigned=satisfied=bad=0
    for n in range(nmax+1):
        # Each object's membership vector is a tuple of booleans.
        for world in itertools.product(tuple(itertools.product((False,True),repeat=arity)),repeat=n):
            assigned+=1
            if expanded:
                premise=all(not (a and d) and (not b or d) and (not t or b) and (not c or t) for a,b,c,d,t in world)
            else:
                premise=all(not (a and b) and (not c or b) for a,b,c in world)
            conclusion=all(not (row[0] and row[2]) for row in world)
            if premise: satisfied+=1;bad+=not conclusion
    return dict(assignments=assigned,satisfying_premises=satisfied,counterexamples=bad)

def main():
    rows=tree_oracle();direct=sets(5,3,False);expanded=sets(3,5,True)
    implementation=model.set_experiment()
    check(sets(4,3,False)==implementation['direct_celarent'],'direct disagreement')
    check(expanded==implementation['expanded_celarent'],'expanded disagreement')
    check(direct['counterexamples']==expanded['counterexamples']==0,'semantic counterexample')
    return {'method':'Independent preorder/stack enumeration and per-object quantified membership; implementation used only for final comparisons','trees':rows,'direct_extended_to_domain_5':direct,'expanded_domain_0_to_3':expanded,'disagreements':0}
if __name__=='__main__':
    print(json.dumps(main(),ensure_ascii=False,indent=2))
