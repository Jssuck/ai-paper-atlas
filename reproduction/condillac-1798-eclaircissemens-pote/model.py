"""Finite teaching model; no dependencies, physical clock, or historical attribution."""
from fractions import Fraction


def _word(word, name='word'):
    if type(word) is not tuple:
        raise TypeError(f'{name} must be a tuple')
    if not word or any(type(x) is not str or not x for x in word):
        raise ValueError(f'{name} must contain nonempty strings')
    return word


def compress(word):
    """Delete adjacent repetitions from a nonempty tuple of string labels."""
    _word(word)
    return tuple(x for i, x in enumerate(word) if i == 0 or x != word[i-1])


def change_count(word):
    _word(word)
    return sum(a != b for a, b in zip(word, word[1:]))


def observe(trace, h):
    _word(trace, 'trace')
    if type(h) is not dict:
        raise TypeError('h must be a dict')
    if any(type(k) is not str or not k or type(v) is not str or not v
           for k, v in h.items()):
        raise ValueError('h keys and values must be nonempty strings')
    if not set(trace) <= h.keys():
        raise ValueError('h must cover every state appearing in trace')
    return tuple(h[x] for x in trace)


def idea_word(trace, h):
    return compress(observe(trace, h))


def factors_through(observations, targets):
    """Finite fiber criterion. Return a decoder on the observed image or None.

    observations and targets correspond positionwise to a supplied finite domain.
    This says nothing about inputs outside that domain.
    """
    _word(observations, 'observations')
    _word(targets, 'targets')
    if len(observations) != len(targets):
        raise ValueError('observations and targets must have equal lengths')
    decoder = {}
    for observation, target in zip(observations, targets):
        if observation in decoder and decoder[observation] != target:
            return None
        decoder[observation] = target
    return decoder


def _schedule(schedule):
    if type(schedule) is not tuple:
        raise TypeError('schedule must be a tuple')
    if not schedule:
        raise ValueError('schedule must be nonempty')
    for event in schedule:
        if type(event) is not tuple or len(event) != 2:
            raise ValueError('each event must be a (Fraction, nonempty string) tuple')
        t, label = event
        if type(t) is not Fraction:
            raise TypeError('event coordinates must be Fraction, not float or int')
        if type(label) is not str or not label:
            raise ValueError('event labels must be nonempty strings')
        if not Fraction(0) <= t < Fraction(1):
            raise ValueError('event coordinates must lie in [0,1)')
    if schedule[0][0] != 0:
        raise ValueError('schedule must begin at 0')
    if any(a[0] >= b[0] for a, b in zip(schedule, schedule[1:])):
        raise ValueError('event coordinates must be strictly increasing')


def synchronize(schedules):
    """Common refinement on a GIVEN shared coordinate interval [0,1).

    Each event label holds on [event time, next event time), or to 1.
    Return (left, right, labels) rows. Adjacent identical labels are allowed.
    """
    if type(schedules) is not tuple:
        raise TypeError('schedules must be a tuple')
    if not schedules:
        raise ValueError('at least one schedule is required')
    for schedule in schedules:
        _schedule(schedule)
    cuts = sorted({t for schedule in schedules for t, _ in schedule} | {Fraction(1)})
    positions = [0] * len(schedules)
    rows = []
    for left, right in zip(cuts, cuts[1:]):
        for i, schedule in enumerate(schedules):
            while positions[i]+1 < len(schedule) and schedule[positions[i]+1][0] <= left:
                positions[i] += 1
        rows.append((left, right, tuple(s[positions[i]][1] for i, s in enumerate(schedules))))
    return tuple(rows)
