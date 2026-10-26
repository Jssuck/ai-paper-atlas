"""Regenerate finite results. Nonzero exit on explicit consistency failures."""
import json
from pathlib import Path
from model import enumerate_models, examples
r = enumerate_models()
if r['oracle_mismatches'] or r['elimination_violations']:
    raise RuntimeError('finite consistency check failed')
data={'enumeration':r,'examples':examples(), 'scope':'Finite extensional teaching model; not essence or scientific knowledge.'}
text=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
Path('logs').mkdir(exist_ok=True)
Path('logs/results.json').write_text(text,encoding='utf-8')
print(text,end='')
