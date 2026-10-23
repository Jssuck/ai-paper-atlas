import unittest
from model import Space, Formula, Assumption, ReductioCertificate, verify_reductio, entails, counterexample, common_rows, is_even_square_equivalent


class Tests(unittest.TestCase):
    def setUp(self):
        self.space = Space(('P', 'S'))
        self.p = self.space.atom('P')
        self.s = self.space.atom('S')

    def test_bridge(self):
        self.assertTrue(entails((self.s.implies(self.p), self.p.negated()), self.s.negated()))

    def test_missing_bridge(self):
        self.assertEqual(counterexample((self.p.negated(),), self.s.negated()), {'P': False, 'S': True})

    def test_wrong_direction(self):
        self.assertFalse(entails((self.p.implies(self.s), self.p.negated()), self.s.negated()))

    def test_reverse_positive(self):
        self.assertTrue(entails((self.p.implies(self.s), self.p), self.s))

    def test_reductio_discharge(self):
        cert = ReductioCertificate((Assumption('bridge', self.s.implies(self.p)), Assumption('not_P', self.p.negated())), Assumption('temporary_S', self.s), self.s.negated())
        self.assertTrue(verify_reductio(cert))
        self.assertTrue(entails((a.formula for a in cert.background), cert.conclusion))

    def test_no_inner_contradiction(self):
        cert = ReductioCertificate((), Assumption('temporary_S', self.s), self.s.negated())
        self.assertFalse(verify_reductio(cert))

    def test_conclusion_not_exact_negation(self):
        cert = ReductioCertificate((Assumption('not_S', self.s.negated()),), Assumption('temporary_S', self.s), self.p)
        self.assertFalse(verify_reductio(cert))

    def test_same_label_cannot_leak(self):
        with self.assertRaises(ValueError):
            ReductioCertificate((Assumption('h', self.s),), Assumption('h', self.s), self.s.negated())

    def test_duplicate_background_labels(self):
        with self.assertRaises(ValueError):
            ReductioCertificate((Assumption('x', self.s), Assumption('x', self.p)), Assumption('h', self.s), self.s.negated())

    def test_inconsistent_background_explicit(self):
        cert = ReductioCertificate((Assumption('p', self.p), Assumption('not_p', self.p.negated())), Assumption('h', self.s), self.s.negated())
        self.assertTrue(verify_reductio(cert))
        self.assertEqual(common_rows((a.formula for a in cert.background), self.space), frozenset())

    def test_empty_premises(self):
        self.assertFalse(entails((), self.p))
        self.assertTrue(entails((), self.p.implies(self.p)))

    def test_empty_atom_space(self):
        sp = Space(())
        self.assertEqual(sp.assignment(0), {})
        self.assertTrue(entails((), Formula(sp, {0})))
        self.assertEqual(counterexample((), Formula(sp, set())), {})

    def test_invalid_atoms(self):
        for atoms in [('P', 'P'), ('',), (3,), (' ',), tuple(str(i) for i in range(9))]:
            with self.assertRaises(ValueError):
                Space(atoms)
        with self.assertRaises(ValueError):
            self.space.atom('missing')

    def test_invalid_rows(self):
        for rows in [{True}, {-1}, {4}, {1.0}, [1, True], [1, 1.0]]:
            with self.assertRaises(ValueError):
                Formula(self.space, rows)
        with self.assertRaises(ValueError):
            self.space.assignment(True)

    def test_validate_after_empty(self):
        with self.assertRaises(TypeError):
            common_rows((Formula(self.space, set()), None), self.space)
        with self.assertRaises(ValueError):
            entails((Formula(self.space, set()), Space(('Q',)).atom('Q')), self.p)

    def test_generators_frozen(self):
        background = (a for a in (Assumption('not_s', self.s.negated()),))
        cert = ReductioCertificate(background, Assumption('h', self.s), self.s.negated())
        self.assertTrue(verify_reductio(cert))
        self.assertTrue(verify_reductio(cert))
        self.assertTrue(entails((f for f in (self.s.implies(self.p), self.p.negated())), self.s.negated()))

    def test_parity(self):
        for n in (-101, -2, -1, 0, 1, 2, 101):
            self.assertTrue(is_even_square_equivalent(n))
        for invalid in (True, 2.0, '2'):
            with self.assertRaises(TypeError):
                is_even_square_equivalent(invalid)

    def test_invalid_certificate(self):
        with self.assertRaises(TypeError):
            verify_reductio(None)
        with self.assertRaises(ValueError):
            Assumption(' ', self.p)
        with self.assertRaises(ValueError):
            ReductioCertificate((), Assumption('h', self.p), Space(('Q',)).atom('Q'))
        with self.assertRaises(TypeError):
            ReductioCertificate((None,), Assumption('h', self.p), self.p.negated())


if __name__ == '__main__':
    unittest.main()
