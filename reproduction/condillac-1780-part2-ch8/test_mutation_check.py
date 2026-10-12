import unittest
from mutation_check import classify, run, strict_equal


def crash():
    raise RuntimeError('deliberate harness diagnostic')


class MutationHarnessTests(unittest.TestCase):
    def test_kill_and_survival_are_distinct(self):
        self.assertEqual(classify(lambda:1,lambda:2,1).status,'killed')
        self.assertEqual(classify(lambda:1,lambda:1,1).status,'survived')

    def test_invalid_baseline_is_not_a_kill(self):
        self.assertEqual(classify(lambda:2,lambda:3,1).status,'invalid_baseline')

    def test_baseline_exception_is_not_a_kill(self):
        result=classify(crash,lambda:2,1)
        self.assertEqual(result.status,'baseline_error')
        self.assertEqual(result.error_type,'RuntimeError')

    def test_mutant_exception_is_not_a_kill(self):
        result=classify(lambda:1,crash,1)
        self.assertEqual(result.status,'mutant_error')
        self.assertEqual(result.error_type,'RuntimeError')

    def test_bool_and_int_observations_do_not_alias(self):
        self.assertFalse(strict_equal(True,1))
        self.assertFalse(strict_equal((True,), (1,)))
        self.assertFalse(strict_equal({'x':True},{'x':1}))
        self.assertFalse(strict_equal({True:'x'},{1:'x'}))
        self.assertFalse(strict_equal({'outer':{True:'x'}},{'outer':{1:'x'}}))
        self.assertEqual(classify(lambda:1,lambda:True,1).status,'killed')

    def test_all_behavioral_faults_are_detected(self):
        results=run()
        self.assertEqual(len(results),13)
        self.assertTrue(all(item['status']=='killed' for item in results.values()))


if __name__=='__main__': unittest.main()
