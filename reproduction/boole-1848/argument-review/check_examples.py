"""Independent checks of five section-9 implications and the p193 wording discrepancy.
Not a proof of the general historical syllogistic rule system.
"""
from itertools import product
u = frozenset(range(3))
sets = [frozenset(i for i in u if mask >> i & 1) for mask in range(8)]
counts = [0] * 5
for x, y, z in product(sets, repeat=3):
    premises = [y <= x and z <= y,
                x <= y and not z & y,
                x <= y and bool(z-y),
                y <= x and u-y <= z,
                bool(y-x) and z <= u-y]
    conclusions = [z <= x, not x & z, bool(z-x),
                   u-x <= z and u-z <= x, bool((u-z) & (u-x))]
    for i, (p, c) in enumerate(zip(premises, conclusions)):
        if p:
            if not c:
                raise RuntimeError((i, x, y, z))
            counts[i] += 1
# Original p193: 'All Xs are Ys' is not 'No not-Xs are Ys'.
x, y = frozenset({0}), frozenset({0, 1})
if not (x <= y and bool((u-x) & y)):
    raise RuntimeError('Expected wording counterexample failed')
print('512 X/Y/Z assignments; five implications per assignment; all passed.')
print('Premise-satisfying counts:', counts)
print('Original p193 wording counterexample passed: X={0}, Y={0,1}, U={0,1,2}.')
print('Finite checks supplement the general set proofs; they do not prove the full historical system.')
