import unittest
from model import Context, Proposition as P, check_chain, evaluate, experiments, powerset


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.major = P('All', 'A', 'B')
        self.minor = P('All', 'B', 'C')
        self.conclusion = P('All', 'A', 'C')

    def check(self, major=None, minor=None, conclusion=None):
        return check_chain(major or self.major, minor or self.minor, conclusion or self.conclusion)

    def test_all_chain(self):
        self.assertEqual(self.check(), (True, 'verified-shape-only'))

    def test_member_chain(self):
        self.assertTrue(self.check(minor=P('Member', 'B', 'c'), conclusion=P('Member', 'A', 'c'))[0])

    def test_some_major_rejected(self):
        self.assertEqual(self.check(major=P('Some', 'A', 'B'))[1], 'major-not-universal')

    def test_member_major_rejected(self):
        self.assertFalse(self.check(major=P('Member', 'A', 'b'))[0])

    def test_some_minor_is_unsupported_not_invalid(self):
        self.assertEqual(self.check(minor=P('Some', 'B', 'C'), conclusion=P('Some', 'A', 'C'))[1], 'unsupported-minor')

    def test_middle_mismatch(self):
        self.assertEqual(self.check(minor=P('All', 'D', 'C'))[1], 'middle-mismatch')

    def test_reverse_major(self):
        self.assertFalse(self.check(major=P('All', 'B', 'A'))[0])

    def test_reverse_minor(self):
        self.assertFalse(self.check(minor=P('All', 'C', 'B'))[0])

    def test_reverse_conclusion(self):
        self.assertFalse(self.check(conclusion=P('All', 'C', 'A'))[0])

    def test_wrong_conclusion_predicate(self):
        self.assertFalse(self.check(conclusion=P('All', 'D', 'C'))[0])

    def test_wrong_conclusion_subject(self):
        self.assertFalse(self.check(conclusion=P('All', 'A', 'D'))[0])

    def test_member_to_universal_rejected(self):
        self.assertFalse(self.check(minor=P('Member', 'B', 'c'), conclusion=P('All', 'A', 'c'))[0])

    def test_universal_to_member_rejected(self):
        self.assertFalse(self.check(conclusion=P('Member', 'A', 'C'))[0])

    def test_different_time(self):
        self.assertEqual(self.check(major=P('All', 'A', 'B', Context('tomorrow')))[1], 'context-mismatch')

    def test_different_aspect(self):
        self.assertEqual(self.check(major=P('All', 'A', 'B', Context(aspect='as-musician')))[1], 'context-mismatch')

    def test_conclusion_context_changed(self):
        self.assertFalse(self.check(conclusion=P('All', 'A', 'C', Context('tomorrow')))[0])

    def test_untyped(self):
        self.assertEqual(check_chain('A B', self.minor, self.conclusion)[1], 'untyped-input')

    def test_missing_input(self):
        self.assertFalse(check_chain(None, self.minor, self.conclusion)[0])

    def test_unknown_kind(self):
        with self.assertRaises(ValueError): P('Usually', 'A', 'B')

    def test_blank_predicate(self):
        with self.assertRaises(ValueError): P('All', '', 'B')

    def test_blank_subject(self):
        with self.assertRaises(ValueError): P('All', 'A', ' ')

    def test_nonstring_name(self):
        with self.assertRaises(ValueError): P('All', 1, 'B')

    def test_untyped_context(self):
        with self.assertRaises(ValueError): P('All', 'A', 'B', 'today')

    def test_blank_context_time(self):
        with self.assertRaises(ValueError): Context('')

    def test_blank_context_aspect(self):
        with self.assertRaises(ValueError): Context(aspect='')

    def test_unknown_extension(self):
        with self.assertRaises(KeyError): evaluate(self.major, {'A': set()}, {})

    def test_unknown_individual(self):
        with self.assertRaises(KeyError): evaluate(P('Member', 'A', 'c'), {'A': {0}}, {})

    def test_explicit_weak_countermodel(self):
        extensions = {'A': {0}, 'B': {0, 1}, 'C': {1}}
        self.assertTrue(evaluate(P('Some', 'A', 'B'), extensions, {}))
        self.assertTrue(evaluate(self.minor, extensions, {}))
        self.assertFalse(evaluate(self.conclusion, extensions, {}))
        self.assertFalse(evaluate(self.major, extensions, {}))

    def test_empty_universal_not_existential(self):
        e = {'A': set(), 'B': set()}
        self.assertTrue(evaluate(self.major, e, {}))
        self.assertFalse(evaluate(P('Some', 'A', 'B'), e, {}))

    def test_sound_shape_not_true_premises(self):
        self.assertTrue(self.check()[0])
        self.assertFalse(evaluate(self.major, {'A': set(), 'B': {0}}, {}))

    def test_identity_not_aspect_equivalence(self):
        whole, role = ('person', 'whole'), ('person', 'musician-role')
        self.assertNotEqual(whole, role)
        survives = {whole}
        self.assertIn(whole, survives)
        self.assertNotIn(role, survives)
        alias = whole
        self.assertEqual(whole in survives, alias in survives)

    def test_powerset_size(self):
        self.assertEqual(len(powerset(3)), 8)

    def test_bounded_results(self):
        r = experiments()
        self.assertEqual(r['all_chain']['assignments'], 585)
        self.assertEqual(r['all_chain']['failures'], 0)
        self.assertEqual(r['member_chain']['failures'], 0)
        self.assertEqual(r['same_object_substitution']['failures'], 0)
        self.assertGreater(r['some_major_all_minor']['countermodels'], 0)

    def test_bad_bound_negative(self):
        with self.assertRaises(ValueError): experiments(-1)

    def test_bad_bound_large(self):
        with self.assertRaises(ValueError): experiments(6)

    def test_bad_bound_boolean(self):
        with self.assertRaises(ValueError): experiments(True)

    def test_bad_bound_string(self):
        with self.assertRaises(ValueError): experiments('3')


if __name__ == '__main__':
    unittest.main(verbosity=2)
