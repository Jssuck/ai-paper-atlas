"""Separate API and proof-scope probes, without editing author files."""
from dataclasses import FrozenInstanceError
import inspect
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from model import Belief, Evidence, InconsistentEvidence, Judgment, Model, Observation, judge


class Robustness(unittest.TestCase):
    def setUp(self):
        self.model = Model(("A", "B", "C"), (
            Observation("q", ("0", "1", "1")),
            Observation("r", ("0", "0", "1")),
            Observation("constant", ("yes", "yes", "yes"))))
        self.initial = Belief(self.model)

    def test_deep_state_has_only_immutable_values(self):
        def visit(value):
            if type(value) in (str, bool):
                return
            if type(value) is tuple:
                for child in value:
                    visit(child)
                return
            self.assertIn(type(value), (Observation, Model, Evidence, Belief, Judgment))
            self.assertTrue(value.__dataclass_params__.frozen)
            for field in value.__dataclass_fields__:
                visit(getattr(value, field))
                with self.assertRaises(FrozenInstanceError):
                    setattr(value, field, getattr(value, field))
                with self.assertRaises(FrozenInstanceError):
                    delattr(value, field)
        visit(self.initial.observe("q", "1"))
        visit(judge(self.model, "A", "B", satisfied=True))
        self.assertIs(type(self.initial.candidates), tuple)
        self.assertIs(type(self.model.signature("A")), tuple)
        self.assertIs(type(self.model.fiber("A")), tuple)

    def test_mutable_and_subclass_inputs_rejected(self):
        class Text(str):
            pass
        class Items(tuple):
            pass
        cases = [
            lambda: Model({"A": 1}, ()),
            lambda: Model(("A",), {"q": ("0",)}),
            lambda: Observation("q", {"A": "0"}),
            lambda: Observation("q", (["0"],)),
            lambda: Model(Items(("A",)), ()),
            lambda: Observation(Text("q"), ("0",)),
            lambda: Observation("q", (Text("0"),)),
            lambda: Belief(self.model, {"q": "1"}),
            lambda: Belief(self.model, iter(())),
            lambda: Evidence("q", bytearray(b"0")),
        ]
        for index, function in enumerate(cases):
            with self.subTest(index=index), self.assertRaises(TypeError):
                function()

    def test_invalid_method_labels_and_flags(self):
        labels = (None, 0, True, b"q", [], {}, "", "\t\n", "missing")
        for value in labels:
            error = ValueError if type(value) is str else TypeError
            functions = (
                lambda: self.model.observation(value),
                lambda: self.model.world_index(value),
                lambda: self.model.signature(value),
                lambda: self.model.fiber(value),
                lambda: self.model.outcome(value, "A"),
                lambda: self.model.outcome("q", value),
                lambda: self.initial.distinguishes(value),
                lambda: self.initial.consult(value, "A", accept=False),
                lambda: self.initial.consult("q", value, accept=False),
                lambda: self.initial.observe(value, "0"),
                lambda: self.initial.observe("q", value),
            )
            for number, function in enumerate(functions):
                with self.subTest(label=repr(value), method=number), self.assertRaises(error):
                    function()
        for value in (0, 1, None, "True", (), []):
            with self.subTest(flag=repr(value)), self.assertRaises(TypeError):
                self.initial.consult("q", "A", accept=value)
            with self.subTest(satisfied=repr(value)), self.assertRaises(TypeError):
                judge(self.model, "A", "A", satisfied=value)

    def test_false_but_consistent_is_not_truth_verification(self):
        # True world A; false q=1 leaves B,C. Truthful r=0 misleadingly singles B.
        false_state = self.initial.observe("q", "1")
        still_wrong = false_state.consult("r", "A")
        self.assertEqual(still_wrong.recognizes(), "B")
        self.assertNotIn("A", still_wrong.candidates)
        with self.assertRaises(InconsistentEvidence):
            still_wrong.consult("q", "A")
        self.assertEqual(still_wrong.recognizes(), "B")

    def test_full_fiber_is_not_current_knowledge(self):
        self.assertEqual(self.model.fiber("A"), ("A",))
        self.assertIsNone(self.initial.recognizes())
        self.assertEqual(self.initial.consult("constant", "A").candidates,
                         self.model.worlds)

    def test_refusing_one_query_does_not_preclude_other_correction(self):
        # Counterexample to an unqualified prose statement in article section 8.5.
        model = Model(("A", "B"), (Observation("q", ("0", "1")),
                                   Observation("r", ("x", "y"))))
        state = Belief(model)
        self.assertIs(state.consult("q", "A", accept=False), state)
        self.assertEqual(state.consult("r", "A").recognizes(), "A")

    def test_duplicate_evidence_order_and_hash(self):
        first = self.initial.observe("q", "1").observe("r", "0")
        second = self.initial.observe("r", "0").observe("q", "1")
        repeated = first.observe("q", "1")
        self.assertEqual(first.candidates, second.candidates)
        self.assertEqual(first.candidates, repeated.candidates)
        self.assertNotEqual(first.history, second.history)
        self.assertEqual(len(repeated.history), 3)
        self.assertEqual(hash(first), hash(Belief(self.model, first.history)))

    def test_adaptive_progress_bound(self):
        # Select a query by current candidate sizes, using a truth-agnostic strategy.
        n = 9
        model = Model(tuple(f"W{i}" for i in range(n)), tuple(
            Observation(f"is {i}", tuple(str(j == i) for j in range(n)))
            for i in range(n - 1)))
        for truth in model.worlds:
            state = Belief(model)
            steps = 0
            while state.recognizes() is None:
                q = next(o.name for o in model.observations if state.distinguishes(o.name))
                old_size = len(state.candidates)
                state = state.consult(q, truth)
                self.assertLess(len(state.candidates), old_size)
                steps += 1
                self.assertLessEqual(steps, n - 1)
            self.assertEqual(state.recognizes(), truth)
        self.assertEqual(steps, n - 1)  # Last world realizes the tight bound.

    def test_unicode_and_exact_labels(self):
        model = Model(("甲", " 乙 "), (Observation("细看", ("一", "二")),))
        self.assertEqual(Belief(model).consult("细看", " 乙 ").recognizes(), " 乙 ")
        with self.assertRaises(ValueError):
            model.world_index("乙")

    def test_signatures_do_not_expose_truth_to_observe(self):
        self.assertEqual(tuple(inspect.signature(Belief.observe).parameters),
                         ("self", "query", "outcome"))
        self.assertEqual(tuple(inspect.signature(Belief.recognizes).parameters), ("self",))


if __name__ == "__main__":
    unittest.main(verbosity=2)
