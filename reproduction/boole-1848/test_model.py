"""Direct set operations are an oracle separate from the table evaluator."""
import unittest
from fractions import Fraction as F
from itertools import product
import boole_model as m


class ModelTests(unittest.TestCase):
    def test_bits_and_zero_arity(self):
        self.assertEqual(m.bits(0), ((),))
        self.assertEqual(m.expansion_at({(): F(3, 2)}, ()), F(3, 2))

    def test_constituent_partition(self):
        for n in range(5):
            for p in m.bits(n):
                values = [m.constituent(a, p) for a in m.bits(n)]
                self.assertEqual(sum(values), 1)
                self.assertEqual(values.count(1), 1)

    def test_expansion_for_rational_tables(self):
        values = (F(-1, 2), F(0), F(2, 3))
        for entries in product(values, repeat=4):
            table = dict(zip(m.bits(2), entries))
            for p, expected in table.items():
                self.assertEqual(m.expansion_at(table, p), expected)

    def test_negative_coefficients_do_not_cancel_between_atoms(self):
        table = m.truth_table(2, lambda x, y: x-y)
        self.assertFalse(m.equation_holds(table, {0, 1}, ({0}, {1})))
        # The sum over people is zero, but the equation is pointwise, not a count.
        self.assertEqual(sum(table[(int(i == 0), int(i == 1))] for i in (0, 1)), 0)

    def test_identity_set_oracle(self):
        table = m.truth_table(2, m.identity_example)
        for size in range(4):
            u = frozenset(range(size))
            for x, y in product(m.powerset(u), repeat=2):
                self.assertEqual(m.equation_holds(table, u, (x, y)), x == y)

    def test_four_endpoint_cases(self):
        self.assertEqual(m.endpoint_choices(0, 0), (0, 1))
        self.assertEqual(m.endpoint_choices(0, 2), (0,))
        self.assertEqual(m.endpoint_choices(-3, 0), (1,))
        self.assertEqual(m.endpoint_choices(2, 2), ())

    def test_all_rational_endpoint_pairs(self):
        values = (F(-1), F(-1, 2), F(0), F(1, 3), F(1), F(2))
        for f0, f1 in product(values, repeat=2):
            got = m.endpoint_choices(f0, f1)
            self.assertEqual(got, tuple(z for z in (0, 1) if (1-z)*f0+z*f1 == 0))
            if f0 != f1:
                ratio = f0/(f0-f1)
                self.assertEqual(got, (int(ratio),) if ratio in (0, 1) else ())

    def test_equal_nonzero_endpoints_are_forbidden(self):
        self.assertEqual(m.endpoint_choices(F(2, 3), F(2, 3)), ())
        self.assertEqual(m.endpoint_choices(1, -1), ())  # ratio 1/2 is not a bit

    def test_generic_solver_against_direct_rational_evaluation(self):
        u = {0, 1}
        sets = m.powerset(u)
        for entries in product((-1, 0, 1), repeat=4):
            table = dict(zip(m.bits(2), entries))
            for x in sets:
                expected = frozenset(y for y in sets
                    if all(table[(int(i in x), int(i in y))] == 0 for i in u))
                self.assertEqual(m.solve_last_class(table, u, (x,)), expected)

    def test_ship_set_oracle(self):
        table = m.truth_table(3, m.ship_example)
        for size in range(4):
            u = frozenset(range(size))
            sets = m.powerset(u)
            for x, y in product(sets, repeat=2):
                # Y∩Z and X\Z are disjoint, so union matches arithmetic sum here.
                expected = frozenset(z for z in sets if x & y == (y & z) | (x - z))
                self.assertEqual(m.solve_last_class(table, u, (x, y)), expected)
                generated = frozenset(m.ship_parametrization(u, x, y, w, wp)
                                      for w, wp in product(sets, repeat=2))
                self.assertEqual(generated, expected)

    def test_free_class_need_not_be_constant_on_atom(self):
        table = m.truth_table(3, m.ship_example)
        sols = m.solve_last_class(table, {0, 1}, ({0, 1}, {0, 1}))
        self.assertIn(frozenset({0}), sols)
        self.assertEqual(len(sols), 4)

    def test_inconsistent_fixed_atom_excludes_all_solutions(self):
        table = m.truth_table(2, lambda x, y: x+1)
        self.assertEqual(m.solve_last_class(table, {0}, ({0},)), frozenset())

    def test_empty_universe_has_one_output_set(self):
        table = m.truth_table(2, lambda x, y: 1)
        self.assertEqual(m.solve_last_class(table, (), ((),)), frozenset({frozenset()}))

    def test_contraposition_set_oracle(self):
        for size in range(4):
            u = frozenset(range(size))
            for x, y in product(m.powerset(u), repeat=2):
                self.assertEqual(y <= x, (u-x) <= (u-y))

    def test_fixed_v_complement_parametrization(self):
        for size in range(4):
            u = frozenset(range(size))
            sets = m.powerset(u)
            for v, y in product(sets, repeat=2):
                expected = frozenset(u-x for x in sets if y == v & x)
                if y <= v:
                    generated = frozenset(m.complement_parametrization(u,v,y,w) for w in sets)
                    self.assertEqual(generated, expected)
                else:
                    self.assertFalse(expected)
                    with self.assertRaises(ValueError):
                        m.complement_parametrization(u,v,y,())

    def test_universal_selector_is_existential_not_forall(self):
        u = {0, 1}; x = frozenset(u); y = frozenset({0})
        self.assertTrue(y <= x)
        self.assertTrue(any(y == v & x for v in m.powerset(u)))
        self.assertFalse(all(y == v & x for v in m.powerset(u)))

    def test_particular_requires_nonempty_shared_selection(self):
        u = frozenset({0, 1}); sets = m.powerset(u)
        for x, y in product(sets, repeat=2):
            witnesses = [v & y for v, vp in product(sets, repeat=2) if v & y == vp & x]
            self.assertTrue(witnesses)  # empty selectors always solve the bare equality
            self.assertEqual(any(bool(s) for s in witnesses), bool(x & y))

    def test_darapti_counterexample_and_existential_repair(self):
        u = frozenset({0,1}); x = frozenset({0}); y=frozenset(); z=frozenset({1})
        self.assertTrue(y <= x and y <= z)
        self.assertFalse(x & z)
        for x,y,z in product(m.powerset(u),repeat=3):
            if y and y<=x and y<=z:
                self.assertTrue(x & z)

    def test_original_elimination_needs_retained_bounds(self):
        for v,vp,x,z in m.bits(4):
            projected = any(x==v*y and z==vp*(1-y) for y in (0,1))
            equality = v*z == vp*(v-x)
            self.assertEqual(projected, equality and x<=v and z<=vp)
        v=vp=x=0; z=1
        self.assertEqual(v*z,vp*(v-x))
        self.assertFalse(any(x==v*y and z==vp*(1-y) for y in (0,1)))

    def test_original_elimination_projection_set_oracle(self):
        u=frozenset({0,1}); sets=m.powerset(u)
        for v,vp,x,z in product(sets,repeat=4):
            projected=any(x==v&y and z==vp&(u-y) for y in sets)
            equation=all(int(i in v)*int(i in z)==int(i in vp)*(int(i in v)-int(i in x)) for i in u)
            self.assertEqual(projected, equation and x<=v and z<=vp)

    def test_conditional_disjunction(self):
        for x,y in m.bits(2):
            self.assertEqual(y<=x, x*y+(1-y)*x+(1-y)*(1-x)==1)
            self.assertEqual(y<=x, y*(1-x)==0)

    def test_input_validation(self):
        for bad in (-1, 1.0, True):
            with self.assertRaises(ValueError): m.bits(bad)
        for bad in (0.5, True, complex(1)):
            with self.assertRaises(TypeError): m.endpoint_choices(bad, 0)
        for bad in ({}, {(0,):0}, {(0,):0,(1,):0.1}, {(2,):0,(0,):1}):
            with self.assertRaises((ValueError,TypeError)): m.table_arity(bad)
        with self.assertRaises(ValueError): m.powerset([1,1])
        with self.assertRaises(ValueError): m.equation_holds({():0},{0},({0},))
        with self.assertRaises(ValueError): m.equation_holds({(0,):0,(1,):0},{0},({1},))
        with self.assertRaises(ValueError): m.endpoint_table({():0})
        with self.assertRaises(ValueError): m.solve_last_class(m.truth_table(2,lambda x,y:0),{0},())
        with self.assertRaises(ValueError): m.expansion_at({(0,):0,(1,):1},(True,))

if __name__ == '__main__':
    unittest.main(verbosity=2)
