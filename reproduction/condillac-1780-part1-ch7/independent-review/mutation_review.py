"""Run independent audit against specific semantic mistakes; never edit model.py."""
from pathlib import Path
import concurrent.futures, hashlib, json, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parent
MODEL=ROOT.parent/'model.py'
FLAGS=['-O'] if sys.flags.optimize==1 else (['-OO'] if sys.flags.optimize==2 else [])
MUTATIONS=(
 ('unknown_as_equal','return "unknown"','return "equal"'),
 ('invert_comparison','return "equal" if left_values[feature] == right_values[feature] else "different"','return "different" if left_values[feature] == right_values[feature] else "equal"'),
 ('lose_provenance','return Observation(object_name, tuple((f, actual[f]) for f in features), provenance)','return Observation(object_name, tuple((f, actual[f]) for f in features), "current")'),
 ('ignore_selection','indices = tuple(catalog.features.index(f) for f in features)','indices = tuple(range(len(catalog.features)))'),
 ('invent_all_witnesses','if all(actual[catalog.features.index(f)] == v for f, v in attributes)','if True'),
 ('erase_all_witnesses','if all(actual[catalog.features.index(f)] == v for f, v in attributes)','if False'),
 ('disjunctive_rule','all(p in known for p in rule.premises)','any(p in known for p in rule.premises)'),
 ('one_scan_only','changed = True\n    return tuple(steps)','changed = False\n    return tuple(steps)'),
 ('unchecked_dependencies','if not set(rule.premises).issubset(known):','if False:'),
 ('unchecked_rule_head','if rule is None or rule.conclusion != step.atom:','if rule is None:'),
 ('forged_initial_fact','if step.atom not in theory.facts:','if False:'),
 ('backward_semantics','if antecedent and not valuation[rule.conclusion]:','if valuation[rule.conclusion] and not antecedent:'),
 ('reverse_inclusion_conclusion','conclusion = a.issubset(c)','conclusion = c.issubset(a)'),
)
source=MODEL.read_text()
for name,before,after in MUTATIONS:
    if source.count(before)!=1: raise RuntimeError(f'nonunique mutation site: {name}')

def run_one(item):
    name,before,after=item
    with tempfile.TemporaryDirectory(prefix='mutation-',dir=ROOT) as dirname:
        target=Path(dirname)/'model.py'
        target.write_text(source.replace(before,after))
        run=subprocess.run([sys.executable,*FLAGS,str(ROOT/'review_model.py'),str(target)],capture_output=True,text=True,timeout=120)
        lines=run.stderr.splitlines()
        last=lines[-1] if lines else ''
        killed=run.returncode==1 and last.startswith('AuditFailure: ')
        return {'name':name,'exit_code':run.returncode,'killed_by_independent_semantic_check':killed,'failure':last}

# Establish the unchanged baseline using the same independent script first.
base=subprocess.run([sys.executable,*FLAGS,str(ROOT/'review_model.py')],capture_output=True,text=True,timeout=120)
if base.returncode: raise RuntimeError('independent baseline failed')
baseline=json.loads(base.stdout)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results=list(pool.map(run_one,MUTATIONS))
if hashlib.sha256(MODEL.read_bytes()).hexdigest()!=baseline['source_sha256']:
    raise RuntimeError('production code changed during mutation audit')
report={'baseline':'PASS','source_sha256':baseline['source_sha256'],'review_script_sha256':baseline['review_script_sha256'],
        'mutation_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'optimization':sys.flags.optimize,'results':results,'killed':sum(r['killed_by_independent_semantic_check'] for r in results),'total':len(results),
        'scope':'Specific semantic errors only. Crashes, syntax/import errors, timeouts and unknown failures are not successes.'}
print(json.dumps(report,ensure_ascii=False,indent=2))
if report['killed']!=report['total']: raise SystemExit(1)
