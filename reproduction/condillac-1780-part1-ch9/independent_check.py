"""Independent finite-model audit; checks are explicit under python -O/-OO."""
from pathlib import Path
import itertools
import json
import random
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from model import SequenceMemory, WeightedHabits, EmbodiedMemory, Observation, Signal


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def reference_replay(rows, cue, budget):
    tokens = [cue]
    for used in range(budget):
        row = rows[tokens[-1]]
        positive = [(v, w) for v, w in row.items() if w > 0]
        if not positive:
            return tuple(tokens), 'missing', used + 1
        winner, score = max(positive, key=lambda item: item[1])
        if sum(w == score for _, w in positive) != 1:
            return tuple(tokens), 'ambiguous', used + 1
        if winner is None:
            return tuple(tokens), 'end', used + 1
        tokens.append(winner)
    return tuple(tokens), 'budget', budget


def main():
    symbols = ('A', 'B')
    outcomes = ('A', 'B', None)
    replay_checks = target_checks = 0
    for vector in itertools.product(range(3), repeat=6):
        m = SequenceMemory()
        rows = {x: dict(zip(outcomes, vector[i*3:i*3+3])) for i, x in enumerate(symbols)}
        for x, row in rows.items():
            for y, weight in row.items():
                if weight:
                    m.habits.reinforce(('', x), y, weight)
        for cue in symbols:
            for budget in range(6):
                result = m.replay(cue, max_transitions=budget)
                require((result.tokens, result.stop, len(result.decisions)) == reference_replay(rows, cue, budget),
                        ('replay', vector, cue, budget))
                replay_checks += 1
        for length in range(1, 5):
            for target in itertools.product(symbols, repeat=length):
                edges = tuple(zip(target, target[1:] + (None,)))
                criterion = all(rows[x][y] > 0 and all(rows[x][y] > w for z, w in rows[x].items() if z != y)
                                for x, y in edges)
                got = m.replay(target[0], max_transitions=length)
                require((got.tokens == target and got.stop == 'end') == criterion, ('criterion', vector, target))
                target_checks += 1
    rng = random.Random(1780)
    capacity_checks = 0
    for trial in range(250):
        cap = rng.choice([None, 1, 2, 3, 4])
        h = WeightedHabits(cap)
        state, born, serial = {}, {}, 0
        for step in range(40):
            if rng.random() > .25:
                edge = (rng.choice(symbols), rng.choice(outcomes))
                amount = rng.randrange(1, 5)
                if edge not in state:
                    born[edge] = serial
                    serial += 1
                state[edge] = state.get(edge, 0) + amount
                if cap is not None and len(state) > cap:
                    ordered = sorted(((weight, born[e], e) for e, weight in state.items()), key=lambda v:(v[0],v[1]))
                    victim = ordered[0][2]
                    del state[victim]
                    del born[victim]
                h.reinforce(edge[0], edge[1], amount)
            else:
                amount = rng.randrange(4)
                state = {e: w-amount for e, w in state.items() if w > amount}
                born = {e: b for e, b in born.items() if e in state}
                h.forget(amount)
            require(h.snapshot() == state and h._born == born and h._serial == serial,
                    ('capacity_decay', trial, step))
            capacity_checks += 1
    m1, m2 = SequenceMemory(), SequenceMemory()
    histories = (tuple('ABACABACA'), tuple('ABACACABA'))
    m1.practice(histories[0]); m2.practice(histories[1])
    require(histories[0] != histories[1], 'history pair must differ')
    require(m1.habits.__dict__ == m2.habits.__dict__, 'full learned SequenceMemory state must agree')
    e = EmbodiedMemory()
    e.teach([Observation('red', Signal('sensor', 'stimulus'))])
    external = e.sense(Signal('sensor', 'stimulus')).event
    e.set_cue('red')
    body = e.express()
    feedback = e.feedback(body).event
    require(external.idea == feedback.idea and external.source != feedback.source, 'provenance collision')
    # Deliberate learned-label mismatch: this flag certifies an input route, not worldly truth.
    require(external.supports_external_object, 'external flag should match intended API contract')
    print(json.dumps({'success': True, 'optimization': sys.flags.optimize,
                      'two_state_weight_assignments': 729, 'reference_replay_checks': replay_checks,
                      'exact_recovery_iff_checks': target_checks,
                      'capacity_decay_full_state_checks': capacity_checks,
                      'noninjective_full_state_pair': ['ABACABACA','ABACACABA'],
                      'provenance_collision_checked': True,
                      'limits': ['finite tests do not prove unbounded theorems',
                                 'provenance flag describes trusted caller route, not world truth',
                                 'no medical or neuroscience validation']}, indent=2))

if __name__ == '__main__':
    main()
