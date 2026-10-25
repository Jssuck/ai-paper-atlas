import unittest
from model import InquiryKey, Ledger, Status, exhaustive_check


class TestInquiry(unittest.TestCase):
    def setUp(self):
        self.l = Ledger()
        self.a = InquiryKey('attribute', 'sun', 't1', 'eclipsed')
        self.e = InquiryKey('existence', 'centaur', 'actual')

    def test_initial_questions(self):
        self.assertEqual(self.l.next_question(self.a), 'fact')
        self.assertEqual(self.l.next_question(self.e), 'exists')

    def test_yes_routes(self):
        for k, q in ((self.a, 'why'), (self.e, 'what')):
            self.l.record(k, Status.YES, 'supplied evidence')
            self.assertEqual(self.l.next_question(k), q)

    def test_no_does_not_route_to_positive_why(self):
        for k in (self.a, self.e):
            self.l.record(k, Status.NO, 'negative evidence')
            self.assertEqual(self.l.next_question(k), 'closed_negative')

    def test_withdraw_reopens(self):
        self.l.record(self.a, Status.YES, 'label')
        self.l.withdraw(self.a)
        self.assertEqual(self.l.next_question(self.a), 'fact')
        self.assertEqual(self.l.state(self.a).evidence, '')

    def test_revision(self):
        self.l.record(self.a, Status.YES, 'old')
        self.l.record(self.a, Status.NO, 'new')
        self.assertEqual(self.l.state(self.a).evidence, 'new')
        self.assertEqual(self.l.next_question(self.a), 'closed_negative')

    def test_time_isolation(self):
        self.l.record(self.a, Status.YES, 'label')
        self.assertEqual(self.l.next_question(InquiryKey('attribute', 'sun', 't2', 'eclipsed')), 'fact')

    def test_subject_isolation(self):
        self.l.record(self.a, Status.YES, 'label')
        self.assertEqual(self.l.next_question(InquiryKey('attribute', 'moon', 't1', 'eclipsed')), 'fact')

    def test_attribute_isolation(self):
        self.l.record(self.a, Status.YES, 'label')
        self.assertEqual(self.l.next_question(InquiryKey('attribute', 'sun', 't1', 'white')), 'fact')

    def test_type_isolation(self):
        self.l.record(self.a, Status.YES, 'label')
        self.assertEqual(self.l.next_question(InquiryKey('existence', 'sun', 't1')), 'exists')

    def test_nominal_description_not_existence(self):
        self.l.propose(self.e, 'nominal description')
        self.assertEqual(self.l.state(self.e).status, Status.UNKNOWN)
        self.assertEqual(self.l.next_question(self.e), 'exists')

    def test_candidates_do_not_certify(self):
        self.l.record(self.a, Status.YES, 'label')
        for text in ('A', 'B'):
            self.l.propose(self.a, text)
        self.assertEqual(self.l.candidates(self.a), ('A', 'B'))
        self.assertIsNone(self.l.certified_answer(self.a))

    def test_no_evidence_rejected(self):
        with self.assertRaises(ValueError): self.l.record(self.a, Status.YES, ' ')
        with self.assertRaises(ValueError): self.l.record(self.a, Status.UNKNOWN, 'label')
        with self.assertRaises(ValueError): self.l.record(self.a, 'yes', 'label')

    def test_bad_key_rejected(self):
        for args in [('bad', 's', 't'), ('attribute', 's', 't'), ('existence', 's', 't', 'p'), ('existence', '', 't')]:
            with self.assertRaises(ValueError): InquiryKey(*args)
        with self.assertRaises(TypeError): self.l.record('not a key', Status.YES, 'label')

    def test_candidate_validation(self):
        with self.assertRaises(ValueError): self.l.propose(self.a, '')
        self.assertEqual(self.l.candidates(self.a), ())

    def test_exhaustive(self):
        self.assertEqual(exhaustive_check(), {'max_length': 4, 'sequences': 242, 'transitions': 852, 'violations': 0})


if __name__ == '__main__':
    unittest.main()
