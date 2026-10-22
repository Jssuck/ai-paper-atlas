import unittest
from model import Model, models, named_models
from demo import run

class ModelTests(unittest.TestCase):
    def test_missing_bridge(self):
        m=named_models()['missing_persistence']
        self.assertTrue(m.categorical('A','B','E'))
        self.assertTrue(m.categorical('A','C','A','contingent'))
        self.assertFalse(m.categorical('B','C','E','possible'))
        self.assertFalse(m.persistent_exclusion('A','B'))

    def test_bridge_not_actual(self):
        m=named_models()['bridge_without_actual_conclusion']
        self.assertTrue(m.persistent_exclusion('A','B'))
        self.assertTrue(m.categorical('A','C','A','contingent'))
        self.assertTrue(m.categorical('B','C','E','possible'))
        self.assertFalse(m.categorical('B','C','E'))

    def test_bridge_not_strict(self):
        m=named_models()['bridge_without_strict_conclusion']
        self.assertTrue(m.persistent_exclusion('A','B'))
        self.assertTrue(m.categorical('A','C','A','contingent'))
        self.assertTrue(m.categorical('B','C','E','necessary'))
        self.assertFalse(m.categorical('B','C','E','contingent'))

    def test_no_modal_conversion(self):
        m=named_models()['possible_negative_not_convertible']
        self.assertTrue(m.categorical('C','B','E','possible'))
        self.assertFalse(m.categorical('B','C','E','possible'))

    def test_objectwise_not_joint(self):
        m=named_models()['objectwise_not_joint']
        self.assertTrue(m.categorical('B','C','E','possible'))
        self.assertFalse(m.jointly_possible('B','C',False))

    def test_vacuity_not_existence(self):
        m=named_models()['empty_subject']
        for mode in ('actual','possible','necessary','contingent'):
            self.assertTrue(m.categorical('A','C','A',mode))
            self.assertFalse(m.categorical('A','C','I',mode))

    def test_actual_index(self):
        m=Model(1,((0,1,1),(1,1,1)),1)
        self.assertTrue(m.categorical('A','B','A'))
        self.assertEqual(m.extension('A'),frozenset({0}))

    def test_immutable(self):
        with self.assertRaises(AttributeError):
            named_models()['missing_persistence'].n=2

    def test_constructor_errors(self):
        bad=[(0,((0,0,0),),0),(-1,((0,0,0),),0),(True,((0,0,0),),0),
             (1,[],0),(1,(),0),(1,([0,0,0],),0),(1,((0,0),),0),
             (1,((2,0,0),),0),(1,((-1,0,0),),0),(1,((False,0,0),),0),
             (1,((0.,0,0),),0),(1,((0,0,0),),-1),(1,((0,0,0),),1),
             (1,((0,0,0),),False)]
        for args in bad:
            with self.subTest(args=args),self.assertRaises(ValueError): Model(*args)

    def test_method_errors(self):
        m=named_models()['empty_subject']
        calls=[lambda:m.extension('D'),lambda:m.extension(None),lambda:m.extension('A',2),
               lambda:m.extension('A',True),lambda:m.categorical('D','C','A'),
               lambda:m.categorical('A','D','A'),lambda:m.categorical('A','C','X'),
               lambda:m.categorical('A','C','A','Q'),lambda:m.persistent_exclusion('A','D'),
               lambda:m.rigid('D'),lambda:m.jointly_possible('D','C'),
               lambda:m.jointly_possible('A','C',1)]
        for call in calls:
            with self.assertRaises(ValueError):call()

    def test_generator_errors(self):
        for args in ((0,2),(1,0),(True,2),(1,True),(1,2.0)):
            with self.assertRaises(ValueError):next(models(*args))

    def test_generator_cardinality(self):
        self.assertEqual(sum(1 for _ in models(1)),128)
        self.assertEqual(sum(1 for _ in models(2)),8192)

    def test_full_sweep(self):
        r=run()
        self.assertEqual(r['configurations'],8320)
        self.assertEqual(r['contingent_quality_equivalences'],149760)
        self.assertEqual(len(r['failed_family_pairs']),24)
        self.assertGreater(r['forward_bridge_cases'],0)
        self.assertGreater(r['reverse_rigid_bridge_cases'],0)
        self.assertGreater(r['raw_rule_counterexamples'],0)

if __name__=='__main__':unittest.main(verbosity=2)
