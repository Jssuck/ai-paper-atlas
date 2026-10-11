"""Independent black/white-box oracle checks; standard library only; -O safe.

The oracle uses record lists and sorted rankings rather than importing model
helpers. No author test or demo is imported. Run from the reproduction folder:
python -B independent-review/test_independent.py
"""
from collections import Counter
from dataclasses import FrozenInstanceError
from itertools import product
from pathlib import Path
import ast
import hashlib
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from model import BodyEvent, EmbodiedMemory, IdeaEvent, Observation, SequenceMemory, Signal, WeightedHabits

METRICS = Counter()


def state(table):
    return (table.capacity, table.snapshot(), dict(table._born), table._serial)


def machine_state(agent):
    return tuple(state(t) for t in (agent.brain.habits, agent.incoming, agent.outgoing))


class RecordOracle:
    """Slow reference retaining an explicit list [key, value, weight, born]."""
    def __init__(self, capacity):
        self.capacity, self.records, self.serial = capacity, [], 0

    def add(self, key, value, amount):
        for entry in self.records:
            if entry[:2] == [key, value]:
                entry[2] += amount
                break
        else:
            self.records.append([key, value, amount, self.serial])
            self.serial += 1
        if self.capacity is not None:
            ranked = sorted(self.records, key=lambda r: (-r[2], -r[3]))
            retained = {r[3] for r in ranked[:self.capacity]}
            self.records = [r for r in self.records if r[3] in retained]

    def decay(self, amount):
        self.records = [[k, v, w - amount, b] for k, v, w, b in self.records if w > amount]

    def state(self):
        return (self.capacity, {(k, v): w for k, v, w, b in self.records},
                {(k, v): b for k, v, w, b in self.records}, self.serial)


def oracle_choice(matrix, token):
    ranked = sorted([(v, w) for (k, v), w in matrix.items() if k == token and w > 0],
                    key=lambda item: -item[1])
    if not ranked:
        return ('missing', None, 0, frozenset())
    winners = frozenset(v for v, w in ranked if w == ranked[0][1])
    if len(winners) > 1:
        return ('ambiguous', None, ranked[0][1], winners)
    return ('chosen', ranked[0][0], ranked[0][1], winners)


def oracle_replay(matrix, cue, budget):
    result, choices = [cue], []
    while len(choices) < budget:
        decision = oracle_choice(matrix, result[-1])
        choices.append(decision)
        status, value, _, _ = decision
        if status != 'chosen':
            return tuple(result), status, tuple(choices)
        if value is None:
            return tuple(result), 'end', tuple(choices)
        result.append(value)
    return tuple(result), 'budget', tuple(choices)


def normalized(result):
    return (result.tokens, result.stop,
            tuple((c.status, c.value, c.strength, frozenset(c.contenders)) for c in result.decisions))


def exact_condition(matrix, target, budget):
    if budget < len(target):
        return False
    for x, desired in zip(target, target[1:] + (None,)):
        if matrix.get((x, desired), 0) == 0:
            return False
        for competitor in ('A', 'B', None):
            if competitor != desired and matrix.get((x, competitor), 0) >= matrix.get((x, desired), 0):
                return False
    return True


class IndependentContractTests(unittest.TestCase):
    def test_all_small_weight_graphs_and_exact_recovery_contract(self):
        edges = tuple(product('AB', ('A', 'B', None)))
        targets = [p for n in range(1, 5) for p in product('AB', repeat=n)]
        for weights in product(range(3), repeat=6):
            matrix = dict(zip(edges, weights))
            model = SequenceMemory()
            for (key, value), weight in matrix.items():
                if weight:
                    model.habits.reinforce(('', key), value, weight)
            before = state(model.habits)
            for cue in ('A', 'B', 'missing'):
                for budget in range(7):
                    observed = model.replay(cue, max_transitions=budget)
                    self.assertEqual(normalized(observed), oracle_replay(matrix, cue, budget))
                    if observed.stop == 'end':
                        self.assertEqual(len(observed.tokens), len(set(observed.tokens)))
                    METRICS['graph_replay_queries'] += 1
            for target in targets:
                for budget in sorted({0, len(target)-1, len(target), len(target)+1}):
                    observed = model.replay(target[0], max_transitions=budget)
                    actual = observed.stop == 'end' and observed.tokens == target
                    self.assertEqual(actual, exact_condition(matrix, target, budget))
                    METRICS['exact_theorem_queries'] += 1
            self.assertEqual(before, state(model.habits))
            METRICS['weight_graphs'] += 1

    def test_exhaustive_capacity_decay_histories_against_record_oracle(self):
        actions = [('add', 'a', 'b', 1), ('add', 'a', 'b', 2),
                   ('add', 'a', None, 1), ('add', 'a', None, 2),
                   ('add', 'b', 'a', 1), ('add', 'b', 'a', 2),
                   ('decay', 1), ('decay', 2)]
        for capacity in (None, 1, 2, 3):
            for history in product(actions, repeat=4):
                model, oracle = WeightedHabits(capacity), RecordOracle(capacity)
                for action in history:
                    if action[0] == 'add':
                        model.reinforce(*action[1:])
                        oracle.add(*action[1:])
                    else:
                        model.forget(action[1])
                        oracle.decay(action[1])
                    self.assertEqual(state(model), oracle.state())
                    self.assertTrue(all(type(w) is int and w > 0 for w in model.snapshot().values()))
                    self.assertEqual(set(model._weights), set(model._born))
                    METRICS['capacity_decay_prefixes'] += 1
                METRICS['capacity_decay_histories'] += 1

    def test_episode_practice_matches_offline_counts_and_copy_boundary(self):
        for length in range(1, 7):
            for tokens in product('ABC', repeat=length):
                model = SequenceMemory()
                mutable = list(tokens)
                model.practice(mutable, context='ctx', repetitions=3)
                mutable[:] = ['changed']
                expected = Counter(((('ctx', x), y)) for x, y in zip(tokens, tokens[1:] + (None,)))
                self.assertEqual(model.habits.snapshot(), {edge: count*3 for edge, count in expected.items()})
                self.assertEqual(model.replay(tokens[0], 'other').stop, 'missing')
                self.assertEqual(model.replay(tokens[0], 'ctx', length).stop == 'end' and
                                 model.replay(tokens[0], 'ctx', length).tokens == tokens,
                                 len(set(tokens)) == len(tokens))
                METRICS['offline_episode_counts'] += 1

    def test_minimum_practice_formula_and_finite_capacity_boundary(self):
        edges = tuple(product('AB', ('A', 'B', None)))
        for weights in product(range(3), repeat=6):
            matrix = dict(zip(edges, weights))
            for target in [('A',), ('B',), ('A','B'), ('B','A')]:
                required = []
                for x, desired in zip(target, target[1:]+(None,)):
                    competition = max([0]+[w for (k,v),w in matrix.items() if k == x and v != desired])
                    required.append(max(0, 1+competition-matrix.get((x,desired),0)))
                minimum = max(required)
                for trials in sorted({0, max(0,minimum-1), minimum, minimum+1}):
                    memory = SequenceMemory()
                    for (key,value),weight in matrix.items():
                        if weight:
                            memory.habits.reinforce(('',key),value,weight)
                    if trials:
                        memory.practice(target, repetitions=trials)
                    result = memory.replay(target[0],max_transitions=len(target))
                    self.assertEqual(result.tokens == target and result.stop == 'end', trials >= minimum)
                    METRICS['minimum_practice_queries'] += 1
                METRICS['minimum_practice_states_targets'] += 1
        for length in range(1,5):
            for target in product('ABC',repeat=length):
                for capacity,repetitions in product((1,2,3),(1,2,3)):
                    memory, oracle = SequenceMemory(capacity), RecordOracle(capacity)
                    memory.practice(iter(target),repetitions=repetitions)
                    for _ in range(repetitions):
                        for x,y in zip(target,target[1:]+(None,)):
                            oracle.add(('',x),y,1)
                    self.assertEqual(state(memory.habits),oracle.state())
                    METRICS['bounded_practice_queries'] += 1
        blocked = SequenceMemory(1)
        blocked.habits.reinforce(('', 'unrelated'), None, 2)
        blocked.practice(['A'], repetitions=100)
        self.assertEqual(blocked.replay('A').stop,'missing')

    def test_metamorphic_relabel_scale_decay_and_context_isolation(self):
        episodes = [('A', 'B', 'A'), ('A', 'C'), ('C', 'B')]
        rename = {'A': '苹果', 'B': '音', 'C': 'Z'}
        base, renamed, scaled = SequenceMemory(), SequenceMemory(), SequenceMemory()
        for tokens in episodes:
            base.practice(tokens, 'one')
            renamed.practice([rename[t] for t in tokens], 'translated')
            scaled.practice(tokens, 'one', 7)
        for cue in 'ABC':
            left = base.replay(cue, 'one', 12)
            right = renamed.replay(rename[cue], 'translated', 12)
            large = scaled.replay(cue, 'one', 12)
            self.assertEqual(right.tokens, tuple(rename[t] for t in left.tokens))
            self.assertEqual((right.stop, large.stop, large.tokens), (left.stop, left.stop, left.tokens))
            self.assertEqual(tuple(c.strength for c in large.decisions), tuple(c.strength*7 for c in left.decisions))
        before = base.replay('A', 'one', 12)
        base.practice(['A', 'C', 'C'], 'unrelated', 9)
        self.assertEqual(base.replay('A', 'one', 12), before)
        for a, b in product(range(4), repeat=2):
            left, right = WeightedHabits(), WeightedHabits()
            for k, v, w in [('A', 'B', 1), ('A', 'C', 3), ('B', None, 6)]:
                left.reinforce(k, v, w)
                right.reinforce(k, v, w)
            left.forget(a); left.forget(b); right.forget(a+b)
            self.assertEqual(state(left), state(right))
        # Capacity is shared across contexts; the isolation claim needs no eviction.
        bounded = SequenceMemory(1)
        bounded.practice(['A'], 'one')
        bounded.practice(['B'], 'two')
        self.assertEqual(bounded.replay('A', 'one').stop, 'missing')
        METRICS['metamorphic_groups'] += 5

    def test_history_collision_includes_retained_metadata_and_future_behavior(self):
        first, second = SequenceMemory(), SequenceMemory()
        first.practice(tuple('ABACABACA')); second.practice(tuple('ABACACABA'))
        self.assertNotEqual('ABACABACA', 'ABACACABA')
        self.assertEqual(state(first.habits), state(second.habits))
        self.assertEqual(first.habits.snapshot(), {(('', 'A'), 'B'):2, (('', 'B'),'A'):2,
                                                  (('', 'A'), 'C'):2, (('', 'C'),'A'):2,
                                                  (('', 'A'),None):1})
        self.assertEqual(first.habits._serial, 5)
        self.assertEqual(first.replay('A').stop, 'ambiguous')
        for tokens, repetitions, decay in [(('A','B'),2,0), (('C','A'),1,1), (('Z',),1,9)]:
            for model in (first, second):
                model.practice(tokens, repetitions=repetitions)
                model.habits.forget(decay)
            self.assertEqual(state(first.habits), state(second.habits))
            for cue in 'ABCZ':
                self.assertEqual(first.replay(cue), second.replay(cue))
        METRICS['complete_state_collision_checks'] += 4

    def test_invalid_inputs_atomicity_and_frozen_return_values(self):
        model = SequenceMemory()
        model.practice(['A','B'])
        before = state(model.habits)
        bad_calls = [lambda: model.practice([]), lambda: model.practice('AB'),
                     lambda: model.practice(['A',[]]), lambda: model.practice(['A',False]),
                     lambda: model.practice(['A'], repetitions=True),
                     lambda: model.practice(['A'], context=None),
                     lambda: model.replay('A', max_transitions=True),
                     lambda: model.replay('A', max_transitions=-1),
                     lambda: model.replay(1), lambda: model.habits.reinforce('A',[],1),
                     lambda: model.habits.reinforce('A','B',1.0), lambda: model.habits.forget(True)]
        for operation in bad_calls:
            with self.assertRaises((TypeError,ValueError)):
                operation()
            self.assertEqual(state(model.habits), before)
        replay = model.replay('A')
        with self.assertRaises(FrozenInstanceError):
            replay.stop = 'end'
        with self.assertRaises(FrozenInstanceError):
            replay.decisions[0].strength = 999
        detached = model.habits.snapshot()
        detached.clear()
        self.assertEqual(state(model.habits), before)
        model.practice(['A','C'], repetitions=2)
        self.assertEqual(replay.tokens, ('A','B'))
        self.assertEqual(replay.decisions[0].strength, 1)
        METRICS['invalid_operation_checks'] += len(bad_calls)

    def test_embodiment_direction_context_gates_provenance_and_stable_trace(self):
        body = EmbodiedMemory()
        observations = [Observation(x, Signal('hand',x)) for x in 'ABC']
        body.teach(observations, context='song', repetitions=3)
        baseline = machine_state(body)
        self.assertIsNone(body.active)
        body.sense(Signal('hand','A'), 'song')
        trace = body.recall('song', 3)
        self.assertEqual([e.source for e in trace.events], ['external','replay','replay'])
        self.assertEqual([e.supports_external_object for e in trace.events], [True,False,False])
        self.assertEqual([event.cause for event in trace.outputs], list(trace.events))
        self.assertEqual([event.signal for event in trace.outputs], [o.signal for o in observations])
        self.assertEqual(body.feedback(trace.outputs[-1], 'song').event.source, 'feedback')
        self.assertFalse(body.active.supports_external_object)
        self.assertEqual(machine_state(body), baseline)
        body.clear_active()
        self.assertEqual(machine_state(body), baseline)
        body.set_cue('A'); body.efferent_enabled = False
        quiet = body.recall('song', 3)
        self.assertEqual(quiet.replay.tokens, ('A','B','C'))
        self.assertEqual(quiet.outputs, (None,None,None))
        body.afferent_enabled = False
        self.assertEqual(body.feedback(trace.outputs[0], 'song').status, 'blocked')
        self.assertIsNone(body.active)
        body.afferent_enabled = True
        self.assertEqual(body.sense(Signal('hand','A'), 'other').status, 'missing')
        body.set_cue('A')
        self.assertEqual(body.recall('other',0).replay.stop, 'budget')
        self.assertEqual(len(body.recall('other',0).events), 1)
        body.forget(3)
        self.assertEqual([s[1] for s in machine_state(body)], [{},{},{}])
        self.assertEqual(trace.events[0], IdeaEvent('A','external'))
        self.assertEqual(trace.replay.tokens, ('A','B','C'))
        self.assertEqual(trace.replay.decisions[0].strength,3)
        # The three tables are separately mutable, not aliased or automatically reciprocal.
        independent = EmbodiedMemory()
        independent.incoming.reinforce(('', Signal('eye','red')), 'red')
        self.assertEqual(independent.sense(Signal('eye','red')).event.idea,'red')
        self.assertIsNone(independent.express())
        self.assertEqual(independent.brain.habits.edge_count, 0)
        METRICS['embodied_contract_groups'] += 9


if __name__ == '__main__':
    tree = ast.parse(Path(__file__).read_text(encoding='utf-8'))
    if any(isinstance(node, ast.Assert) for node in ast.walk(tree)):
        raise RuntimeError('Independent checks must not disappear under optimization')
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(IndependentContractTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    summary = {'stage':'complete', 'tests':result.testsRun, 'failures':len(result.failures),
               'errors':len(result.errors), 'skips':len(result.skipped),
               'optimized':sys.flags.optimize, 'metrics':dict(METRICS),
               'model_sha256':hashlib.sha256((ROOT/'model.py').read_bytes()).hexdigest(),
               'bare_asserts':0}
    print('INDEPENDENT_RESULT=' + json.dumps(summary, sort_keys=True))
    sys.exit(0 if result.wasSuccessful() and result.testsRun == 8 else 1)
