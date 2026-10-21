"""Independent finite checks of the article's arguments, not its implementation.
No import from production model; sets and explicit quantifiers are used.
Finite checks supplement, and do not replace, the article's general proofs.
"""
import itertools
import json

D = (0, 1)
SUBSETS = tuple(frozenset(x for x in D if mask & (1 << x)) for mask in range(4))
MOODS = (
 ('Barbara', ('A','M','P'),('A','S','M'),('A','S','P'),False),
 ('Celarent',('E','M','P'),('A','S','M'),('E','S','P'),False),
 ('Darii',('A','M','P'),('I','S','M'),('I','S','P'),False),
 ('Ferio',('E','M','P'),('I','S','M'),('O','S','P'),False),
 ('Cesare',('E','P','M'),('A','S','M'),('E','S','P'),False),
 ('Camestres',('A','P','M'),('E','S','M'),('E','S','P'),False),
 ('Festino',('E','P','M'),('I','S','M'),('O','S','P'),False),
 ('Baroco',('A','P','M'),('O','S','M'),('O','S','P'),False),
 ('Darapti',('A','M','P'),('A','M','S'),('I','S','P'),True),
 ('Disamis',('I','M','P'),('A','M','S'),('I','S','P'),False),
 ('Datisi',('A','M','P'),('I','M','S'),('I','S','P'),False),
 ('Felapton',('E','M','P'),('A','M','S'),('O','S','P'),True),
 ('Bocardo',('O','M','P'),('A','M','S'),('O','S','P'),False),
 ('Ferison',('E','M','P'),('I','M','S'),('O','S','P'),False),
)
checks = 0
def require(condition, label):
 global checks
 checks += 1
 if not condition:
  raise RuntimeError(label)

def q(world, proposition):
 kind, sub, pred = proposition
 s, p = world[sub], world[pred]
 if kind == 'A': return all(x in p for x in s)
 if kind == 'E': return all(x not in p for x in s)
 if kind == 'I': return any(x in p for x in s)
 if kind == 'O': return any(x not in p for x in s)
 raise ValueError('unknown form')

def n(model, prop): return all(q(w, prop) for w in model)
def r(model, kind, sub, pred):
 return any(all(x in w[sub] and ((x in w[pred]) if kind == 'I' else (x not in w[pred])) for w in model) for x in D)
def world(s,m,p): return {'S':frozenset(s),'M':frozenset(m),'P':frozenset(p)}

worlds = tuple(dict(zip(('S','M','P'), row)) for row in itertools.product(SUBSETS, repeat=3))
statistics = {name:{'premise_models':0,'unrestricted_countermodels':0} for name,*_ in MOODS}
for model in itertools.product(worlds, repeat=2):
 for name,p1,p2,c,needs_nonempty in MOODS:
  premises = n(model,p1) and n(model,p2)
  conclusion = n(model,c)
  if premises:
   statistics[name]['premise_models'] += 1
   if not conclusion: statistics[name]['unrestricted_countermodels'] += 1
  eligible = (not needs_nonempty) or all(w['M'] for w in model)
  require(not (eligible and premises) or conclusion, name)
 for sub,pred in (('S','P'),('S','M'),('M','P')):
  require(not r(model,'I',sub,pred) or n(model,('I',sub,pred)), 'RI implies NI')
  require(not r(model,'O',sub,pred) or n(model,('O',sub,pred)), 'RO implies NO')
 require(not (r(model,'O','S','M') and n(model,('A','P','M'))) or r(model,'O','S','P'), 'rigid Baroco')
 require(not (r(model,'O','M','P') and n(model,('A','M','S'))) or r(model,'O','S','P'), 'rigid Bocardo')
 for w in model:
  for sub,pred in (('S','P'),('S','M'),('M','P')):
   require(q(w,('A',sub,pred)) != q(w,('O',sub,pred)), 'A/O contradictory')
   require(q(w,('E',sub,pred)) != q(w,('I',sub,pred)), 'E/I contradictory')
   require(q(w,('E',sub,pred)) == q(w,('E',pred,sub)), 'E conversion')

# Direct article examples, independent of the exhaustive implication loop.
switch_i = (world({0},set(),{0}),world({1},set(),{1}))
require(n(switch_i,('I','S','P')) and not r(switch_i,'I','S','P'),'switching I witness')
switch_o = (world({0},set(),set()),world({1},set(),set()))
require(n(switch_o,('O','S','P')) and not r(switch_o,'O','S','P'),'switching O witness')
empty = (world(set(),set(),set()),)*2
require(n(empty,('A','M','P')) and n(empty,('A','M','S')) and not n(empty,('I','S','P')),'empty Darapti')
require(n(empty,('E','M','P')) and n(empty,('A','M','S')) and not n(empty,('O','S','P')),'empty Felapton')
baroco = (world({0,1},{0},{0}),)*2
require(n(baroco,('A','P','M')) and n(baroco,('O','S','M')) and r(baroco,'O','S','P'),'Baroco example')
require(q(baroco[0],('O','S','M')) and not q(baroco[0],('O','M','S')),'O converse failure')
bocardo = (world({0},{0},set()),world({1},{1},set()))
require(n(bocardo,('O','M','P')) and n(bocardo,('A','M','S')) and n(bocardo,('O','S','P')) and not r(bocardo,'O','S','P'),'Bocardo unstable witness')
actual = (world({0},{0},{0}),world({0},{0},set()))
require(q(actual[0],('A','M','P')) and q(actual[0],('A','S','M')) and not n(actual,('A','S','P')),'actual not necessary')
possible = (world({0},{0},set()),world(set(),{0},{0}))
require(any(q(w,('A','M','P')) for w in possible) and any(q(w,('I','S','M')) for w in possible) and not any(q(w,('I','S','P')) for w in possible),'separate possibility')
require(not any(q(w,('A','M','P')) and q(w,('I','S','M')) for w in possible),'no joint possible premises')
mixed = (world({0},{0},{0}),world({0},set(),set()))
require(n(mixed,('A','M','P')) and q(mixed[0],('A','S','M')) and not n(mixed,('A','S','P')),'mixed necessary major')
require({name for name,s in statistics.items() if s['unrestricted_countermodels']} == {'Darapti','Felapton'},'only two empty-policy failures')
print(json.dumps({'status':'PASS','domain_size':2,'world_count':2,'models':4096,'checks':checks,'moods':statistics,'scope':'Finite verification only; no production-code import, no historical semantics uniqueness claim.'},ensure_ascii=False,indent=2))
