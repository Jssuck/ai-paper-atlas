"""Unit tests are separate from exhaustive.py's bounded oracle enumeration."""
from dataclasses import FrozenInstanceError
import unittest
from model import Belief, Evidence, InconsistentEvidence, Judgment, Model, Observation, judge


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.model = Model(("A", "B", "C"), (
            Observation("coarse", ("same", "same", "other")),
            Observation("fine", ("a", "b", "c")),
        ))
        self.initial = Belief(self.model)

    def test_empty_history_is_full_domain(self):
        self.assertEqual(self.initial.candidates, self.model.worlds)
        self.assertIsNone(self.initial.recognizes())

    def test_feedback_retains_truth_and_history(self):
        first = self.initial.consult("coarse", "B")
        second = first.consult("fine", "B")
        self.assertEqual(first.candidates, ("A", "B"))
        self.assertEqual(second.candidates, ("B",))
        self.assertEqual(second.recognizes(), "B")
        self.assertEqual(second.history, (Evidence("coarse", "same"), Evidence("fine", "b")))
        self.assertEqual(self.initial.history, ())

    def test_distinguishing_and_repeated_query(self):
        first = self.initial.consult("coarse", "B")
        self.assertFalse(first.distinguishes("coarse"))
        self.assertTrue(first.distinguishes("fine"))
        repeated = first.consult("coarse", "B")
        self.assertEqual(first.candidates, repeated.candidates)
        self.assertEqual(len(repeated.history), 2)

    def test_refusal_preserves_identity(self):
        self.assertIs(self.initial.consult("fine", "B", accept=False), self.initial)

    def test_indistinguishable_worlds_survive(self):
        model = Model(("A", "B"), (Observation("same", ("x", "x")),))
        state = Belief(model)
        for _ in range(10):
            state = state.consult("same", "A")
        self.assertEqual(state.candidates, ("A", "B"))
        self.assertEqual(model.fiber("A"), ("A", "B"))
        self.assertIsNone(state.recognizes())

    def test_zero_queries_and_singleton_domain(self):
        one = Model(("A",), ())
        two = Model(("A", "B"), ())
        self.assertEqual(Belief(one).recognizes(), "A")
        self.assertIsNone(Belief(two).recognizes())
        self.assertEqual(two.signature("A"), ())
        self.assertEqual(two.fiber("A"), ("A", "B"))

    def test_satisfaction_all_four_combinations(self):
        results = {
            (judge(self.model, guess, "A", satisfied=s).correct, s)
            for guess in ("A", "B") for s in (False, True)
        }
        self.assertEqual(results, {(False, False), (False, True), (True, False), (True, True)})
        self.assertEqual(self.initial.history, ())

    def test_false_consistent_input_can_mislead(self):
        # Consistency is NOT a truth detector. If truth is B, this is false input.
        misled = self.initial.observe("fine", "a")
        self.assertEqual(misled.recognizes(), "A")
        self.assertNotIn("B", misled.candidates)
        with self.assertRaises(InconsistentEvidence):
            misled.consult("fine", "B")

    def test_contradiction_is_rejected_without_mutation(self):
        first = self.initial.observe("fine", "a")
        with self.assertRaises(InconsistentEvidence):
            first.observe("fine", "b")
        self.assertEqual(first.candidates, ("A",))
        self.assertEqual(first.history, (Evidence("fine", "a"),))

    def test_types_and_domains_are_rejected(self):
        cases = [
            (TypeError, lambda: Model(["A"], ())),
            (ValueError, lambda: Model((), ())),
            (ValueError, lambda: Model(("A", "A"), ())),
            (TypeError, lambda: Model((1,), ())),
            (ValueError, lambda: Model((" ",), ())),
            (TypeError, lambda: Model(("A",), [])),
            (TypeError, lambda: Model(("A",), ("q",))),
            (ValueError, lambda: Model(("A",), (Observation("q", ("x", "y")),))),
            (ValueError, lambda: Model(("A",), (Observation("q", ("x",)), Observation("q", ("y",))))),
            (TypeError, lambda: Observation(1, ("x",))),
            (ValueError, lambda: Observation("", ("x",))),
            (TypeError, lambda: Observation("q", ["x"])),
            (ValueError, lambda: Observation("q", ())),
            (TypeError, lambda: Observation("q", (False,))),
            (ValueError, lambda: Observation("q", (" ",))),
            (TypeError, lambda: Evidence(None, "x")),
            (ValueError, lambda: Evidence("q", "")),
            (TypeError, lambda: Belief(None)),
            (TypeError, lambda: Belief(self.model, [])),
            (TypeError, lambda: Belief(self.model, (("fine", "a"),))),
            (ValueError, lambda: Belief(self.model, (Evidence("missing", "a"),))),
            (ValueError, lambda: self.initial.observe("fine", "outside")),
            (TypeError, lambda: self.initial.observe("fine", 1)),
            (ValueError, lambda: self.model.observation("missing")),
            (ValueError, lambda: self.model.world_index("missing")),
            (TypeError, lambda: self.model.signature(None)),
            (ValueError, lambda: self.model.fiber("missing")),
            (ValueError, lambda: self.initial.distinguishes("missing")),
            (ValueError, lambda: self.initial.consult("missing", "A", accept=False)),
            (ValueError, lambda: self.initial.consult("fine", "missing", accept=False)),
            (TypeError, lambda: self.initial.consult("fine", "A", accept=1)),
            (TypeError, lambda: judge(None, "A", "A", satisfied=True)),
            (ValueError, lambda: judge(self.model, "missing", "A", satisfied=True)),
            (ValueError, lambda: judge(self.model, "A", "missing", satisfied=True)),
            (TypeError, lambda: judge(self.model, "A", "A", satisfied=1)),
            (TypeError, lambda: Judgment(1, True)),
            (TypeError, lambda: Judgment(True, "yes")),
        ]
        self.assertEqual(len(cases), 37)
        for number, (exception, function) in enumerate(cases, start=1):
            with self.subTest(invalid_case=number):
                with self.assertRaises(exception):
                    function()

    def test_dataclasses_are_frozen(self):
        for obj, field, value in (
            (self.model, "worlds", ("X",)),
            (self.model.observations[0], "name", "different"),
            (self.initial, "history", ()),
            (Evidence("q", "a"), "outcome", "b"),
            (Judgment(True, False), "satisfied", True),
        ):
            with self.subTest(type=type(obj).__name__):
                with self.assertRaises(FrozenInstanceError):
                    setattr(obj, field, value)


if __name__ == "__main__":
    unittest.main(verbosity=2)
