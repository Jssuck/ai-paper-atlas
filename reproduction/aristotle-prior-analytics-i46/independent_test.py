"""Independent pointwise oracles, not the author's enumeration implementation."""
import itertools
import unittest
import model

STATS = {'scope_cases':0,'inclusion_cases':0,'quantifier_cases':0,'ability_cases':0}

def choose(u, bits):
    return {x for x, b in zip(u,bits) if b}

class IndependentTests(unittest.TestCase):
    def test_scope_pointwise(self):
        for n in range(7):
            u = tuple('p'+str(i) for i in range(n))
            # 0 outside applicability, 1 applicable negative, 2 positive.
            for states in itertools.product(range(3),repeat=n):
                t = {x for x,s in zip(u,states) if s>0}
                p = {x for x,s in zip(u,states) if s==2}
                q = model.scope_square(u,t,p)
                for x,s in zip(u,states):
                    expected = [(False,True,False,True), (False,True,True,False), (True,False,False,True)][s]
                    self.assertEqual(tuple(x in k for k in (q.A,q.B,q.C,q.D)),expected)
                self.assertEqual(q.B & q.D, set(u)-t)
                self.assertEqual(q.C==q.B,t==set(u))
                self.assertEqual(q.A==q.D,t==set(u))
                STATS['scope_cases']+=1
    def test_inclusion_pointwise(self):
        for n in range(7):
            u=tuple('q'+str(i) for i in range(n))
            for states in itertools.product(range(3),repeat=n):
                # outside A, A minus C, inside C
                a={x for x,s in zip(u,states) if s>0}
                c={x for x,s in zip(u,states) if s==2}
                q=model.complement_inclusion(u,c,a)
                for x,s in zip(u,states):
                    self.assertEqual((x in q['B'],x in q['D']),[(True,True),(False,True),(False,False)][s])
                self.assertEqual(q['B']<q['D'], any(s==1 for s in states))
                self.assertEqual(q['D']<=q['B'],a==c)
                STATS['inclusion_cases']+=1
    def test_quantifier_pointwise(self):
        for n in range(7):
            u=tuple('r'+str(i) for i in range(n))
            for states in itertools.product(range(4),repeat=n):
                s={x for x,k in zip(u,states) if k&1}
                p={x for x,k in zip(u,states) if k&2}
                q=model.quantifiers(u,s,p)
                all_yes=all(not(k&1) or bool(k&2) for k in states)
                some_no=any((k&1) and not(k&2) for k in states)
                all_no=all(not(k&1) or not(k&2) for k in states)
                self.assertEqual(q,{'all':all_yes,'not_all':not all_yes,'some_not':some_no,'all_not':all_no})
                STATS['quantifier_cases']+=1
    def test_joint_denial_truth_table(self):
        u=('x','y','z')
        for a_bits in itertools.product([False,True],repeat=3):
            for b_bits in itertools.product([False,True],repeat=3):
                a,b=choose(u,a_bits),choose(u,b_bits)
                self.assertEqual(model.joint_denial(u,a,b),{x for x,aa,bb in zip(u,a_bits,b_bits) if not aa and not bb})
        self.assertEqual(model.joint_denial(u,{'x'},{'y','z'}),set())
    def test_ability_pointwise(self):
        for n in range(7):
            for values in itertools.product([False,True],repeat=n):
                q=model.abilities(iter(values))
                self.assertEqual(q,{'can_walk':True in values,'can_not_walk':False in values,'not_can_walk':True not in values})
                STATS['ability_cases']+=1
        self.assertEqual(model.abilities([True,False]),{'can_walk':True,'can_not_walk':True,'not_can_walk':False})
    def test_countermodels(self):
        q=model.scope_square(['w','b','s'],['w','b'],['w'])
        self.assertEqual(q.B-q.C,{'s'})
        self.assertEqual(q.D-q.A,{'s'})
        self.assertFalse(model.quantifiers(['w','b'],['w','b'],['w'])['all_not'])
        self.assertTrue(model.quantifiers(['w','b'],['w','b'],['w'])['not_all'])
    def test_empty_edges(self):
        q=model.scope_square([],[],[])
        self.assertEqual(q.A|q.B|q.C|q.D,set())
        self.assertEqual(model.quantifiers(['x'],[],[]),{'all':True,'not_all':False,'some_not':False,'all_not':True})
        self.assertEqual(model.abilities([]),{'can_walk':False,'can_not_walk':False,'not_can_walk':True})
    def test_invalid_and_late_inputs(self):
        cases=[lambda:model.scope_square(['x'],['x'],['y']),lambda:model.scope_square(['x'],[],['x']),lambda:model.quantifiers(['x'],[],['y']),lambda:model.complement_inclusion(['x'],['x'],[]),lambda:model.joint_denial(['x'],[],['y'])]
        for f in cases:
            with self.assertRaises(ValueError): f()
        for bad in [None,1,'x',[True],['x',None],['']]:
            with self.assertRaises(TypeError): model.scope_square(bad,[],[])
        for bad in [[True,0],[False,'false'],'false',None]:
            with self.assertRaises(TypeError): model.abilities(bad)
    def test_generator_immutability(self):
        u=['x','y']; t=['x']; p=['x']
        q=model.scope_square(iter(u),iter(t),iter(p))
        u.append('z');t.clear();p.clear()
        self.assertEqual(q.universe,{'x','y'})
        self.assertEqual(q.A,{'x'})
    def test_subset_generator_validation(self):
        self.assertEqual(set(model.subsets(['x','x','y'])),{frozenset(),frozenset(['x']),frozenset(['y']),frozenset(['x','y'])})
        with self.assertRaises(TypeError): list(model.subsets(iter(['x',False])))

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(IndependentTests))
    print('Independent pointwise counts:',STATS,flush=True)
    if not result.wasSuccessful(): raise SystemExit(1)
