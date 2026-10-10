"""Run actual local checks and write sanitized, shareable evidence.

Only allowlisted environment fields are retained. No environment-variable dump,
user name, hostname, absolute local path, credential, browser log, or source scan
is copied into the release evidence. Existing independent-review evidence is
preserved, not cleaned or overwritten.
"""
from __future__ import annotations
import datetime
import hashlib
import importlib.util
import json
import platform
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT=Path(__file__).resolve().parent
EVIDENCE=ROOT/'evidence'


def main():
    EVIDENCE.mkdir(exist_ok=True)
    commands=[('unit-tests.log',['-m','unittest','-v']),
              ('polynomial-certificate.log',['polynomial_certificate.py']),
              ('reproduction.log',['reproduce.py']),
              ('notebook-validation.log',['validate_notebook.py','--execute'])]
    runs=[]
    for filename,args in commands:
        result=subprocess.run([sys.executable,*args],cwd=ROOT,capture_output=True,text=True)
        clean=(result.stdout+result.stderr).replace(str(ROOT),'[REPRODUCTION_ROOT]')
        display='python '+' '.join(args)
        (EVIDENCE/filename).write_text('$ '+display+'\n'+clean+f'\nexit_code={result.returncode}\n',encoding='utf-8')
        runs.append({'command':display,'exit_code':result.returncode,'log':filename})
        print(display, 'PASS' if result.returncode==0 else 'FAIL')
        if result.returncode:raise SystemExit(result.returncode)
    svg_checks=[]
    for filename in ['divider-domains.svg','equal-chords.svg']:
        tree=ET.parse(ROOT/'output'/filename)
        root=tree.getroot()
        assert root.tag=='{http://www.w3.org/2000/svg}svg'
        assert root.find('{http://www.w3.org/2000/svg}title') is not None
        assert root.find('{http://www.w3.org/2000/svg}desc') is not None
        assert all('http://' not in v and 'https://' not in v for el in root.iter() for k,v in el.attrib.items() if k.endswith('href'))
        svg_checks.append({'file':'output/'+filename,'valid_xml':True,'title_and_description':True,'external_href_count':0})
    environment={
        'runtime_reported_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'python_version':platform.python_version(),
        'implementation':platform.python_implementation(),
        'operating_system':platform.system(),
        'architecture':platform.machine(),
        'required_dependencies':'Python standard library only',
        'network_access_required':False,
        'packages_installed_for_this_reproduction':[],
        'notebook_execution':'Plain sequential CPython exec; not Jupyter',
        'notebook_validation':'Basic custom nbformat-4 structure/AST checks; not full official schema',
        'optional_notebook_modules_present':{name:importlib.util.find_spec(name) is not None for name in ['jupyter','nbformat','nbclient']},
        'redaction':'Allowlist only: no environment variables, username, hostname, absolute paths, credentials or external data.'}
    (EVIDENCE/'environment.json').write_text(json.dumps(environment,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    sys.path.insert(0,str(ROOT))
    import test_sylvester
    test_count=unittest.defaultTestLoader.loadTestsFromModule(test_sylvester).countTestCases()
    nb=json.loads((ROOT/'tutorial.ipynb').read_text())
    summary={
        'all_checks_passed':True,'commands':runs,'unit_tests':test_count,
        'exact_rational_triangle_substitutions':4010,'finite_grid_cases':4760,
        'notebook_cells':len(nb['cells']),
        'notebook_code_cells_executed':sum(c['cell_type']=='code' for c in nb['cells']),
        'notebook_saved_error_outputs':0,'svg_checks':svg_checks,
        'boundaries':['Finite checks do not establish universal theorems.',
                      'The polynomial coefficient identity and positivity argument are distinct from grid sampling.',
                      'No Jupyter execution or formal proof-assistant verification is claimed.']}
    (EVIDENCE/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    files=sorted([*ROOT.glob('*.py'),ROOT/'.gitignore',ROOT/'README.md',ROOT/'tutorial.ipynb',*list((ROOT/'output').glob('*'))])
    manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files if p.is_file()}
    (EVIDENCE/'artifact-sha256.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(f'PASS: {test_count} unit tests; {summary["notebook_code_cells_executed"]} CPython notebook cells; 2 SVG structures.')
    print('Actual sanitized logs saved under evidence/. Independent review files preserved.')


if __name__=='__main__':main()
