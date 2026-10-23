"""Independent bit-mask oracle; not copied from the author's set-intersection tests."""
import itertools
import json
import math
import unittest
from model import (Space, Formula, Assumption, ReductioCertificate,
                   verify_reductio, entails, counterexample, common_rows,
                   is_even_square_equivalent)


def rows_formula(space, mask):
    return Formula(space, (i for i in range(space.rows) if (mask >> i) & 1))


class IndependentChecks(unittest.TestCase):
    def test_all_truth_sets_against_bit_oracle(self):
        sp = Space(('P', 'S'))
        fs = [rows_formula(sp, i) for i in range(16)]
        count = 0
        for a, b, c in itertools.product(range(16), repeat=3):
            bad = (a & b) & (15 ^ c)
            self.assertEqual(entails((fs[a], fs[b]), fs[c]), bad == 0)
            witness = counterexample((fs[a], fs[b]), fs[c])
            if bad:
                first = (bad & -bad).bit_length() - 1
                self.assertEqual(witness, {'P': bool(first & 2), 'S': bool(first & 1)})
            else:
                self.assertIsNone(witness)
            count += 1
        self.assertEqual(count, 4096)

    def test_certificate_full_space(self):
        sp = Space(('P', 'S'))
        fs = [rows_formula(sp, i) for i in range(16)]
        accepted = 0
        for g, h, c in itertools.product(range(16), repeat=3):
            cert = ReductioCertificate((Assumption('g', fs[g]),), Assumption('h', fs[h]), fs[c])
            expected = ((g & h) == 0) and (c == (15 ^ h))
            self.assertEqual(verify_reductio(cert), expected)
            accepted += expected
        self.assertEqual(accepted, 81)

    def test_two_backgrounds_and_discharge(self):
        sp = Space(('X', 'Y'))
        fs = [rows_formula(sp, i) for i in range(16)]
        count = 0
        for a, b, h in itertools.product(range(16), repeat=3):
            cert = ReductioCertificate((Assumption('a', fs[a]), Assumption('b', fs[b])), Assumption('h', fs[h]), fs[15 ^ h])
            expected = (a & b & h) == 0
            self.assertEqual(verify_reductio(cert), expected)
            self.assertEqual(entails((fs[a], fs[b]), fs[15 ^ h]), expected)
            count += 1
        self.assertEqual(count, 4096)

    def test_bridges_from_plain_booleans(self):
        sp = Space(('P', 'S'))
        p, s = sp.atom('P'), sp.atom('S')
        self.assertEqual(p.negated().implies(s.negated()), s.implies(p))
        for pp, ss in itertools.product((False, True), repeat=2):
            row = 2 * int(pp) + int(ss)
            self.assertEqual(row in s.implies(p).true_rows, (not ss) or pp)
            self.assertEqual(row in p.implies(s).true_rows, (not pp) or ss)
        self.assertTrue(entails((p.negated().implies(s.negated()), p.negated()), s.negated()))
        for background in ((p.negated(),), (p.implies(s), p.negated())):
            self.assertEqual(counterexample(background, s.negated()), {'P': False, 'S': True})

    def test_scope_labels_not_provenance_authentication(self):
        sp = Space(('P',))
        p = sp.atom('P')
        with self.assertRaises(ValueError):
            ReductioCertificate((Assumption('H', p),), Assumption('H', p), p.negated())
        # Different labels for identical formula are permitted, as documented.
        cert = ReductioCertificate((Assumption('renamed', p), Assumption('not_p', p.negated())), Assumption('H', p), p.negated())
        self.assertTrue(verify_reductio(cert))
        self.assertEqual(common_rows((a.formula for a in cert.background), sp), frozenset())

    def test_empty_space_and_generators(self):
        sp = Space(())
        top, bottom = Formula(sp, (0,)), Formula(sp, ())
        self.assertEqual(sp.rows, 1)
        self.assertTrue(entails(iter(()), top))
        self.assertEqual(counterexample(iter(()), bottom), {})
        cert = ReductioCertificate((Assumption('b', bottom) for _ in range(1)), Assumption('h', top), bottom)
        self.assertTrue(verify_reductio(cert))
        self.assertTrue(verify_reductio(cert))

    def test_validation_not_skipped(self):
        sp = Space(('P',))
        p = sp.atom('P')
        for values in ([0, False], [1, True], [0, 0.0], [-1], [2]):
            with self.assertRaises(ValueError):
                Formula(sp, iter(values))
        with self.assertRaises(TypeError):
            common_rows(iter((Formula(sp, ()), object())), sp)
        with self.assertRaises(ValueError):
            common_rows(iter((Formula(sp, ()), Space(('Q',)).atom('Q'))), sp)
        with self.assertRaises(TypeError):
            verify_reductio(object())
        with self.assertRaises(ValueError):
            sp.assignment(False)

    def test_atom_spaces_and_permutation(self):
        sp = Space(('Y', 'X'))
        self.assertEqual(sp.assignment(1), {'Y': False, 'X': True})
        self.assertEqual(sp.assignment(2), {'Y': True, 'X': False})
        self.assertEqual(Space(tuple('ABCDEFGH')).rows, 256)
        with self.assertRaises(ValueError):
            Space(tuple('ABCDEFGHI'))
        with self.assertRaises(ValueError):
            Space(('X', 'X'))
        with self.assertRaises(ValueError):
            sp.atom('missing')

    def test_integer_parity_by_division(self):
        for n in range(-512, 513):
            q, remainder = divmod(n, 2)
            self.assertEqual(n, 2 * q + remainder)
            self.assertEqual((n * n) % 2, remainder)
            self.assertTrue(is_even_square_equivalent(n))
        for value in (True, 2.0, '2', None):
            with self.assertRaises(TypeError):
                is_even_square_equivalent(value)

    def test_fraction_count_independent(self):
        coprime = 0
        for p in range(1, 65):
            for q in range(1, 65):
                # Euclidean algorithm independently, rather than importing gcd for count.
                a, b = p, q
                while b:
                    a, b = b, a % b
                coprime += a == 1
                self.assertNotEqual(p * p, 2 * q * q)
        self.assertEqual(coprime, 2519)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(IndependentChecks)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    print(json.dumps({'independent_tests': result.testsRun,
                      'entailment_truth_set_triples': 4096,
                      'certificate_triples': 4096,
                      'two_background_discharge_triples': 4096,
                      'accepted_single_background_certificates': 81,
                      'integer_parity_checks': 1025,
                      'bounded_fraction_pairs': 4096,
                      'coprime_fraction_pairs': 2519,
                      'scope': 'Finite implementation audit; general claims require the displayed proofs.'}, sort_keys=True))
