import unittest
from model import (ScenarioModel, Person, Condition, HEALTH, DISEASE, from_cells,
                   survey, celarent_survey)

class ModelTests(unittest.TestCase):
    def test_separate_not_joint(self):
        m = from_cells(1, (1, 2)); p = m.persons[0]
        self.assertTrue(m.possible(HEALTH, p))
        self.assertTrue(m.possible(DISEASE, p))
        self.assertFalse(m.joint_possible(HEALTH, DISEASE, p))
        self.assertFalse(m.holds(DISEASE, p, 'w0'))
        self.assertTrue(m.possibly_none(HEALTH))
        self.assertFalse(m.necessarily_none(HEALTH))

    def test_quantifier_scope(self):
        m = from_cells(2, (1, 2, 2, 1))
        self.assertTrue(m.all_possibly(DISEASE))
        self.assertFalse(m.possibly_all(DISEASE))
        self.assertFalse(m.possibly_none(HEALTH))

    def test_no_necessity_to_be_healthy(self):
        m = from_cells(1, (2, 2))
        self.assertTrue(m.necessarily_none(HEALTH))
        self.assertFalse(m.possible(HEALTH, m.persons[0]))

    def test_empty_domain_vacuity(self):
        m = from_cells(0, ())
        self.assertTrue(m.all_possibly(DISEASE))
        self.assertTrue(m.possibly_all(DISEASE))
        self.assertTrue(m.necessarily_none(HEALTH))
        self.assertTrue(m.possibly_none(HEALTH))

    def test_type_rejection(self):
        m = from_cells(1, (1, 2))
        with self.assertRaises(TypeError): m.holds(HEALTH, DISEASE, 'w0')
        with self.assertRaises(TypeError): m.holds('health', m.persons[0], 'w0')
        with self.assertRaises(ValueError): m.holds(HEALTH, Person('unknown'), 'w0')
        with self.assertRaises(ValueError): m.holds(Condition('unknown'), m.persons[0], 'w0')
        with self.assertRaises(ValueError): m.holds(HEALTH, m.persons[0], 'unknown')

    def test_empty_domain_validates_all_conditions(self):
        m = from_cells(0, ())
        for fn in (m.all_possibly, m.possibly_all, m.possibly_none, m.necessarily_none):
            with self.assertRaises(TypeError): fn('health')
            with self.assertRaises(ValueError): fn(Condition('unknown'))
        with self.assertRaises(ValueError): m.possible(HEALTH, Person('absent'))

    def test_joint_short_circuit_validates_second_condition(self):
        m = from_cells(1, (0, 0)); p = m.persons[0]
        with self.assertRaises(TypeError): m.joint_possible(HEALTH, 'disease', p)
        with self.assertRaises(ValueError): m.joint_possible(HEALTH, Condition('unknown'), p)
        with self.assertRaises(TypeError): m.joint_possible(HEALTH, DISEASE, HEALTH)
        with self.assertRaises(ValueError): m.joint_possible(HEALTH, DISEASE, Person('absent'))

    def test_input_validation(self):
        for n, cells in ((-1, ()), (1, (1,)), (1, (1, 3)), (True, (1, 2))):
            with self.assertRaises(ValueError): from_cells(n, cells)
        p = Person('p')
        with self.assertRaises(ValueError): ScenarioModel((p,), (), {})
        with self.assertRaises(ValueError): ScenarioModel((p,), ('w',), {})
        with self.assertRaises(ValueError):
            ScenarioModel((p,), ('w',), {(HEALTH,'w'):{p},(DISEASE,'w'):{p}})
        with self.assertRaises(TypeError): ScenarioModel((HEALTH,), ('w',), {})

    def test_celarent_bounded_enumeration(self):
        for n in range(4):
            s = celarent_survey(n)
            self.assertEqual(s['triples'], 2**(3*n))
            self.assertEqual(s['failures'], 0)

    def test_modal_bounded_enumeration(self):
        for n in (0,1,2): self.assertEqual(survey(n)['models'], 3**(2*n))
        self.assertEqual(survey(0)['counterexamples_to_necessarily_no_health'], 0)
        self.assertGreater(survey(1)['counterexamples_to_necessarily_no_health'], 0)
        self.assertEqual(survey(1)['universal_possibility_scope_gaps'], 0)
        self.assertGreater(survey(2)['universal_possibility_scope_gaps'], 0)

if __name__ == '__main__': unittest.main(verbosity=2)
