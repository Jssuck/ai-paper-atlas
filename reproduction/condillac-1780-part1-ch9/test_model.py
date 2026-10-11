"""Tests retain all checks under python -O and -OO: no bare assert statements."""
import itertools
import unittest
from collections import Counter
from model import (BodyEvent, EmbodiedMemory, IdeaEvent, Observation, SequenceMemory,
                   Signal, WeightedHabits)
from demo import scenarios


class HabitTests(unittest.TestCase):
    def test_missing(self):
        self.assertEqual(WeightedHabits().choose("absent").status, "missing")

    def test_reinforcement_changes_strength(self):
        h = WeightedHabits()
        h.reinforce("a", "b", 2)
        h.reinforce("a", "b", 3)
        self.assertEqual(h.choose("a").strength, 5)

    def test_tie_is_not_arbitrary_winner(self):
        h = WeightedHabits()
        h.reinforce("a", "b")
        h.reinforce("a", "c")
        self.assertEqual(h.choose("a").status, "ambiguous")
        self.assertEqual(set(h.choose("a").contenders), {"b", "c"})

    def test_unique_strongest_not_first_inserted(self):
        h = WeightedHabits()
        h.reinforce("a", "b")
        h.reinforce("a", "c", 2)
        self.assertEqual(h.choose("a").value, "c")

    def test_end_is_distinct_from_missing(self):
        h = WeightedHabits()
        h.reinforce("a", None)
        self.assertEqual(h.choose("a").status, "chosen")
        self.assertIsNone(h.choose("a").value)
        self.assertEqual(h.choose("b").status, "missing")

    def test_snapshot_is_copy(self):
        h = WeightedHabits()
        h.reinforce("a", "b")
        copy = h.snapshot()
        copy.clear()
        self.assertEqual(h.edge_count, 1)

    def test_additive_forgetting_and_pruning(self):
        h = WeightedHabits()
        h.reinforce("a", "b", 3)
        h.reinforce("a", "c")
        h.forget(1)
        self.assertEqual(h.snapshot(), {("a", "b"): 2})
        h.forget(2)
        self.assertEqual(h.edge_count, 0)
        self.assertEqual(h._born, {})

    def test_zero_forgetting_is_identity(self):
        h = WeightedHabits()
        h.reinforce("a", "b")
        before = h.snapshot()
        h.forget(0)
        self.assertEqual(before, h.snapshot())

    def test_capacity_weakest_then_oldest(self):
        h = WeightedHabits(2)
        h.reinforce("a", "b", 2)
        h.reinforce("a", "c")
        h.reinforce("a", "d")
        self.assertEqual(h.snapshot(), {("a", "b"): 2, ("a", "d"): 1})
        self.assertEqual(h.edge_count, 2)

    def test_new_weak_edge_can_evict_itself(self):
        h = WeightedHabits(1)
        h.reinforce("a", "b", 2)
        h.reinforce("a", "c")
        self.assertEqual(h.snapshot(), {("a", "b"): 2})

    def test_reintroduced_edge_has_new_birth(self):
        h = WeightedHabits(1)
        h.reinforce("a", "b")
        h.forget(1)
        h.reinforce("a", "b")
        self.assertEqual(h._born[("a", "b")], 1)

    def test_invalid_arguments_are_explicit_exceptions(self):
        for value in (0, -1, 1.5, True):
            with self.subTest(capacity=value), self.assertRaises(ValueError):
                WeightedHabits(value)
        h = WeightedHabits()
        for value in (0, -1, 1.5, True):
            with self.subTest(amount=value), self.assertRaises(ValueError):
                h.reinforce("a", "b", value)
        for value in (-1, 1.5, True):
            with self.subTest(decay=value), self.assertRaises(ValueError):
                h.forget(value)
        with self.assertRaises(TypeError):
            h.reinforce([], "b")
        self.assertEqual(h.edge_count, 0)


class SequenceTests(unittest.TestCase):
    def test_exact_recovery_and_end_decision(self):
        m = SequenceMemory()
        m.practice(["do", "mi", "sol"])
        result = m.replay("do", max_transitions=3)
        self.assertEqual(result.tokens, ("do", "mi", "sol"))
        self.assertEqual(result.stop, "end")
        self.assertEqual(len(result.decisions), 3)

    def test_single_token_episode(self):
        m = SequenceMemory()
        m.practice(["A"])
        self.assertEqual(m.replay("A").tokens, ("A",))
        self.assertEqual(m.replay("A").stop, "end")

    def test_missing_cue_returns_only_cue(self):
        result = SequenceMemory().replay("unknown")
        self.assertEqual(result.tokens, ("unknown",))
        self.assertEqual(result.stop, "missing")

    def test_shared_cue_collision(self):
        m = SequenceMemory()
        m.practice(["A", "B"])
        m.practice(["A", "C"])
        self.assertEqual(m.replay("A").stop, "ambiguous")
        self.assertEqual(m.replay("A").tokens, ("A",))

    def test_practice_selects_frequency_not_intention(self):
        m = SequenceMemory()
        m.practice(["A", "B"])
        m.practice(["A", "C"], repetitions=2)
        self.assertEqual(m.replay("A").tokens, ("A", "C"))
        self.assertEqual(m.replay("A").stop, "end")

    def test_context_repairs_cross_episode_collision(self):
        m = SequenceMemory()
        m.practice(["A", "B"], "left")
        m.practice(["A", "C"], "right")
        self.assertEqual(m.replay("A", "left").tokens, ("A", "B"))
        self.assertEqual(m.replay("A", "right").tokens, ("A", "C"))
        self.assertEqual(m.replay("A", "absent").stop, "missing")

    def test_context_does_not_repair_internal_repetition(self):
        m = SequenceMemory()
        m.practice(["A", "B", "A", "C"], "one")
        self.assertEqual(m.replay("A", "one").stop, "ambiguous")

    def test_terminal_competes_with_continuation(self):
        m = SequenceMemory()
        m.practice(["A"])
        m.practice(["A", "B"])
        self.assertEqual(m.replay("A").stop, "ambiguous")

    def test_cycle_stops_by_budget(self):
        m = SequenceMemory()
        m.habits.reinforce(("", "A"), "A")
        result = m.replay("A", max_transitions=3)
        self.assertEqual(result.tokens, ("A", "A", "A", "A"))
        self.assertEqual(result.stop, "budget")
        self.assertEqual(len(result.decisions), 3)

    def test_zero_budget_and_exact_boundary(self):
        m = SequenceMemory()
        m.practice(["A", "B"])
        self.assertEqual(m.replay("A", max_transitions=0).stop, "budget")
        self.assertEqual(m.replay("A", max_transitions=0).decisions, ())
        self.assertEqual(m.replay("A", max_transitions=1).stop, "budget")
        self.assertEqual(m.replay("A", max_transitions=2).stop, "end")

    def test_replay_is_read_only(self):
        m = SequenceMemory()
        m.practice(["A", "B"])
        before = m.habits.snapshot()
        m.replay("A")
        self.assertEqual(m.habits.snapshot(), before)

    def test_loss_of_entire_first_edge(self):
        m = SequenceMemory(2)
        m.practice(["A", "B", "C"])
        self.assertEqual(m.habits.edge_count, 2)
        self.assertEqual(m.replay("A").stop, "missing")

    def test_noninjective_history_even_with_eviction_metadata(self):
        left, right = SequenceMemory(), SequenceMemory()
        left.practice(["A", "B", "A", "C", "A", "B", "A", "C", "A"])
        right.practice(["A", "B", "A", "C", "A", "C", "A", "B", "A"])
        self.assertEqual(left.habits.snapshot(), right.habits.snapshot())
        self.assertEqual(left.habits._born, right.habits._born)
        self.assertEqual(left.habits._serial, right.habits._serial)
        self.assertEqual(left.replay("A"), right.replay("A"))

    def test_invalid_episode_does_not_partially_train(self):
        m = SequenceMemory()
        for tokens in ([], "AB", ["A", ""], ["A", None]):
            with self.subTest(tokens=tokens), self.assertRaises(ValueError):
                m.practice(tokens)
        self.assertEqual(m.habits.edge_count, 0)
        with self.assertRaises(ValueError):
            m.practice(["A"], repetitions=True)
        with self.assertRaises(ValueError):
            m.replay("A", max_transitions=-1)
        with self.assertRaises(ValueError):
            m.replay("")
        with self.assertRaises(ValueError):
            m.practice(["A"], context=None)

    def test_exhaustive_single_episode_recovery_363_cases(self):
        checked = successes = 0
        for length in range(1, 6):
            for sequence in itertools.product("ABC", repeat=length):
                m = SequenceMemory()
                m.practice(sequence)
                result = m.replay(sequence[0], max_transitions=length)
                expected = len(set(sequence)) == len(sequence)
                actual = result.tokens == sequence and result.stop == "end"
                with self.subTest(sequence=sequence):
                    self.assertEqual(actual, expected)
                checked += 1
                successes += actual
        self.assertEqual((checked, successes), (363, 15))

    def test_exhaustive_two_episode_reference_392_queries(self):
        episodes = [p for n in range(1, 4) for p in itertools.product("AB", repeat=n)]
        checked = 0
        for left, right in itertools.product(episodes, repeat=2):
            m = SequenceMemory()
            m.practice(left)
            m.practice(right)
            counts = Counter()
            for sequence in (left, right):
                counts.update(zip(sequence, sequence[1:] + (None,)))
            for sequence in (left, right):
                correct = True
                for x, y in zip(sequence, sequence[1:] + (None,)):
                    competitors = [v for (a, b), v in counts.items() if a == x and b != y]
                    correct = correct and counts[x, y] > max(competitors, default=0)
                result = m.replay(sequence[0], max_transitions=len(sequence))
                with self.subTest(left=left, right=right, target=sequence):
                    self.assertEqual(result.tokens == sequence and result.stop == "end", correct)
                checked += 1
        self.assertEqual(checked, 392)


class EmbodimentTests(unittest.TestCase):
    def make_agent(self):
        agent = EmbodiedMemory()
        agent.teach([Observation(x, Signal("hand", x)) for x in "ABC"], repetitions=2)
        return agent

    def test_clear_only_removes_active_event(self):
        agent = self.make_agent()
        agent.sense(Signal("hand", "A"))
        before = [t.snapshot() for t in (agent.brain.habits, agent.incoming, agent.outgoing)]
        agent.clear_active()
        self.assertIsNone(agent.active)
        self.assertEqual(before, [t.snapshot() for t in (agent.brain.habits, agent.incoming, agent.outgoing)])

    def test_source_attribution_survives_replay(self):
        agent = self.make_agent()
        agent.sense(Signal("hand", "A"))
        result = agent.recall()
        self.assertEqual([e.source for e in result.events], ["external", "replay", "replay"])
        self.assertEqual([e.supports_external_object for e in result.events], [True, False, False])
        self.assertEqual([e.idea for e in result.events], ["A", "B", "C"])
        self.assertEqual(agent.active, IdeaEvent("C", "replay"))

    def test_feedback_not_independent_external_evidence(self):
        agent = self.make_agent()
        agent.set_cue("B")
        body = agent.express()
        self.assertIsInstance(body, BodyEvent)
        activated = agent.feedback(body)
        self.assertEqual(activated.event.idea, "B")
        self.assertEqual(activated.event.source, "feedback")
        self.assertFalse(activated.event.supports_external_object)
        external = agent.sense(body.signal)
        self.assertEqual(external.event.idea, activated.event.idea)
        self.assertTrue(external.event.supports_external_object)

    def test_incoming_and_outgoing_paths_are_separate(self):
        agent = self.make_agent()
        agent.afferent_enabled = False
        self.assertEqual(agent.sense(Signal("hand", "A")).status, "blocked")
        self.assertIsNone(agent.active)
        agent.set_cue("A")
        result = agent.recall()
        self.assertEqual(result.replay.tokens, ("A", "B", "C"))
        self.assertTrue(all(x is not None for x in result.outputs))
        agent.efferent_enabled = False
        agent.set_cue("A")
        result = agent.recall()
        self.assertTrue(all(x is None for x in result.outputs))
        self.assertEqual(result.replay.tokens, ("A", "B", "C"))

    def test_feedback_obeys_incoming_gate(self):
        agent = self.make_agent()
        agent.set_cue("A")
        body = agent.express()
        agent.afferent_enabled = False
        self.assertEqual(agent.feedback(body).status, "blocked")

    def test_missing_or_ambiguous_sensation_clears_stale_active(self):
        agent = self.make_agent()
        agent.set_cue("A")
        self.assertEqual(agent.sense(Signal("hand", "missing")).status, "missing")
        self.assertIsNone(agent.active)
        signal = Signal("hand", "A")
        agent.incoming.reinforce(("", signal), "D", 2)
        self.assertEqual(agent.sense(signal).status, "ambiguous")
        self.assertIsNone(agent.active)

    def test_ambiguous_expression_is_not_emitted(self):
        agent = self.make_agent()
        agent.outgoing.reinforce(("", "A"), Signal("foot", "A"), 2)
        agent.set_cue("A")
        self.assertIsNone(agent.express())

    def test_unactivated_recall_is_error(self):
        with self.assertRaises(ValueError):
            self.make_agent().recall()

    def test_forgetting_reaches_three_tables(self):
        agent = self.make_agent()
        agent.forget(2)
        self.assertEqual([t.edge_count for t in (agent.brain.habits, agent.incoming, agent.outgoing)], [0, 0, 0])

    def test_teaching_and_recall_do_not_implicitly_reinforce(self):
        agent = self.make_agent()
        self.assertIsNone(agent.active)
        before = [t.snapshot() for t in (agent.brain.habits, agent.incoming, agent.outgoing)]
        agent.sense(Signal("hand", "A"))
        agent.recall()
        agent.feedback(agent.express())
        self.assertEqual(before, [t.snapshot() for t in (agent.brain.habits, agent.incoming, agent.outgoing)])

    def test_validation_is_atomic(self):
        agent = EmbodiedMemory()
        with self.assertRaises(ValueError):
            agent.teach([Observation("A", Signal("hand", "A")), "bad"])
        self.assertEqual(agent.brain.habits.edge_count, 0)
        with self.assertRaises(ValueError):
            Signal("", "A")
        with self.assertRaises(ValueError):
            Observation("A", "bad")
        with self.assertRaises(ValueError):
            agent.feedback("bad")

    def test_demo_scenarios_have_expected_outcomes(self):
        data = scenarios()
        self.assertEqual(data["exact_recovery"]["stop"], "end")
        self.assertEqual(data["shared_cue_tie"]["stop"], "ambiguous")
        self.assertEqual(data["after_three_decay_units"]["edges"], 0)
        self.assertTrue(data["different_histories_same_weights"]["equal_birth_metadata"])
        self.assertEqual(data["central_replay_without_body_output"]["nonempty_outputs"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
