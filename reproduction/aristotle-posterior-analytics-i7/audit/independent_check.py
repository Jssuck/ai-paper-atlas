"""Independent finite policy and semantic checks; no production oracle used."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import itertools
import unittest
from model import Atom, Rule, Bridge, Step, allowed, verify, closure

class IndependentChecks(unittest.TestCase):
    def test_policy_table(self):
        domains=('X','Y','Z')
        atoms=[Atom(d,p) for d in domains for p in ('p','q')]
        pairs=[(x,y) for x in domains for y in domains if x!=y]
        count=0
        for mask in range(64):
            edges=[pair for k,pair in enumerate(pairs) if mask & (1<<k)]
            registry=[Bridge('link-'+str(k),Atom(x,'p'),Atom(y,'p')) for k,(x,y) in enumerate(pairs) if (x,y) in edges]
            for a,b in itertools.product(atoms, repeat=2):
                if a.domain==b.domain:
                    r=Rule(a,b,'common')
                    expected=True
                else:
                    k=pairs.index((a.domain,b.domain))
                    r=Rule(a,b,'bridge','link-'+str(k))
                    expected=(a.predicate=='p' and b.predicate=='p' and bool(mask & (1<<k)))
                self.assertEqual(allowed(r,registry),expected)
                count+=1
        self.assertEqual(count,2304)

    def test_independent_material_models(self):
        atoms=[Atom('X','p'),Atom('X','q'),Atom('Y','p'),Atom('Y','q')]
        a,b,c,d=atoms
        candidates=[Rule(a,b),Rule(c,d,'common'),Rule(b,c,'bridge','bc'),Rule(d,a,'bridge','da')]
        count=0
        for rulebits,bridgebits,factbits in itertools.product(range(16),range(4),range(16)):
            rs=[r for i,r in enumerate(candidates) if rulebits & (1<<i)]
            bs=[]
            if bridgebits&1:bs.append(Bridge('bc',b,c))
            if bridgebits&2:bs.append(Bridge('da',d,a))
            facts=[x for i,x in enumerate(atoms) if factbits & (1<<i)]
            # Four fixed semantic edges, selected without allowed/production oracle.
            index_edges=[]
            for i,(src,dst) in enumerate([(0,1),(2,3),(1,2),(3,0)]):
                if (rulebits & (1<<i)) and (i<2 or bridgebits & (1<<(i-2))):
                    index_edges.append((src,dst))
            models=[]
            for val in range(16):
                if (val & factbits)!=factbits:continue
                if all(not (val & (1<<u)) or (val & (1<<v)) for u,v in index_edges):models.append(val)
            self.assertGreater(len(models),0)
            expected={atoms[i] for i in range(4) if all(v & (1<<i) for v in models)}
            self.assertEqual(closure(facts,rs,bs),expected)
            count+=1
        self.assertEqual(count,1024)

    def test_semantic_false_bridge(self):
        a,b=Atom('X','true'),Atom('Y','false')
        bridge=Bridge('bad',a,b)
        self.assertTrue(verify([a],[Step(Rule(a,b,'bridge','bad'),0)],b,[bridge]))
        valuation={a:True,b:False}
        self.assertFalse((not valuation[a]) or valuation[b])

    def test_no_laundering_and_exact_direction(self):
        a,b,c=Atom('X','p'),Atom('Y','p'),Atom('Y','beauty')
        bs=[Bridge('b',a,b)]
        for r in [Rule(a,b,'local'),Rule(a,b,'common'),Rule(b,a,'bridge','b'),Rule(a,c,'bridge','b'),Rule(a,b,'bridge','wrong')]:
            self.assertFalse(verify([r.source],[Step(r,0)],r.target,bs))

    def test_sequence_integrity(self):
        a,b,c=Atom('X','p'),Atom('X','q'),Atom('Y','q')
        bs=[Bridge('bc',b,c)]
        r1=Rule(a,b);r2=Rule(b,c,'bridge','bc')
        self.assertTrue(verify([a],[Step(r1,0),Step(r2,1)],c,bs))
        for index in [-1,1,True,0.0,'0']:
            self.assertFalse(verify([a],[Step(r1,index)],b))
        self.assertFalse(verify([a],[Step(r2,0)],c,bs))

    def test_cycles_do_not_seed(self):
        a,b=Atom('X','p'),Atom('Y','q')
        bs=[Bridge('ab',a,b),Bridge('ba',b,a)]
        rs=[Rule(a,b,'bridge','ab'),Rule(b,a,'bridge','ba')]
        self.assertEqual(closure([],rs,bs),set())
        self.assertEqual(closure([a],rs,bs),{a,b})

    def test_cube_product_and_sum_boundary(self):
        for m,n in itertools.product(range(-8,9),repeat=2):
            self.assertEqual(m**3*n**3,(m*n)**3)
        self.assertEqual(2**3*3**3,216)
        self.assertFalse(any(k**3==2 for k in range(-2,3)))

    def test_same_domain_not_semantic_truth(self):
        a,b=Atom('X','p'),Atom('X','q')
        self.assertTrue(verify([a],[Step(Rule(a,b),0)],b))
        self.assertFalse((not True) or False)
        self.assertFalse(verify([a],[],b))

if __name__=='__main__':unittest.main(verbosity=2)
