"""Original, restricted teaching models for Posterior Analytics I.25.
No empirical cognition or causal-scientific claim is inferred from these models.
"""
from dataclasses import dataclass
from functools import lru_cache
from itertools import product
import json

@dataclass(frozen=True)
class Proof:
    polarity: str
    children: tuple = ()

    def validate(self):
        if self.polarity not in ('A', 'E'):
            raise ValueError('Only universal affirmative A and universal negative E')
        if not self.children:
            return self
        if len(self.children) != 2:
            raise ValueError('Binary inference only')
        for child in self.children:
            if not isinstance(child, Proof):
                raise ValueError('Children must be proofs')
            child.validate()
        labels = tuple(c.polarity for c in self.children)
        if self.polarity == 'A' and labels != ('A', 'A'):
            raise ValueError('A requires AA')
        if self.polarity == 'E' and labels not in (('A', 'E'), ('E', 'A')):
            raise ValueError('E requires exactly one E')
        return self

    def leaves(self):
        self.validate()
        return (self.polarity,) if not self.children else sum((c.leaves() for c in self.children), ())

    def internal_nodes(self):
        self.validate()
        return 0 if not self.children else 1 + sum(c.internal_nodes() for c in self.children)

@lru_cache(None)
def shapes(n):
    """All ordered full binary tree shapes with n internal nodes."""
    if not isinstance(n, int) or n < 0:
        raise ValueError('Nonnegative integer required')
    if n == 0:
        return (None,)
    return tuple((l, r) for k in range(n) for l in shapes(k) for r in shapes(n-1-k))

def label(shape, negative_leaf=None):
    """One optional negative leaf; propagate its type along its ancestor path."""
    if negative_leaf is not None and (not isinstance(negative_leaf, int) or negative_leaf < 0):
        raise ValueError('Invalid leaf index')
    counter = [0]
    def visit(s):
        if s is None:
            p = Proof('E' if counter[0] == negative_leaf else 'A')
            counter[0] += 1
            return p
        l, r = visit(s[0]), visit(s[1])
        return Proof('E' if 'E' in (l.polarity, r.polarity) else 'A', (l, r))
    p = visit(shape)
    if negative_leaf is not None and negative_leaf >= counter[0]:
        raise ValueError('Leaf index outside tree')
    return p.validate()

def tree_experiment(max_internal=6):
    rows=[]
    for n in range(max_internal+1):
        counts={'internal_nodes':n, 'shapes':len(shapes(n)), 'affirmative_proofs':0, 'negative_proofs':0, 'violations':0}
        for s in shapes(n):
            a=label(s); counts['affirmative_proofs']+=1
            counts['violations'] += int(a.leaves().count('E') != 0 or len(a.leaves()) != n+1)
            for i in range(n+1):
                p=label(s,i); counts['negative_proofs']+=1
                counts['violations'] += int(p.leaves().count('E') != 1 or len(p.leaves()) != n+1 or p.internal_nodes()!=n)
        rows.append(counts)
    return rows

def subset(x,y):
    return x & ~y == 0

def disjoint(x,y):
    return x & y == 0

def set_experiment():
    direct={'assignments':0, 'satisfying_premises':0, 'counterexamples':0}
    for n in range(5):
        for a,b,c in product(range(1<<n), repeat=3):
            direct['assignments']+=1
            if disjoint(a,b) and subset(c,b):
                direct['satisfying_premises']+=1
                direct['counterexamples']+=int(not disjoint(a,c))
    expanded={'assignments':0, 'satisfying_premises':0, 'counterexamples':0}
    for n in range(4):
        for a,b,c,d,e_term in product(range(1<<n),repeat=5):
            expanded['assignments']+=1
            if disjoint(a,d) and subset(b,d) and subset(e_term,b) and subset(c,e_term):
                expanded['satisfying_premises']+=1
                expanded['counterexamples']+=int(not disjoint(a,c))
    return {'direct_celarent':direct,'expanded_celarent':expanded}

def cost_example():
    """Declared additive costs, not measured seconds or human familiarity."""
    short=(10,10); long=(1,1,1)
    return {'equal_unit_cost':{'short':2,'long':3}, 'unequal_cost':{'short':sum(short),'long':sum(long)},'unequal_premise_costs':{'short':list(short),'long':list(long)}}

def counterexamples():
    # A=C={0}, B={1}: both A/B and B/C disjoint, but A/C overlap.
    a,b,c=1,2,1
    return {'two_negative_premises':{'A':a,'B':b,'C':c,'premises_true':disjoint(a,b) and disjoint(b,c),'claimed_negative_conclusion':disjoint(a,c)},'redundant_negative_premise':{'A':1,'B':2,'C':2,'D':4,'premises_true':disjoint(1,2) and subset(2,2) and disjoint(1,4),'conclusion_true':disjoint(1,2),'negative_assumptions_listed':2,'explanation':'The unused A/D assumption is not a leaf of the reduced Celarent derivation.'}}

def run():
    return {'scope':'Restricted polarity trees, finite extensional sets, declared additive cost only','trees':tree_experiment(),'sets':set_experiment(),'costs':cost_example(),'counterexamples':counterexamples()}

if __name__=='__main__':
    print(json.dumps(run(),ensure_ascii=False,indent=2))
