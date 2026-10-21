"""Independent set-based checks; imports no authored reduction implementation."""
from itertools import product, combinations
from pathlib import Path
import json, sys
BASE=Path(__file__).resolve().parents[1]
checks=0

def require(ok, label):
    global checks
    checks+=1
    if not ok: raise RuntimeError(label)

def val(q,x,y):
    if q=='A': return x<=y
    if q=='E': return x.isdisjoint(y)
    if q=='I': return bool(x&y)
    if q=='O': return bool(x-y)
    raise ValueError(q)

def powerset(xs):
    return [frozenset(c) for n in range(len(xs)+1) for c in combinations(xs,n)]

# A new tuple representation rather than the authored integer-bit oracle.
types=list(product([False,True],repeat=3))
supports=[]
for ss in powerset(types):
    if not ss: continue
    sets=tuple(frozenset(t for t in ss if t[k]) for k in range(3))
    supports.append(sets) # P,S,M
require(len(supports)==255,'support count')
require(sum(all(s) for s in supports)==218,'nonempty count')
rows=json.loads((BASE/'classification.json').read_text())
valid=0; invalid=0
for row in rows:
    fig=row['figure']; q=row['major']; r=row['minor']
    universe=[s for s in supports if row['policy']=='allow-empty' or all(s)]
    for direction in ['forward','reverse']:
      for conclusion in 'AEIO':
        bad=[]
        for P,S,M in universe:
          pair={1:((M,P),(S,M)),2:((P,M),(S,M)),3:((M,P),(M,S))}[fig]
          x,y=(S,P) if direction=='forward' else (P,S)
          if val(q,*pair[0]) and val(r,*pair[1]) and not val(conclusion,x,y): bad.append((P,S,M))
        truth=not bad
        require(truth==(conclusion in row[direction]),f'classification {row["policy"]}/{fig}/{q}{r}/{direction}/{conclusion}')
        valid+=truth; invalid+=not truth
require((valid,invalid)==(59,709),'reported count')

modes=[(1,'AAA','Barbara'),(1,'EAE','Celarent'),(1,'AII','Darii'),(1,'EIO','Ferio'),(2,'EAE','Cesare'),(2,'AEE','Camestres'),(2,'EIO','Festino'),(2,'AOO','Baroco'),(3,'AAI','Darapti'),(3,'EAO','Felapton'),(3,'IAI','Disamis'),(3,'AII','Datisi'),(3,'OAO','Bocardo'),(3,'EIO','Ferison')]
for fig,mode,name in modes:
    for P,S,M in supports:
        pair={1:((M,P),(S,M)),2:((P,M),(S,M)),3:((M,P),(M,S))}[fig]
        antecedent=val(mode[0],*pair[0]) and val(mode[1],*pair[1])
        if name in ('Darapti','Felapton'): antecedent=antecedent and bool(M)
        require(not antecedent or val(mode[2],S,P),'named proof '+name)

# Every local line in the two central reductions is checked under its assumptions.
for A,B,C in product(powerset([0,1,2]),repeat=3):
    require(val('A',B,A)==(not val('O',B,A)),'A/O')
    require(val('E',B,A)==(not val('I',B,A)),'E/I')
    require(val('E',B,A)==val('E',A,B),'E conversion')
    require(val('I',B,A)==val('I',A,B),'I conversion')
    require(not(val('A',B,A) and val('A',C,B)) or val('A',C,A),'Barbara')
    require(not(val('E',B,A) and val('A',C,B)) or val('E',C,A),'Celarent')
    # Darii assumes E(C,A), then converts and composes before using I(C,B).
    if val('A',B,A) and val('E',C,A):
        require(val('E',A,C),'Darii line2')
        require(val('E',B,C),'Darii line3')
        require(val('E',C,B),'Darii line4')
        require(not val('I',C,B),'Darii clash')
    if val('E',B,A) and val('A',C,A):
        require(val('E',A,B),'Ferio line2')
        require(val('E',C,B),'Ferio line3')
        require(not val('I',C,B),'Ferio clash')
    require(not(val('I',B,A) and val('E',C,B)) or val('O',A,C),'reverse I/E')
    require(not(val('A',B,A) and val('E',C,B) and B) or val('O',A,C),'reverse A/E with B')
    require(not(val('A',C,A) and val('A',C,B) and C) or val('I',B,A),'Darapti C-only existence')
# Displayed counterexamples and logical non-equivalences.
u=frozenset([0]); empty=frozenset()
require(val('A',empty,u) and not val('I',u,empty),'A conversion failure')
require(val('O',frozenset([0,1]),u) and not val('O',u,frozenset([0,1])),'O conversion failure')
require(val('A',empty,u) and val('E',u,empty) and not val('O',u,u),'reverse empty-B failure')
require(val('A',empty,u) and val('A',empty,u) and not val('I',empty,u),'empty universal conflict reminder')
require(val('A',empty,u) and val('E',empty,u),'A/E compatibility')
require(val('I',frozenset([0,1]),u) and val('O',frozenset([0,1]),u),'I/O compatibility')
report={'status':'PASS','checks':checks,'classification_comparisons':768,'valid_conclusions':valid,'invalid_conclusions':invalid,'named_mode_support_checks':14*255,'local_universe_size':3,'imports_author_implementation':False,'optimization':sys.flags.optimize,'scope':'Finite verification supports the separately stated general proofs; not a proof of unrestricted logic.'}
print(json.dumps(report,ensure_ascii=False,indent=2))
