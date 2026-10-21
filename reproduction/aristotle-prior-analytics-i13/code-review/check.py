"""Independent integer-mask oracle plus isolated mutation checks; standard library."""
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import model

def require(value, message):
    if not value:
        raise RuntimeError(message)

counts = {'models': 0, 'fixed_subject_pairs': 0, 'sentence_vectors': 0}
for worlds in (1, 2, 3):
    for bits in itertools.product(range(4), repeat=2*worlds):
        aa, bb = bits[:worlds], bits[worlds:]
        ext = lambda masks: tuple(frozenset(x for x in range(2) if mask >> x & 1) for mask in masks)
        m = model.Model(2, ext(aa), ext(bb))
        counts['models'] += 1
        require(m.complement().A == ext(tuple(a ^ 3 for a in aa)) and m.complement().B == m.B, 'complement extension oracle')
        require(m.swap().A == m.B and m.swap().B == m.A, 'swap extension oracle')
        varying = sum(1 << x for x in range(2) if len({a >> x & 1 for a in aa}) == 2)
        possible_b = 0
        for b in bb: possible_b |= b
        require(m.subject() == ext((bb[0],))[0], 'actual subject')
        require(m.subject('possible') == ext((possible_b,))[0], 'possible subject')
        for sm in range(4):
            ss = ext((sm,))[0]
            counts['fixed_subject_pairs'] += 1
            require(m.all_each_contingent(ss) == (sm & varying == sm), 'U oracle')
            require(m.some_each_contingent(ss) == bool(sm & varying), 'T oracle')
            expected = {
                'all': tuple(a & sm == sm for a in aa),
                'none': tuple(a & sm == 0 for a in aa),
                'some': tuple(a & sm != 0 for a in aa),
                'notall': tuple(a & sm != sm for a in aa),
            }
            for form, values in expected.items():
                counts['sentence_vectors'] += 1
                require(m.sentence(ss, form) == values, 'sentence oracle')
                require(m.sentence_contingent(ss, form) == (len(set(values)) == 2), 'C oracle')

runs = []
for mode in ([], ['-O'], ['-OO']):
    label = mode[0] if mode else 'normal'
    p = subprocess.run([sys.executable, *mode, '-m', 'unittest', '-v', 'test_model'], cwd=ROOT, capture_output=True, text=True)
    (ROOT/'code-review'/('tests-'+label.lstrip('-')+'.txt')).write_text(p.stdout+p.stderr)
    require(p.returncode == 0, 'tests failed: '+label)
    d = subprocess.run([sys.executable, *mode, 'demo.py'], cwd=ROOT, capture_output=True, text=True)
    require(d.returncode == 0 and not d.stderr, 'demo failed')
    require(d.stdout == (ROOT/'results.json').read_text(), 'saved results byte mismatch')
    (ROOT/'code-review'/('demo-'+label.lstrip('-')+'.txt')).write_text(d.stdout)
    runs.append({'mode': label, 'tests_returncode': p.returncode, 'demo_exact': True})

source = (ROOT/'model.py').read_text()
mutations = {
    'C_becomes_possible': ('return any(v) and not all(v)', 'return any(v)'),
    'U_becomes_existential': ('return all(self.individual(x) for x in self.check_subject(S))', 'return any(self.individual(x) for x in self.check_subject(S))'),
    'T_becomes_universal': ('return any(self.individual(x) for x in self.check_subject(S))', 'return all(self.individual(x) for x in self.check_subject(S))'),
    'possible_subject_actual_only': ('return frozenset().union(*self.B)', 'return self.B[0]'),
    'all_becomes_some': ("if form == 'all': return S <= A", "if form == 'all': return bool(S & A)"),
    'none_becomes_notall': ("if form == 'none': return not (S & A)", "if form == 'none': return bool(S - A)"),
    'complement_identity': ('tuple(U - A for A in self.A)', 'tuple(A for A in self.A)'),
    'accept_empty_truth_vector': ('or not values:', ':'),
}
mutation_results = []
for name, (old, new) in mutations.items():
    require(source.count(old) == 1, 'mutation location not unique')
    with tempfile.TemporaryDirectory() as temp:
        td = Path(temp)
        (td/'model.py').write_text(source.replace(old,new))
        (td/'test_model.py').write_text((ROOT/'test_model.py').read_text())
        p = subprocess.run([sys.executable, '-m', 'unittest', 'test_model'], cwd=td, capture_output=True, text=True)
        killed = p.returncode != 0
        mutation_results.append({'mutation':name,'killed_by_original_tests':killed,'returncode':p.returncode,'test_summary':next((line for line in reversed(p.stderr.splitlines()) if line.startswith(('FAILED (','OK'))),'no summary')})

result = {'oracle':counts,'reruns':runs,'mutations':mutation_results,'limitations':'Finite checks only; selected mutants are a diagnostic, not a completeness guarantee.'}
print(json.dumps(result, indent=2))
