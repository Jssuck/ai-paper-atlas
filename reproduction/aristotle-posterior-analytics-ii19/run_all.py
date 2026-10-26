"""Run actual examples, tests and notebook without third-party dependencies."""
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path
from model import analyse, compatible_explanations, group_memories
from oracle import verify

root=Path(__file__).resolve().parent
logs=root/'logs'; logs.mkdir(exist_ok=True)
examples={
 'no_observation':analyse(list('abc'), []),
 'hundred_repeats':analyse(list('abc'), [('a',True)]*100),
 'two_distinct_positive':analyse(list('abc'), [('a',True),('b',True)]),
 'finite_domain_covered':analyse(list('abc'), [('a',True),('b',True),('c',True)]),
 'counterexample':analyse(list('abc'), [('a',True),('b',False)]),
 'empty_domain':analyse([], []),
 'opposite_completions':compatible_explanations(['a','b'], [('a',True)]),
 'given_class_groups':group_memories(list('abc'), [('a',True),('a',True),('b',True)],{'a':'X','b':'X','c':'Y'})
}
report={'scope':'Modern finite-domain teaching model; no nous, probability, or historical psychology validation.','examples':examples,'oracle':verify()}
(root/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(logs/'demo.log').write_text('Command: python3 run_all.py\n'+json.dumps(report,ensure_ascii=False,indent=2)+'\n')
commands=[]
for option,name in [([], 'tests-normal.log'),(['-O'],'tests-O.log'),(['-OO'],'tests-OO.log')]:
    args=option+['-m','unittest','-v','test_model']
    p=subprocess.run([sys.executable]+args,cwd=root,text=True,capture_output=True)
    command='python3 '+' '.join(args)
    (logs/name).write_text('Command: '+command+'\n'+p.stdout+p.stderr+'Exit code: '+str(p.returncode)+'\n')
    commands.append({'command':command,'exit_code':p.returncode})
    if p.returncode: raise RuntimeError('test run failed')
p=subprocess.run([sys.executable,'run_notebook.py'],cwd=root,text=True,capture_output=True)
(logs/'notebook-exec.log').write_text('Command: python3 run_notebook.py\n'+p.stdout+p.stderr+'Exit code: '+str(p.returncode)+'\n')
commands.append({'command':'python3 run_notebook.py','exit_code':p.returncode})
if p.returncode: raise RuntimeError('notebook execution failed')
(logs/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
(root/'environment.json').write_text(json.dumps({'python':platform.python_version(),'implementation':platform.python_implementation(),'system':platform.system(),'machine':platform.machine(),'dependencies':'standard library only','notebook_execution':'sequential exec in a new Python process; not a Jupyter kernel'},indent=2)+'\n')
checks={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='sha256.json'}
(root/'sha256.json').write_text(json.dumps(checks,indent=2)+'\n')
print(json.dumps({'tests_per_mode':24,'modes':['normal','-O','-OO'],'notebook_cells':5,'oracle':report['oracle']},ensure_ascii=False))
