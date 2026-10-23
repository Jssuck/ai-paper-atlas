import unittest
from model import *

class Tests(unittest.TestCase):
    def test_e_i_conversion(self):
        for k in ('E','I'):
            p=prop(k,'S','P'); self.assertEqual(convert(convert(p)),p)
    def test_a_needs_subject_existence(self):
        p=prop('A','S','P')
        for ne in ((),('P',)):
            with self.assertRaises(ValueError): convert(p,ne)
        self.assertEqual(convert(p,('S',)),prop('I','P','S'))
    def test_o_not_convertible(self):
        with self.assertRaises(ValueError): convert(prop('O','S','P'),TERMS)
    def test_invalid_kinds_terms(self):
        for args in [('X','S','P'),('A','X','P'),('A','S','S')]:
            with self.assertRaises(ValueError): prop(*args)
    def test_figures(self):
        for f in (0,4,True):
            with self.assertRaises(ValueError): mood(f,'AAA')
        with self.assertRaises(ValueError): mood(1,'AA')
    def test_explicit_first(self):
        for name in ('Barbara','Celarent','Darii','Ferio'):
            f,l,n=MOODS[name]; a,b,c=mood(f,l); self.assertEqual(first_figure(a,b),c)
    def test_wrong_first_pair(self):
        a,b,c=mood(2,'AOO')
        with self.assertRaises(ValueError): first_figure(a,b)
    def test_direct_certificates(self):
        for premises,steps,c,ne in demonstrations().values():
            self.assertTrue(verify(premises,steps,c,ne))
    def test_indirect_certificates(self):
        for args in indirect_demonstrations().values(): self.assertTrue(reductio(*args))
    def test_wrong_discharge(self):
        p,h,s,r,c=indirect_demonstrations()['Baroco']
        self.assertFalse(reductio(p,h,s,r,prop('O','P','S')))
    def test_forward_refs(self):
        p=prop('E','S','P')
        with self.assertRaises(ValueError): check_steps((p,),(Step('convert',(1,),convert(p)),))
    def test_bad_step_output(self):
        p=prop('E','S','P')
        with self.assertRaises(ValueError): check_steps((p,),(Step('convert',(0,),prop('I','P','S')),))
    def test_bool_index(self):
        with self.assertRaises(ValueError): Step('convert',(True,),prop('E','S','P'))
        args=indirect_demonstrations()['Baroco']
        with self.assertRaises(ValueError): reductio(*args[:3],(True,3),args[4])
    def test_generator_inputs(self):
        p,s,c,ne=demonstrations()['Darapti']
        self.assertTrue(verify(iter(p),iter(s),c,iter(ne)))
    def test_validate_even_unused_existence(self):
        with self.assertRaises(ValueError): convert(prop('E','S','P'),('bad',))
        with self.assertRaises(ValueError): check_steps((),(),('bad',))
    def test_all_moods(self):
        for f,l,ne in MOODS.values():
            a,b,c=mood(f,l); self.assertIsNone(countermodel((a,b),c,ne))
    def test_existence_countermodels(self):
        for name in ('Darapti','Felapton'):
            f,l,ne=MOODS[name]; a,b,c=mood(f,l)
            self.assertIsNotNone(countermodel((a,b),c))
    def test_bad_semantic_inputs(self):
        p=prop('A','S','P')
        with self.assertRaises(ValueError): holds(p,{'S':set()})
        with self.assertRaises(TypeError): holds(p,{'S':[], 'P':set(),'M':set()})
        with self.assertRaises(TypeError): countermodel((p,42),p)
    def test_weak_conversion_not_equivalence(self):
        p=prop('A','S','P'); q=convert(p,('S',))
        self.assertIsNone(countermodel((p,),q,('S',)))
        self.assertIsNotNone(countermodel((q,),p,('S',)))
    def test_invalid_simple_a_and_o(self):
        for k in ('A','O'):
            self.assertIsNotNone(countermodel((prop(k,'S','P'),),prop(k,'P','S'),TERMS))
    def test_model_count(self):
        ms=list(models()); self.assertEqual(len(ms),128)
        self.assertEqual(sum(all(m[t] for t in TERMS) for m in ms),109)

if __name__=='__main__': unittest.main()
