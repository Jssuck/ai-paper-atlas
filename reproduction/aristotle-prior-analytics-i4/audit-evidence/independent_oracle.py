#!/usr/bin/env python3
"""Independent auditor: explicit named Venn regions and cardinality semantics.
No author code is used to construct the expected model space or expected truth.
Run: python independent_oracle.py /path/to/reproduction
"""
import csv
import hashlib
import importlib.util
import io
import itertools
import json
import pathlib
import subprocess
import sys
from collections import Counter

ROOT = pathlib.Path(sys.argv[1]).resolve()
KINDS = ('A', 'E', 'I', 'O')
MODES = ('empty-allowed', 'all-nonempty')
REGIONS = tuple(frozenset(x) for x in ('', 'S', 'M', 'MS', 'P', 'PS', 'PM', 'PMS'))
ROUTES = {'AA':'A', 'EA':'E', 'AI':'I', 'EI':'O'}
CHECKS = Counter()

def require(condition, message):
    if not condition:
        raise RuntimeError(message)
    CHECKS['assertions'] += 1

def extensions(support):
    return {term: frozenset(i for i in support if term in REGIONS[i]) for term in 'PMS'}

def truth(ext, kind, subject, predicate):
    # Count shared witnesses; do not use the production subset/difference tests
    # or the author's per-point logical-implication oracle.
    left = ext[subject]
    shared = sum(1 for x in left if x in ext[predicate])
    return {'A': shared == len(left), 'E': shared == 0,
            'I': shared > 0, 'O': shared < len(left)}[kind]

def premises(ext, pair):
    return truth(ext, pair[0], 'M', 'P') and truth(ext, pair[1], 'S', 'M')

def dictionary(support):
    return {'support': list(support), 'type_bits_PMS': [''.join('1' if t in REGIONS[i] else '0' for t in 'PMS') for i in support],
            'cardinality':len(support), 'mask':sum(2 ** i for i in support), 'U':list(support),
            **{term:sorted(ext) for term, ext in extensions(support).items()}}

# Enumerate all subsets using 8 independent yes/no choices, then sort; this is
# independent of the author's combinations(), models(), masks and admission.
SUPPORTS = sorted((tuple(i for i, occupied in enumerate(selection) if occupied)
                   for selection in itertools.product((False, True), repeat=8) if any(selection)),
                  key=lambda s:(len(s),s))
SPACES = {MODES[0]: SUPPORTS,
          MODES[1]: [s for s in SUPPORTS if all(extensions(s).values())]}
require(len(SPACES[MODES[0]]) == 255, 'independent 255 count')
# Inclusion-exclusion: exclude supports missing each of three terms.
require(255 - 3*15 + 3*3 - 1 == len(SPACES[MODES[1]]) == 218, 'independent 218 count')

# Only now load implementation as a black-box comparison target.
sys.path.insert(0, str(ROOT))
import categorical as implementation
report = json.loads((ROOT/'results/report.json').read_text(encoding='utf-8'))
expected_forms = {}
summary = {'model_counts':{m:len(SPACES[m]) for m in MODES}, 'valid_forms':{}, 'valid_reverse_forms':{},
           'minimum_countermodel_cardinalities':{}, 'premise_counts':{}, 'witnesses':{},
           'independent_oracle':'explicit named Venn regions; cardinality of shared witnesses'}
for support in SUPPORTS:
    ext = extensions(support)
    model = implementation.Model(support)
    require(model.as_dict() == dictionary(support), f'serialized model {support}')
    for kind, subject, predicate in itertools.product(KINDS, 'PMS', 'PMS'):
        require(model.holds(kind,subject,predicate) == truth(ext,kind,subject,predicate), f'atomic {support} {kind} {subject} {predicate}')
        CHECKS['atomic_truths'] += 1

for mode in MODES:
    space = SPACES[mode]
    require([m.support for m in implementation.models(mode)] == space, 'enumeration '+mode)
    require(report['model_counts'][mode] == len(space), 'report count '+mode)
    summary['premise_counts'][mode] = {}
    for pair in itertools.product(KINDS, repeat=2):
        pair = ''.join(pair)
        count = sum(premises(extensions(s), pair) for s in space)
        require(count > 0, 'nonvacuous premises '+mode+pair)
        summary['premise_counts'][mode][pair] = count
    for reverse in (False, True):
        subject, predicate = ('P','S') if reverse else ('S','P')
        direction = 'P->S' if reverse else 'S->P'
        expected = []
        distribution = Counter()
        for form in itertools.product(KINDS, repeat=3):
            form = ''.join(form)
            failures = [s for s in space if premises(extensions(s), form[:2]) and not truth(extensions(s),form[2],subject,predicate)]
            countermodel = failures[0] if failures else None
            row = {'form':form,'mode':mode,'direction':direction,'valid':not failures,
                   'premise_model_count':summary['premise_counts'][mode][form[:2]],
                   'minimal_countermodel':None if countermodel is None else dictionary(countermodel)}
            expected.append(row)
            actual = implementation.analyze_form(*form, mode=mode, reverse=reverse)
            require(actual.as_dict() == row, 'API form '+mode+direction+form)
            CHECKS['form_results'] += 1
            if countermodel is not None:
                distribution[str(len(countermodel))] += 1
                CHECKS['minimum_countermodels'] += 1
        expected_forms[mode,reverse] = expected
        require(report['reverse_forms' if reverse else 'forms'][mode] == expected, 'full report form list '+mode+direction)
        require([x.as_dict() for x in implementation.all_forms(mode=mode,reverse=reverse)] == expected, 'all_forms '+mode+direction)
        key = 'valid_reverse_forms' if reverse else 'valid_forms'
        valid = [r['form'] for r in expected if r['valid']]
        require(report[key][mode] == valid, 'report valid forms '+mode+direction)
        summary[key][mode] = valid
        summary['minimum_countermodel_cardinalities'][mode+' '+direction] = dict(sorted(distribution.items()))

# Verify all 48 A/E witness records, including minimum cardinality and ties.
expected_pairs = [''.join(p) for p in itertools.product(KINDS,repeat=2) if ''.join(p) not in ROUTES]
for mode in MODES:
    rows = []
    for pair in expected_pairs:
        row = {'pair':pair,'mode':mode}
        for kind in ('A','E'):
            choices = [s for s in SPACES[mode] if extensions(s)['S'] and premises(extensions(s), pair) and truth(extensions(s),kind,'S','P')]
            require(bool(choices), 'witness exists '+mode+pair+kind)
            row[kind+'_SP_witness'] = dictionary(choices[0])
            e = extensions(choices[0])
            incompatible = ('E','O') if kind == 'A' else ('A','I')
            require(all(not truth(e,k,'S','P') for k in incompatible), 'witness rejects '+mode+pair+kind)
            CHECKS['nonvacuous_witnesses'] += 1
        rows.append(row)
    require(report['nonproductive_witnesses'][mode] == rows, 'complete witness report '+mode)
    require(implementation.nonproductive_witnesses(mode=mode) == rows, 'witness API '+mode)
    summary['witnesses'][mode] = rows

# Independent labeled universes, P/M/S selected as three arbitrary subsets.
# This bypasses the implementation's type enumeration for minimum-size checks.
labeled_first_failure = {}
for n in range(1,4):
    U = tuple(range(n))
    subsets = [frozenset(U[i] for i,present in enumerate(bits) if present)
               for bits in itertools.product((False,True),repeat=n)]
    for P,M,S in itertools.product(subsets,repeat=3):
        ext = {'P':P,'M':M,'S':S}
        encoded = tuple(REGIONS.index(frozenset(t for t in 'PMS' if i in ext[t])) for i in U)
        support = tuple(sorted(set(encoded)))
        for k,x,y in itertools.product(KINDS,'PMS','PMS'):
            require(truth(ext,k,x,y) == truth(extensions(support),k,x,y),'labeled compression')
            CHECKS['labeled_atomic_compressions'] += 1
        for mode in MODES:
            if mode == 'all-nonempty' and not all(ext.values()):
                continue
            for reverse in (False,True):
                x,y = ('P','S') if reverse else ('S','P')
                for form in itertools.product(KINDS,repeat=3):
                    form=''.join(form)
                    if premises(ext,form[:2]) and not truth(ext,form[2],x,y):
                        labeled_first_failure.setdefault((mode,reverse,form),n)
        CHECKS['labeled_models'] += 1
for (mode,reverse),rows in expected_forms.items():
    for row in rows:
        observed = labeled_first_failure.get((mode,reverse,row['form']))
        require(observed == (None if row['valid'] else row['minimal_countermodel']['cardinality']), 'independent labeled minimum '+mode+row['form'])

expected_table=[]
for pair in itertools.product(KINDS,repeat=2):
    pair=''.join(pair)
    row={'pair':pair,'original_strongest':ROUTES.get(pair,'')}
    for mode in MODES:
        for reverse in (False,True):
            row[mode+('_reverse' if reverse else '_forward')]=''.join(r['form'][2] for r in expected_forms[mode,reverse] if r['form'][:2]==pair and r['valid'])
    expected_table.append(row)
require(report['premise_pair_table']==expected_table,'JSON 16 pair table')
with (ROOT/'results/premise-pairs.csv').open(encoding='utf-8',newline='') as f:
    require(list(csv.DictReader(f))==expected_table,'CSV 16 pair table')
with (ROOT/'results/forms.csv').open(encoding='utf-8',newline='') as f:
    csvrows=list(csv.DictReader(f))
expected_flat=expected_forms[MODES[0],False]+expected_forms[MODES[1],False]
require(len(csvrows)==128,'CSV 128 rows')
for actual,expected in zip(csvrows,expected_flat):
    converted={**actual,'valid':actual['valid']=='True', 'premise_model_count':int(actual['premise_model_count']),
               'minimal_countermodel':json.loads(actual['minimal_countermodel'])}
    require(converted==expected,'CSV exact row '+expected['mode']+expected['form'])
human=(ROOT/'results/walkthrough.txt').read_text(encoding='utf-8')
require('\ufffd' not in human,'Unicode replacement-character check')
for row in expected_table:
    columns=('pair','original_strongest','empty-allowed_forward','all-nonempty_forward','empty-allowed_reverse','all-nonempty_reverse')
    line=' | '.join(row[k] or '无' for k in columns)
    require(line in human.splitlines(),'human column check '+row['pair'])
for row in summary['witnesses']['all-nonempty']:
    line=f"{row['pair']}: A 支撑={row['A_SP_witness']['support']}; E 支撑={row['E_SP_witness']['support']}"
    require(line in human.splitlines(),'human witnesses '+row['pair'])
for fmt,name in [('human','walkthrough.txt'),('json','report.json'),('pairs-csv','premise-pairs.csv'),('forms-csv','forms.csv')]:
    for options in ([],['-O'],['-OO']):
        result=subprocess.run([sys.executable,*options,str(ROOT/'walkthrough.py'),'--format',fmt],capture_output=True,check=True)
        require(result.stdout==(ROOT/'results'/name).read_bytes(),'exact CLI bytes '+fmt+repr(options))
        require(not result.stderr,'CLI stderr '+fmt+repr(options))
        CHECKS['exact_cli_outputs'] += 1
require(subprocess.check_output([sys.executable,str(ROOT/'walkthrough.py')])==(ROOT/'results/walkthrough.txt').read_bytes(),'default CLI')
mutations=json.loads((ROOT/'results/mutations.json').read_text(encoding='utf-8'))
require(mutations['total']==mutations['killed']==len(mutations['records'])==16,'16 mutations')
require(len({r['mutation'] for r in mutations['records']})==16,'16 unique mutations')
for row in mutations['records']:
    out=row['test_output']
    require(row['returncode']==1 and row['killed_by_assertion'] and 'FAIL:' in out and 'AssertionError' in out and 'ERROR:' not in out and 'Ran 1 test' in out,'mutation real assertion '+row['mutation'])
    CHECKS['mutation_assertion_records'] += 1
summary['checks']=dict(CHECKS)
summary['status']='pass'
print(json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True))
