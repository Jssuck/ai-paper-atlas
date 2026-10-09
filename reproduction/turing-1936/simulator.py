"""Auditable teaching transducer; not Turing's full historical universal machine.

One bi-infinite work tape, finite deterministic transition table, and an append-only
observable output stream. `emit` is a modern annotation, not a second readable tape.
All machines start on a blank tape with head at 0. Missing rules halt.
"""
from dataclasses import dataclass
from itertools import product

BLANK = '_'


@dataclass(frozen=True)
class Action:
    state: str
    write: str
    move: int
    emit: str = ''


class Machine:
    def __init__(self, states, alphabet, start, rules):
        self.states = frozenset(states)
        self.alphabet = frozenset(alphabet)
        self.start = start
        self.rules = dict(rules)
        if start not in self.states or BLANK not in self.alphabet:
            raise ValueError('Invalid start or missing blank')
        for (q, symbol), a in self.rules.items():
            if q not in self.states or a.state not in self.states:
                raise ValueError('Unknown state')
            if symbol not in self.alphabet or a.write not in self.alphabet:
                raise ValueError('Unknown symbol')
            if a.move not in (-1, 0, 1) or a.emit not in ('', '0', '1'):
                raise ValueError('Invalid movement or output')


def run(machine, cap):
    """Execute at most cap transitions, including initial configuration in trace.

    Status is halted iff the terminal configuration has no rule. Otherwise it is
    cap_reached: an observation limit, never a verdict about infinite behavior.
    """
    if not isinstance(cap, int) or cap < 0:
        raise ValueError('cap must be a nonnegative integer')
    state, head, tape, output = machine.start, 0, {}, ''
    trace = []

    def snapshot(step, emitted):
        return dict(step=step, state=state, head=head,
                    scanned=tape.get(head, BLANK),
                    tape={str(k): tape[k] for k in sorted(tape)},
                    emitted=emitted, output=output)

    trace.append(snapshot(0, ''))
    for step in range(1, cap + 1):
        a = machine.rules.get((state, tape.get(head, BLANK)))
        if a is None:
            break
        if a.write == BLANK:
            tape.pop(head, None)
        else:
            tape[head] = a.write
        head += a.move
        state = a.state
        output += a.emit
        trace.append(snapshot(step, a.emit))
    status = ('halted' if (state, tape.get(head, BLANK)) not in machine.rules
              else 'cap_reached')
    return dict(cap=cap, steps=len(trace) - 1, status=status, output=output,
                trace=trace)


def alternating():
    # Modern two-state simplification, one printed bit per transition.
    return Machine({'a', 'b'}, {'_', '0', '1'}, 'a', {
        ('a', '_'): Action('b', '0', 1, '0'),
        ('b', '_'): Action('a', '1', 1, '1'),
    })


def alternating_spaced():
    # Source-aligned layout of section 3, example I (p. 233).
    # State names normalized to p0, gap0, p1, gap1, not a facsimile transcription.
    return Machine({'p0', 'gap0', 'p1', 'gap1'}, {'_', '0', '1'}, 'p0', {
        ('p0', '_'): Action('gap0', '0', 1, '0'),
        ('gap0', '_'): Action('p1', '_', 1),
        ('p1', '_'): Action('gap1', '1', 1, '1'),
        ('gap1', '_'): Action('p0', '_', 1),
    })


def one_then_silent():
    return Machine({'first', 'silent'}, {'_', '0'}, 'first', {
        ('first', '_'): Action('silent', '0', 1, '0'),
        ('silent', '_'): Action('silent', '_', 1),
    })


def delayed_forever(delay):
    """delay silent steps; first output at delay+1, then infinitely many zeros."""
    if not isinstance(delay, int) or delay < 0:
        raise ValueError('delay must be a nonnegative integer')
    states = {f'd{i}' for i in range(delay)} | {'emit'}
    rules = {(f'd{i}', '_'): Action(f'd{i+1}' if i+1 < delay else 'emit', '_', 1)
             for i in range(delay)}
    rules[('emit', '_')] = Action('emit', '0', 1, '0')
    return Machine(states, {'_', '0'}, 'd0' if delay else 'emit', rules)


def silent_forever():
    return Machine({'silent'}, {'_'}, 'silent', {
        ('silent', '_'): Action('silent', '_', 1)})


def enumerate_one_state():
    """All 18^2 total tables on fixed states={q}, alphabet={_,x}.

    Per (q,symbol) choose write in {_,x}, move in {-1,0,1}, emit in {'',0,1}.
    This deliberately small modern transducer class does not enumerate all TMs.
    """
    actions = [Action('q', w, d, e)
               for w, d, e in product(('_', 'x'), (-1, 0, 1), ('', '0', '1'))]
    for blank_action, x_action in product(actions, repeat=2):
        yield Machine({'q'}, {'_', 'x'}, 'q', {
            ('q', '_'): blank_action, ('q', 'x'): x_action})
