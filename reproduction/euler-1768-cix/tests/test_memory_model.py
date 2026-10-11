"""Executable requirements, edge cases, and finite-domain coverage."""
from dataclasses import FrozenInstanceError, fields
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from memory_model import Action, Cue, Kind, State, all_actions, all_states, demo, exhaustive_check, transition

F, B = Cue.FIRE, Cue.BELL


def run(*actions):
    state = State()
    output = None
    for action in actions:
        state, output = transition(state, action)
    return state, output


def a(kind, cue=None):
    return Action(kind, cue)


class DistinctionTests(unittest.TestCase):
    def test_first_perception_stores_and_supplies_conviction(self):
        state, out = run(a(Kind.PERCEIVE, F))
        self.assertEqual(state, State(frozenset({F}), frozenset({F}), F, F))
        self.assertIs(out.recognized, False)
        self.assertIs(out.current_existence_conviction, F)
        self.assertIsNone(out.recall_succeeded)

    def test_storage_can_outlast_attention_and_input(self):
        state, out = run(a(Kind.PERCEIVE, F), a(Kind.WITHDRAW), a(Kind.SET_ASIDE))
        self.assertIn(F, state.retained)
        self.assertIn(F, state.recallable)
        self.assertIsNone(state.attention)
        self.assertIsNone(state.sensory)
        for _ in range(1000):
            state, out = transition(state, a(Kind.SET_ASIDE))
        self.assertIn(F, state.retained)
        self.assertIsNone(out.current_existence_conviction)

    def test_withdrawing_input_need_not_remove_attended_idea(self):
        state, out = run(a(Kind.PERCEIVE, F), a(Kind.WITHDRAW))
        self.assertIs(state.attention, F)
        self.assertIsNone(out.sensory_input)
        self.assertIsNone(out.current_existence_conviction)

    def test_recalled_fire_does_not_produce_fire_conviction(self):
        state, out = run(a(Kind.PERCEIVE, F), a(Kind.WITHDRAW),
                         a(Kind.SET_ASIDE), a(Kind.RECALL, F))
        self.assertIs(out.recall_succeeded, True)
        self.assertIs(state.attention, F)
        self.assertIsNone(out.sensory_input)
        self.assertIsNone(out.current_existence_conviction)
        self.assertIsNone(out.recognized)

    def test_attention_and_sensory_input_can_have_different_contents(self):
        state, out = run(a(Kind.PERCEIVE, F), a(Kind.PERCEIVE, B), a(Kind.RECALL, F))
        self.assertIs(state.attention, F)
        self.assertIs(state.sensory, B)
        self.assertIs(out.current_existence_conviction, B)
        self.assertIsNot(out.current_existence_conviction, F)

    def test_recall_can_coexist_with_independent_current_input(self):
        before, _ = run(a(Kind.PERCEIVE, F))
        after, out = transition(before, a(Kind.RECALL, F))
        self.assertIs(out.recall_succeeded, True)
        self.assertIs(out.current_existence_conviction, F)
        self.assertIs(after.sensory, before.sensory)

    def test_set_aside_does_not_erase_current_input(self):
        state, out = run(a(Kind.PERCEIVE, F), a(Kind.SET_ASIDE))
        self.assertIsNone(state.attention)
        self.assertIs(state.sensory, F)
        self.assertIs(out.current_existence_conviction, F)

    def test_recognition_uses_retention_before_new_encoding(self):
        state, first = run(a(Kind.PERCEIVE, F))
        state, second = transition(state, a(Kind.PERCEIVE, F))
        self.assertIs(first.recognized, False)
        self.assertIs(second.recognized, True)

    def test_inaccessible_is_retained_and_can_be_recognized(self):
        state, _ = run(a(Kind.PERCEIVE, F), a(Kind.WITHDRAW), a(Kind.MAKE_INACCESSIBLE, F))
        self.assertIn(F, state.retained)
        self.assertNotIn(F, state.recallable)
        self.assertIsNone(state.attention)
        state, recall = transition(state, a(Kind.RECALL, F))
        self.assertIs(recall.recall_succeeded, False)
        state, perception = transition(state, a(Kind.PERCEIVE, F))
        self.assertIs(perception.recognized, True)
        self.assertIn(F, state.recallable)

    def test_never_seen_recall_fails_and_first_perception_is_not_recognition(self):
        state, out = run(a(Kind.RECALL, F))
        self.assertEqual(state, State())
        self.assertIs(out.recall_succeeded, False)
        _, out = transition(state, a(Kind.PERCEIVE, F))
        self.assertIs(out.recognized, False)

    def test_recall_failure_does_not_tell_inaccessible_from_absent(self):
        inaccessible, _ = run(a(Kind.PERCEIVE, F), a(Kind.WITHDRAW), a(Kind.MAKE_INACCESSIBLE, F))
        _, old_output = transition(inaccessible, a(Kind.RECALL, F))
        _, new_output = transition(State(), a(Kind.RECALL, F))
        self.assertEqual(old_output, new_output)
        self.assertNotEqual(inaccessible, State())

    def test_failed_recall_does_not_delete_unrelated_attention(self):
        state, out = run(a(Kind.PERCEIVE, B), a(Kind.RECALL, F))
        self.assertIs(out.recall_succeeded, False)
        self.assertIs(state.attention, B)
        self.assertIs(state.sensory, B)

    def test_complete_reset_has_no_surviving_history_flag(self):
        erased, _ = run(a(Kind.PERCEIVE, F), a(Kind.PERCEIVE, B), a(Kind.ERASE_ALL))
        self.assertEqual(erased, State())
        self.assertEqual({f.name for f in fields(State)}, {"retained", "recallable", "attention", "sensory"})
        for action in all_actions():
            if action.kind is Kind.MAKE_INACCESSIBLE:
                with self.assertRaises(ValueError):
                    transition(erased, action)
                with self.assertRaises(ValueError):
                    transition(State(), action)
            else:
                self.assertEqual(transition(erased, action), transition(State(), action))
        self.assertIs(transition(erased, a(Kind.PERCEIVE, F))[1].recognized, False)

    def test_equal_states_stay_equal_under_a_shared_future_sequence(self):
        left, _ = run(a(Kind.PERCEIVE, F), a(Kind.ERASE_ALL))
        right = State()
        future = [a(Kind.PERCEIVE, B), a(Kind.WITHDRAW), a(Kind.MAKE_INACCESSIBLE, B),
                  a(Kind.RECALL, B), a(Kind.PERCEIVE, B), a(Kind.PERCEIVE, F), a(Kind.ERASE_ALL)]
        for action in future:
            left, lout = transition(left, action)
            right, rout = transition(right, action)
            self.assertEqual((left, lout), (right, rout))

    def test_memory_is_token_specific(self):
        state, _ = run(a(Kind.PERCEIVE, F))
        _, out = transition(state, a(Kind.PERCEIVE, B))
        self.assertIs(out.recognized, False)

    def test_inputs_not_mutated_and_results_not_aliased_mutably(self):
        before = State()
        after, _ = transition(before, a(Kind.PERCEIVE, F))
        self.assertEqual(before, State())
        self.assertNotEqual(after, before)
        with self.assertRaises(FrozenInstanceError):
            after.attention = None


class ValidationTests(unittest.TestCase):
    def test_invalid_state_types_and_invariants(self):
        for kwargs in [dict(retained={F}), dict(retained=frozenset({"fire"})),
                       dict(recallable=frozenset({F})), dict(attention=F), dict(sensory=F),
                       dict(attention="fire"), dict(sensory=False),
                       dict(retained=frozenset({F}), sensory=F)]:
            with self.subTest(kwargs=kwargs), self.assertRaises((TypeError, ValueError)):
                State(**kwargs)

    def test_invalid_action_types_and_arguments(self):
        for kind, cue in [("recall", F), (Kind.RECALL, None), (Kind.PERCEIVE, "fire"),
                          (Kind.WITHDRAW, F), (Kind.ERASE_ALL, F), (False, None)]:
            with self.subTest(kind=kind, cue=cue), self.assertRaises((TypeError, ValueError)):
                Action(kind, cue)

    def test_rejects_invalid_transition_argument_types(self):
        for state, action in [(None, a(Kind.WITHDRAW)), (State(), {"kind": "withdraw"})]:
            with self.assertRaises(TypeError):
                transition(state, action)

    def test_cannot_block_never_retained_or_currently_presented_cue(self):
        with self.assertRaisesRegex(ValueError, "unretained"):
            transition(State(), a(Kind.MAKE_INACCESSIBLE, F))
        state, _ = run(a(Kind.PERCEIVE, F))
        with self.assertRaisesRegex(ValueError, "withdraw"):
            transition(state, a(Kind.MAKE_INACCESSIBLE, F))
        self.assertIs(state.sensory, F)

    def test_state_serialization_requires_exact_keys_and_types(self):
        base = State().to_dict()
        cases = [None, [], {}, {**base, "hidden_history": True},
                 {**base, "retained": "fire"}, {**base, "retained": ["fire", "fire"]},
                 {**base, "retained": [None]}, {**base, "retained": ["dragon"]},
                 {**base, "attention": 0}, {**base, "sensory": "fire"}]
        for case in cases:
            with self.subTest(case=case), self.assertRaises((TypeError, ValueError)):
                State.from_dict(case)

    def test_action_serialization_requires_exact_keys_and_types(self):
        cases = [None, {}, {"kind": "recall"}, {"kind": "recall", "cue": "fire", "extra": 0},
                 {"kind": "bad", "cue": None}, {"kind": 3, "cue": None},
                 {"kind": "recall", "cue": None}, {"kind": "recall", "cue": "bad"},
                 {"kind": "withdraw", "cue": "fire"}]
        for case in cases:
            with self.subTest(case=case), self.assertRaises((TypeError, ValueError)):
                Action.from_dict(case)

    def test_serialization_round_trips_entire_finite_domain(self):
        for state in all_states():
            self.assertEqual(State.from_dict(json.loads(json.dumps(state.to_dict()))), state)
        for action in all_actions():
            self.assertEqual(Action.from_dict(json.loads(json.dumps(action.to_dict()))), action)


class CompleteDomainAndCliTests(unittest.TestCase):
    def test_every_valid_state_and_action_checked(self):
        report = exhaustive_check()
        self.assertEqual(report["states"], 29)
        self.assertEqual(report["reachable_states"], 29)
        self.assertEqual(report["actions"], 9)
        self.assertEqual(report["state_action_pairs"], 261)
        self.assertEqual(report["successful_transitions"], 235)
        self.assertEqual(report["rejected_preconditions"], 26)
        self.assertEqual(report["successful_transitions"] + report["rejected_preconditions"], 261)
        self.assertEqual(report["status"], "PASS")

    def test_demo_is_deterministic_and_contains_true_witnesses(self):
        result = demo()
        self.assertEqual(result, demo())
        witness = result["equal_state_witness"]
        self.assertTrue(witness["same_complete_state"])
        self.assertTrue(witness["same_next_state_and_output"])
        self.assertIs(witness["recognition_after_either_history"], False)
        self.assertIs(result["cases"]["inaccessible_then_recognized"]["steps"][-1]["output"]["recognized"], True)

    def test_cli_outputs_json_to_stdout_and_file(self):
        module = Path(__file__).resolve().parents[1] / "memory_model.py"
        result = subprocess.run([sys.executable, str(module), "--check"], capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout)["status"], "PASS")
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "nested" / "demo.json"
            subprocess.run([sys.executable, str(module), "--demo", "--output", str(target)], check=True)
            self.assertEqual(json.loads(target.read_text(encoding="utf-8")), demo())

    def test_exhaustive_checker_runs_under_optimized_python(self):
        module = Path(__file__).resolve().parents[1] / "memory_model.py"
        result = subprocess.run([sys.executable, "-O", str(module), "--check"], capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout)["status"], "PASS")

    def test_cli_rejects_conflicting_modes(self):
        module = Path(__file__).resolve().parents[1] / "memory_model.py"
        result = subprocess.run([sys.executable, str(module), "--demo", "--check"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("not allowed", result.stderr)


if __name__ == "__main__":
    unittest.main()
