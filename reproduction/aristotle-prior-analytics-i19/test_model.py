import unittest
from modal_model import Model
from examples import examples, make

class ModelTests(unittest.TestCase):
    def test_basic_four_forms(self):
        m=make([0,1],[({0},{0,1},set())])
        self.assertEqual([m.eval('D',f,'A','B') for f in 'aeio'],[False,False,True,True])
        self.assertEqual([m.eval('D',f,'B','A') for f in 'aeio'],[True,False,True,False])

    def test_empty_terms(self):
        m=make([0],[(set(),set(),set())])
        for mode in ('D','N','C','P','Box'):
            self.assertEqual([m.eval(mode,f,'A','B') for f in 'aeio'],[True,True,False,False])

    def test_one_world_contingency(self):
        m=make([0],[({0},{0},{0})])
        for f in 'aeio': self.assertFalse(m.eval('C',f,'A','B'))

    def test_actual_not_zero(self):
        m=make([0],[({0},{0},{0}),(set(),{0},{0})],actual=1)
        self.assertTrue(m.eval('D','e','A','B'))
        self.assertFalse(m.eval('D','a','A','B'))
        self.assertTrue(m.eval('C','a','A','B'))

    def test_copy_and_freeze(self):
        world={'A':{0},'B':{0},'C':{0}}
        m=Model([0],[world]); world['A'].clear()
        self.assertTrue(m.eval('D','a','A','B'))
        with self.assertRaises(TypeError): m.worlds[0]['A']=frozenset()
        with self.assertRaises(AttributeError): m.actual=2

    def test_domain_validation(self):
        for d in (None,1,'x',iter([0]),{True},{0.0}):
            with self.assertRaises(TypeError): Model(d,[{'A':set(),'B':set(),'C':set()}])
        with self.assertRaises(ValueError): Model([], [{'A':set(),'B':set(),'C':set()}])

    def test_world_validation(self):
        for w in (None,1,'x',iter([])):
            with self.assertRaises(TypeError): Model([0],w)
        with self.assertRaises(ValueError): Model([0],[])
        with self.assertRaises(TypeError): Model([0],[[]])
        for w in ({'A':set(),'B':set()}, {'A':set(),'B':set(),'C':set(),'D':set()},
                  {'A':{1},'B':set(),'C':set()}):
            with self.assertRaises(ValueError): Model([0],[w])
        for x in (None,'x',1,{True},{0.0}):
            with self.assertRaises(TypeError): Model([0],[{'A':x,'B':set(),'C':set()}])

    def test_actual_validation(self):
        w=[{'A':set(),'B':set(),'C':set()}]
        for a in (True,False,None,0.0,'0'):
            with self.assertRaises(TypeError): Model([0],w,a)
        for a in (-1,1,2):
            with self.assertRaises(ValueError): Model([0],w,a)

    def test_query_validation(self):
        m=examples()['awake']; good=['D','a','A','B']
        for i in range(4):
            for x in (None,True,[],0):
                q=good.copy();q[i]=x
                with self.assertRaises(TypeError): m.eval(*q)
            q=good.copy();q[i]='unknown'
            with self.assertRaises(ValueError): m.eval(*q)

    def test_weak_not_necessary(self):
        m=examples()['weak_not_necessary']
        self.assertTrue(m.eval('N','e','A','B') and m.eval('C','a','A','C'))
        self.assertTrue(m.eval('D','e','B','C') and m.eval('P','e','B','C'))
        self.assertFalse(m.eval('N','e','B','C'))

    def test_weak_not_strong(self):
        m=examples()['weak_not_strong']
        self.assertTrue(m.eval('N','e','A','B') and m.eval('C','a','A','C'))
        self.assertTrue(m.eval('D','e','B','C') and m.eval('P','e','B','C'))
        self.assertFalse(m.eval('C','e','B','C'))

    def test_conversion_failure(self):
        m=examples()['conversion_fails']
        self.assertTrue(m.eval('N','e','A','B'));self.assertFalse(m.eval('N','e','B','A'))

    def test_awake_semantics_difference(self):
        m=examples()['awake']
        self.assertTrue(m.eval('Box','a','A','C') and m.eval('C','a','A','B'))
        self.assertTrue(m.eval('D','a','B','C'));self.assertFalse(m.eval('D','e','B','C'))
        self.assertFalse(m.eval('N','a','A','C'))
        n=examples()['anchored_affirmative']
        self.assertTrue(n.eval('N','a','A','C') and n.eval('C','a','A','B'))
        self.assertTrue(n.eval('D','e','B','C'))

    def test_reverse_particular(self):
        m=examples()['reverse_particular']
        self.assertTrue(m.eval('N','e','A','C') and m.eval('C','i','A','B'))
        self.assertTrue(m.eval('D','o','C','B'));self.assertFalse(m.eval('D','o','B','C'))

    def test_particular_negative_insufficient(self):
        m=examples()['particular_negative']
        self.assertTrue(m.eval('N','o','A','B') and m.eval('C','a','A','C'))
        self.assertFalse(m.eval('D','e','B','C'));self.assertFalse(m.eval('D','o','B','C'))

    def test_box_negative_insufficient(self):
        m=examples()['box_negative']
        self.assertTrue(m.eval('Box','e','A','B') and m.eval('C','a','A','C'))
        self.assertFalse(m.eval('N','e','A','B'));self.assertFalse(m.eval('D','e','B','C'))

    def test_particular_necessary_witness_order(self):
        m=make([0,1],[({0},{0,1},set()),({1},{0,1},set())])
        self.assertTrue(m.eval('Box','i','A','B'));self.assertFalse(m.eval('N','i','A','B'))

if __name__=='__main__': unittest.main(verbosity=2)
