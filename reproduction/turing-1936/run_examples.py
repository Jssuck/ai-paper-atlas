"""Print reproducible JSON evidence to stdout; uses only Python's standard library."""
import json
import platform
import sys
from collections import Counter
from simulator import (run, alternating, alternating_spaced, one_then_silent,
                       delayed_forever, silent_forever, enumerate_one_state)

cases = {
    'alternating_6': run(alternating(), 6),
    'source_aligned_alternating_12': run(alternating_spaced(), 12),
    'one_then_silent_12': run(one_then_silent(), 12),
    'delayed_20_at_cap_20': run(delayed_forever(20), 20),
    'delayed_20_at_cap_24': run(delayed_forever(20), 24),
    'silent_at_cap_20': run(silent_forever(), 20),
}
counts = Counter()
statuses = Counter()
for machine in enumerate_one_state():
    r = run(machine, 20)
    counts[len(r['output'])] += 1
    statuses[r['status']] += 1
report = {
    'environment': {'python': sys.version, 'implementation': platform.python_implementation(),
                    'platform': platform.platform(), 'dependencies': 'Python standard library only'},
    'model': 'Modern deterministic one-work-tape transducer with observable emit annotation',
    'cases': cases,
    'finite_enumeration': {
        'scope': 'All total one-state tables over work alphabet {_,x}; 18 actions per entry',
        'machine_count': sum(counts.values()), 'cap_per_machine': 20,
        'observed_output_length_histogram': dict(sorted(counts.items())),
        'observed_status_histogram': dict(statuses),
        'warning': 'No inferred circle-free classification; finite observations are not a general decision procedure.'
    }
}
print(json.dumps(report, indent=2, ensure_ascii=False))
