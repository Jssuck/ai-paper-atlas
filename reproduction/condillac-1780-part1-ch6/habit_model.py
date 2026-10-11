"""Modern teaching stipulation, not Condillac's algorithm or a psychology model."""

from fractions import Fraction


def _rational(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, Fraction)):
        raise TypeError(f"{name} must be int or Fraction; float/bool are rejected")
    return Fraction(value)


def _inputs(inputs):
    if isinstance(inputs, (str, bytes)):
        raise TypeError("inputs must be a collection of binary integers, not str/bytes")
    result = tuple(inputs)
    if any(type(u) is not int or u not in (0, 1) for u in result):
        raise ValueError("each input must be an integer 0 or 1 (not bool)")
    return result


def _arguments(alpha, initial, inputs):
    alpha, initial = _rational(alpha, "alpha"), _rational(initial, "initial")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be strictly between 0 and 1")
    if not 0 <= initial <= 1:
        raise ValueError("initial must be in [0, 1]")
    return alpha, initial, _inputs(inputs)


def habit_trace(alpha, initial, inputs):
    """Return (h_0, ..., h_n), with h_(t+1)=(1-alpha)*h_t+alpha*u_t."""
    alpha, initial, inputs = _arguments(alpha, initial, inputs)
    trace = [initial]
    for u in inputs:
        trace.append((1 - alpha) * trace[-1] + alpha * u)
    return tuple(trace)


def habit_closed_form(alpha, initial, inputs):
    """Evaluate the exact finite weighted-sum formula, including the empty path."""
    alpha, initial, inputs = _arguments(alpha, initial, inputs)
    n = len(inputs)
    return (1 - alpha) ** n * initial + alpha * sum(
        ((1 - alpha) ** (n - 1 - k) * u for k, u in enumerate(inputs)),
        Fraction(0),
    )


def action_inputs(actions, tracked_action):
    """Mark occurrences of one named action; this does not infer an intention."""
    if isinstance(actions, (str, bytes)):
        raise TypeError("actions must be a collection of labels, not a scalar str/bytes")
    if not isinstance(tracked_action, str) or not tracked_action:
        raise ValueError("tracked_action must be a nonempty string")
    actions = tuple(actions)
    if any(not isinstance(a, str) or not a for a in actions):
        raise ValueError("actions must be nonempty strings")
    return tuple(int(a == tracked_action) for a in actions)
