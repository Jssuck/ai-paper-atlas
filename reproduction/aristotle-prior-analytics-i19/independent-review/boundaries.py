"""Independent metamorphic boundaries not limited to contiguous positive IDs."""
import itertools,json,pathlib,sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from modal_model import Model
rows=[{'A':{0},'B':{0,1},'C':{1}},{'A':{1},'B':{1},'C':set()}]
base=Model([0,1],rows,1)
renamed=Model([-7,99],[{t:{(-7,99)[x] for x in xs} for t,xs in w.items()} for w in rows],1)
permuted=Model([0,1],rows[::-1],0)
doubled=Model([0,1],rows*2,3)
checks=0
for q in itertools.product(('D','N','C','P','Box'),'aeio','ABC','ABC'):
    expected=base.eval(*q)
    for other in (renamed,permuted,doubled):
        if other.eval(*q)!=expected:raise RuntimeError('metamorphic failure '+str(q))
        checks+=1
# Input tuples, duplicate IDs, detached serialization and frozen extensions.
m=Model((0,0),({'A':(0,0),'B':[0,0],'C':frozenset()},))
copy=m.as_dict();copy['worlds'][0]['A'].clear();copy['domain'].clear()
if not m.eval('D','a','A','B'):raise RuntimeError('serialization mutation leaked')
if m.domain!=frozenset({0}):raise RuntimeError('duplicate normalization failed')
try:m.worlds[0]['A'].add(1)
except AttributeError:pass
else:raise RuntimeError('extension mutable')
print(json.dumps({'optimization':sys.flags.optimize,'metamorphic_comparisons':checks,'boundaries':['negative and nonconsecutive IDs','world permutation with designated index mapped','world duplication','tuple/frozenset/list accepted','duplicate IDs normalized','as_dict detached','extension frozen'],'result':'PASS'},indent=2))
