"""Independent audit: 7 relevant membership cells, outside object implicit.
No imports from or reads of the reproduction program.
"""
from itertools import product
from pathlib import Path
import csv,json
ROOT=Path(__file__).resolve().parent
kinds='AEIO'
# Bit assignments: P=4, Q=2, M=1. Each integer 1..7 is an occupied cell.
models=[frozenset(x for x in range(1,8) if mask&(1<<(x-1))) for mask in range(128)]
models.sort(key=lambda s:(len(s), sorted(s)))
bits={'P':4,'Q':2,'M':1}
fig={1:(('M','Q'),('P','M')),2:(('Q','M'),('P','M')),3:(('M','Q'),('M','P')),4:(('Q','M'),('M','P'))}
listed={1:['AAA','AII','EAE','EIO'],2:['AEE','AOO','EAE','EIO'],3:['AAI','IAI','AII','EAO','EIO','OAO'],4:['AAI','IAI','AEE','EAO','EIO']}
def term(s,t):return frozenset(x for x in s if x&bits[t])
def h(s,k,x,y):
 a,b=term(s,x),term(s,y)
 if k=='A':return a<=b
 if k=='E':return not a&b
 if k=='I':return bool(a&b)
 return bool(a-b)
def encode(s):
 if s is None:return None
 return {'U':sorted(s) or [0],**{t:sorted(term(s,t)) for t in bits}}
rows=[]
for f in range(1,5):
 for a,b,c in product(kinds,repeat=3):
  premise=lambda s:h(s,a,*fig[f][0]) and h(s,b,*fig[f][1])
  counters=[s for s in models if premise(s) and not h(s,c,'P','Q')]
  nonempty=[s for s in counters if all(term(s,t) for t in bits)]
  ms=''.join((a,b,c))
  rows.append({'figure':f,'mood':ms,'source_listed':ms in listed[f],'valid_empty_allowed':not counters,'valid_all_terms_nonempty':not nonempty,'counter_empty_allowed':encode(counters[0] if counters else None),'counter_all_terms_nonempty':encode(nonempty[0] if nonempty else None)})
assert len(rows)==256
assert sum(r['valid_empty_allowed'] for r in rows)==15
assert sum(r['valid_all_terms_nonempty'] for r in rows)==24
assert sum(r['source_listed'] for r in rows)==19
assert all(len(r['counter_all_terms_nonempty']['U'])<=3 for r in rows if not r['valid_all_terms_nonempty'])
assert all(len(r['counter_empty_allowed']['U'])<=3 for r in rows if not r['valid_empty_allowed'])
# The public CSV keeps only the essential independent 256-form classification.
fields=('figure','mood','source_listed','valid_empty_allowed','valid_all_terms_nonempty')
with (ROOT/'classification256.csv').open('w',newline='') as out:
 w=csv.DictWriter(out,fieldnames=fields);w.writeheader()
 for r in rows:w.writerow({k:r[k] for k in fields})
all_valid={(r['figure'],r['mood']) for r in rows if r['valid_all_terms_nonempty']}
source={(r['figure'],r['mood']) for r in rows if r['source_listed']}
maximal={(f,m) for f,m in all_valid if not (m[-1]=='I' and (f,m[:2]+'A') in all_valid) and not (m[-1]=='O' and (f,m[:2]+'E') in all_valid)}
assert maximal==source
q_m_valid=set()
for f in range(1,5):
 for a,b,c in product(kinds,repeat=3):
  if all(not(h(s,a,*fig[f][0]) and h(s,b,*fig[f][1])) or h(s,c,'P','Q') for s in models if term(s,'Q') and term(s,'M')):
   q_m_valid.add((f,a+b+c))
assert q_m_valid==source
assert sum(all(term(s,t) for t in bits) for s in models)==109
for f in range(1,5):
 for a,b in product(kinds,repeat=2):
  assert any(all(term(s,t) for t in bits) and h(s,a,*fig[f][0]) and h(s,b,*fig[f][1]) for s in models)
print('PASS: 128 representatives; 109 have all terms nonempty.')
print('PASS: 256 forms; 15 valid with empty terms allowed; 24 valid with all terms nonempty.')
print('PASS: The 19 nonweakened forms and the 19 Q/M-nonempty forms both equal the source list.')
print('PASS: All invalid forms have explicit countermodels of at most 3 objects.')
print('PASS: All 64 premise pairs are satisfiable with all terms nonempty.')
report=ROOT.parents[1]/'reproduction/euler-1768-cvi/results/report.json'
if report.exists():
 other={r['id']:r for r in json.loads(report.read_text())['all_256_forms']}
 for r in rows:
  k=f"{r['figure']}-{r['mood']}";v=other[k]
  assert r['source_listed']==v['listed_by_euler'],k
  assert r['valid_empty_allowed']==v['no_term_existence']['valid'],k
  assert r['valid_all_terms_nonempty']==v['all_terms_nonempty']['valid'],k
 print('PASS: All 512 validity decisions and 256 source-list flags agree with the independent main reproduction.')
