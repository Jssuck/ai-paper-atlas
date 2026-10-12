"""Independent bounded checks for the public argument audit (standard library).

Planning oracle: bit-mask dynamic programming in increasing mask order.
Teaching oracle: dynamic programming over eliminated wrong-row masks.
These finite checks are not general proofs or educational experiments.
"""
from datetime import datetime, timezone
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))
from model import (HypothesisSpace, Lesson, PlanningProblem, closure,
                   is_identified, minimum_teaching_set, replay, shortest_plan,
                   version_space)


def require(condition, description):
    if not condition:
        raise RuntimeError(description)


def skills(mask, width):
    return frozenset(f's{i}' for i in range(width) if mask & (1 << i))


def run_planning():
    width = 3
    limit = 1 << width
    rules = tuple(product(range(limit), range(1, limit)))
    cases = 0
    dp_runs = 0
    for size in range(3):
        for selected in combinations(rules, size):
            lessons = tuple(Lesson(f'L{i}', skills(p, width), skills(g, width))
                            for i, (p, g) in enumerate(selected))
            for initial in range(limit):
                distance = [None] * limit
                distance[initial] = 0
                for state in range(limit):
                    if distance[state] is None:
                        continue
                    for pre, gain in selected:
                        after = state | gain
                        if state & pre == pre and after != state:
                            proposal = distance[state] + 1
                            if distance[after] is None or proposal < distance[after]:
                                distance[after] = proposal
                reachable = tuple(s for s, d in enumerate(distance) if d is not None)
                union = 0
                for state in reachable:
                    union |= state
                # Monotone serializability says the union is itself reachable.
                require(distance[union] is not None, 'reachable union not reachable')
                dp_runs += 1
                for target in range(limit):
                    problem = PlanningProblem(skills(limit - 1, width), skills(initial, width),
                                              skills(target, width), lessons)
                    expected = [distance[s] for s in reachable if s & target == target]
                    expected_length = min(expected) if expected else None
                    actual = shortest_plan(problem)
                    require((None if actual is None else len(actual)) == expected_length,
                            'BFS disagrees with ordered-mask DP')
                    require(closure(problem) == skills(union, width), 'closure disagrees with DP')
                    require((target & union == target) == (actual is not None),
                            'reachability equivalence failed')
                    if actual is not None:
                        require(problem.goal <= replay(problem, actual), 'replay missed target')
                        require(len(actual) <= width - initial.bit_count(), 'strict growth bound')
                    cases += 1
    return {'skill_count': width, 'maximum_distinct_rules': 2,
            'rule_kinds': len(rules), 'oracle_dp_runs': dp_runs, 'goal_cases': cases}


def teaching_number_by_elimination_dp(rows, target, width):
    if target not in rows:
        return None
    wrong = tuple(row for row in rows if row != target)
    covers = tuple(sum(1 << j for j, row in enumerate(wrong) if row[i] != target[i])
                   for i in range(width))
    distance = {0: 0}
    for coverage in covers:
        previous = tuple(distance.items())
        for eliminated, count in previous:
            new = eliminated | coverage
            distance[new] = min(distance.get(new, width + 1), count + 1)
    return distance[(1 << len(wrong)) - 1]


def run_teaching():
    min_cases = filter_cases = hitting_cases = 0
    for width in range(3):
        domain = tuple(f'x{i}' for i in range(width))
        all_rows = tuple(product((0, 1), repeat=width))
        for length in range(4):
            for rows in product(all_rows, repeat=length):
                space = HypothesisSpace(domain, rows)
                for target in all_rows:
                    answer = minimum_teaching_set(space, target)
                    expected_size = teaching_number_by_elimination_dp(rows, target, width)
                    require((None if answer is None else len(answer)) == expected_size,
                            'minimum teaching disagrees with elimination DP')
                    if answer is not None:
                        require(is_identified(space, target, answer), 'teaching answer not identifying')
                    min_cases += 1
                    for selected_mask in range(1 << width):
                        observations = tuple((domain[i], target[i]) for i in range(width)
                                             if selected_mask & (1 << i))
                        hit = all(row == target or any(selected_mask & (1 << i)
                                  and row[i] != target[i] for i in range(width)) for row in rows)
                        require(is_identified(space, target, observations)
                                == (target in rows and hit), 'conditional hitting equivalence')
                        hitting_cases += 1
                    for labels in product(((), (0,), (1,), (0, 1)), repeat=width):
                        observations = tuple((domain[i], label) for i in range(width)
                                             for label in labels[i])
                        retained = set(range(len(rows)))
                        for i in range(width):
                            for label in labels[i]:
                                retained.difference_update(j for j, row in enumerate(rows)
                                                           if row[i] != label)
                        expected = tuple(sorted(retained))
                        require(version_space(space, observations) == expected, 'filter oracle')
                        require(version_space(space, tuple(reversed(observations))) == expected,
                                'filter order invariance')
                        require(version_space(space, observations + observations) == expected,
                                'filter duplicate invariance')
                        identified = bool(expected) and all(rows[j] == target for j in expected)
                        require(is_identified(space, target, observations) == identified,
                                'nonempty behavior identification')
                        filter_cases += 1
    return {'domain_sizes': [0, 1, 2], 'ordered_family_lengths': [0, 1, 2, 3],
            'duplicates_included': True, 'minimum_target_cases': min_cases,
            'target_subset_hitting_cases': hitting_cases,
            'target_observation_cases': filter_cases}


def main():
    result = {'generated_at_utc': datetime.now(timezone.utc).isoformat(),
              'python': sys.version, 'optimization_level': sys.flags.optimize,
              'source_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in (BASE / 'model.py', Path(__file__))},
              'planning': run_planning(), 'teaching': run_teaching(),
              'status': 'pass',
              'limitation': 'Bounded implementation checks; not a general proof or educational experiment.'}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
