"""Independent truth-table audit; not an implementation of ancient modal logic."""
import itertools
import json
from pathlib import Path
import model as subject


def equal(actual, expected, label):
    if actual != expected:
        raise RuntimeError(f'{label}: expected {expected!r}, received {actual!r}')


def rejected(call, label):
    try:
        call()
    except (TypeError, ValueError):
        return
    raise RuntimeError(f'{label}: malformed input accepted')


def scenario_counts(n):
    # Enumerate each person's ordered scenario pair, unlike world-major author loop.
    choices = list(itertools.product((0, 1, 2), repeat=2))
    count = pre_count = bad_count = gap_count = 0
    for rows in itertools.product(choices, repeat=n):
        disease_sets = [{w for w, s in enumerate(row) if s == 2} for row in rows]
        health_sets = [{w for w, s in enumerate(row) if s == 1} for row in rows]
        everyone_can = all(bool(s) for s in disease_sets)
        common = set((0, 1))
        for ds in disease_sets:
            common.intersection_update(ds)
        no_health_anywhere = not any(health_sets)
        count += 1
        pre_count += everyone_can
        bad_count += everyone_can and not no_health_anywhere
        gap_count += everyone_can and not common
        cells = tuple(rows[p][w] for w in range(2) for p in range(n))
        m = subject.from_cells(n, cells)
        equal(m.all_possibly(subject.DISEASE), everyone_can, 'forall exists')
        equal(m.possibly_all(subject.DISEASE), bool(common), 'exists forall')
        equal(m.necessarily_none(subject.HEALTH), no_health_anywhere, 'all absent')
        equal(m.possibly_none(subject.HEALTH),
              any(all(w not in hs for hs in health_sets) for w in (0, 1)), 'some absent')
        for p, h, d in zip(m.persons, health_sets, disease_sets):
            equal(m.possible(subject.HEALTH, p), bool(h), 'health witness')
            equal(m.possible(subject.DISEASE, p), bool(d), 'disease witness')
            equal(m.joint_possible(subject.HEALTH, subject.DISEASE, p), bool(h & d), 'joint')
    expected = dict(persons=n, scenarios=2, models=count,
                    all_possibly_diseased=pre_count,
                    counterexamples_to_necessarily_no_health=bad_count,
                    universal_possibility_scope_gaps=gap_count)
    equal(subject.survey(n), expected, 'survey totals')
    return expected


def classical_counts(n):
    # Each object independently carries A/B/C bits; check implications pointwise.
    cases = prem = failures = 0
    for rows in itertools.product(tuple(itertools.product((False, True), repeat=3)), repeat=n):
        antecedent = all(not (a and b) and (not c or b) for a, b, c in rows)
        conclusion = all(not (a and c) for a, b, c in rows)
        sets = [{i for i, row in enumerate(rows) if row[k]} for k in range(3)]
        equal(subject.celarent(*sets), (antecedent, conclusion), 'Celarent truth table')
        cases += 1
        prem += antecedent
        failures += antecedent and not conclusion
    result = dict(persons=n, triples=cases, true_premises=prem, failures=failures)
    equal(subject.celarent_survey(n), result, 'Celarent totals')
    return result


def validation():
    empty = subject.from_cells(0, ())
    for name in ('all_possibly', 'possibly_all', 'possibly_none', 'necessarily_none'):
        for bad in ('health', subject.Condition('unknown')):
            rejected(lambda name=name, bad=bad: getattr(empty, name)(bad), name)
    neither = subject.from_cells(1, (0, 0))
    p = neither.persons[0]
    rejected(lambda: neither.joint_possible(subject.HEALTH, 'disease', p), 'short-circuit second type')
    rejected(lambda: neither.joint_possible(subject.HEALTH, subject.Condition('unknown'), p), 'short-circuit second name')
    rejected(lambda: neither.holds(subject.HEALTH, subject.DISEASE, 'w0'), 'condition as person')
    rejected(lambda: subject.from_cells(True, (1, 2)), 'boolean domain size')
    rejected(lambda: subject.ScenarioModel((), (), {}), 'empty world set')
    rejected(lambda: neither.holds(subject.HEALTH, p, 'unknown'), 'unknown world')
    return 'passed empty-domain and short-circuit malformed-input checks'


if __name__ == '__main__':
    result = {'scenario_counts': [scenario_counts(n) for n in range(4)],
              'classical_counts': [classical_counts(n) for n in range(4)],
              'validation': validation()}
    stored = json.loads(Path('results.json').read_text())
    equal(stored['scenario_surveys'], result['scenario_counts'][:3], 'published scenario results')
    equal(stored['celarent_surveys'], result['classical_counts'], 'published classical results')
    print(json.dumps(result, indent=2))
    print('PASS independent truth tables, method-by-method comparisons and published counts')
