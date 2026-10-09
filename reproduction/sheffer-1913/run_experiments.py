"""Generate measured outputs without external packages, downloads, or training."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import sys
import time

import sheffer as s


def run():
    started = time.perf_counter()
    results = {
        'reconstruction': 'Original teaching implementation; Sheffer 1913 did not publish software.',
        'finite_historical_models': {name: model.check() for name, model in s.original_finite_models().items()},
        'infinite_rational_model': s.rational_symbolic_results(),
        'closed_table_enumeration': [s.enumerate_closed(n) for n in (1, 2, 3)],
        'translation': s.translation_experiment(),
        'negative_controls': {},
    }
    p, q = ('var', 'p'), ('var', 'q')
    for label, wrong in [('omitted_final_negation', ('nor',p,q)),
                         ('nor_formula_relabeled_nand', ('nand',('nand',p,q),('nand',p,q)))]:
        same, witness = s.equivalent(s.parse('p | q'), wrong)
        results['negative_controls'][label] = {'equivalent': same, 'counterexample': witness}
        assert not same
    results['execution'] = {
        'timestamp_utc': datetime.now(timezone.utc).isoformat(),
        'python': sys.version,
        'platform': platform.platform(),
        'runtime_seconds': round(time.perf_counter() - started, 6),
        'dependencies': 'Python standard library only',
        'scope': 'Finite table checks and bounded formula tests do not prove the general representation theorem.'
    }
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='results/experiments.json')
    args = parser.parse_args()
    results = run()
    path = Path(args.out)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Sheffer 1913: original teaching reconstruction, stdlib only')
    for name, model in s.original_finite_models().items():
        print(f'{name}: P1–P5 = {model.signature()}')
    print('Rational P4 counterexample:', results['infinite_rational_model']['P4_witness'])
    for row in results['closed_table_enumeration']:
        print(f"n={row['n']}: {row['tables_examined']} closed labeled tables; {row['all_five_count']} satisfy P1–P5")
    print('Translation:', results['translation'])
    print('Negative controls:', results['negative_controls'])
    print('Result JSON:', path)
    print('Runtime:', results['execution']['runtime_seconds'], 'seconds')
