"""Independent set-valued oracle and bounded mutation checks; no general-proof claim."""
import importlib.util, itertools, json, pathlib, sys, types
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import modal_models as m
checks=0

def eq(a,b,label):
    global checks
    checks+=1
    if a != b: raise RuntimeError(label + ': mismatch')

def ext(world,term):
    mask=world[('P','S','M').index(term)]
    return {i for i in range(2) if (mask // (2**i)) % 2}

def val(world,k,s,p):
    a,b=ext(world,s),ext(world,p)
    if k=='A': return a.issubset(b)
    if k=='E': return a.isdisjoint(b)
    if k=='I': return bool(a.intersection(b))
    return bool(a.difference(b))

# Explicit independently transcribed tuples, not imported mood construction.
specs={
'Barbara':(('A','M','P'),('A','S','M'),('A','S','P')),
'Celarent':(('E','M','P'),('A','S','M'),('E','S','P')),
'Darii':(('A','M','P'),('I','S','M'),('I','S','P')),
'Ferio':(('E','M','P'),('I','S','M'),('O','S','P')),
'Cesare':(('E','P','M'),('A','S','M'),('E','S','P')),
'Camestres':(('A','P','M'),('E','S','M'),('E','S','P')),
'Festino':(('E','P','M'),('I','S','M'),('O','S','P')),
'Baroco':(('A','P','M'),('O','S','M'),('O','S','P')),
'Darapti':(('A','M','P'),('A','M','S'),('I','S','P')),
'Disamis':(('I','M','P'),('A','M','S'),('I','S','P')),
'Datisi':(('A','M','P'),('I','M','S'),('I','S','P')),
'Felapton':(('E','M','P'),('A','M','S'),('O','S','P')),
'Bocardo':(('O','M','P'),('A','M','S'),('O','S','P')),
'Ferison':(('E','M','P'),('I','M','S'),('O','S','P'))}
rows={n:dict(premise_models_free=0,failures_free=0,premise_models_middle_nonempty=0,failures_middle_nonempty=0) for n in specs}
gaps={'I':0,'O':0}; local=stable=0
for masks in itertools.product(range(4), repeat=6):
    worlds=(masks[:3],masks[3:]); model=m.Model(2,worlds)
    for s,p,k in itertools.product(('P','S','M'),('P','S','M'),('A','E','I','O')):
        outcomes=[val(w,k,s,p) for w in worlds]
        for wi in range(2): eq(m.categorical(model,wi,k,s,p),outcomes[wi],'categorical')
        eq(m.necessary(model,k,s,p),all(outcomes),'necessary')
        if k in ('I','O'):
            sets=[ext(w,s).intersection(ext(w,p)) if k=='I' else ext(w,s).difference(ext(w,p)) for w in worlds]
            for wi in range(2): eq(m.witnesses(model,wi,k,s,p),tuple(sorted(sets[wi])),'local witnesses')
            rigid=tuple(sorted(set.intersection(*sets)))
            eq(m.rigid_witnesses(model,k,s,p),rigid,'rigid witnesses')
            if (s,p)==('S','P'): gaps[k]+=all(outcomes) and not rigid
    for n,(a,b,c) in specs.items():
        eq(m.propositions(n),(a,b,c),'specification')
        pre=all(val(w,*a) and val(w,*b) for w in worlds)
        con=all(val(w,*c) for w in worlds)
        nonempty=all(ext(w,'M') for w in worlds)
        eq(m.premises(model,n),pre,'premises free')
        eq(m.premises(model,n,True),bool(pre and nonempty),'premises policy')
        eq(m.conclusion(model,n),con,'conclusion')
        if pre:
            rows[n]['premise_models_free']+=1; rows[n]['failures_free']+=not con
            if nonempty:
                rows[n]['premise_models_middle_nonempty']+=1
                rows[n]['failures_middle_nonempty']+=not con
            if n in ('Baroco','Bocardo'):
                xs=m.exposition(model,n); eq(len(xs),2,'exposition length')
                for wi,x in enumerate(xs):
                    eq(x in ext(worlds[wi],'S')-ext(worlds[wi],'P'),True,'exposition destination');local+=1
                part=b if n=='Baroco' else a
                wit=set.intersection(*[ext(w,part[1])-ext(w,part[2]) for w in worlds])
                if wit:
                    stable+=1
                    eq(wit.issubset(set.intersection(*[ext(w,'S')-ext(w,'P') for w in worlds])),True,'stable transfer')
report=m.run_report()
eq(report['models'],4096,'model count')
for n,row in rows.items():
    for field,count in row.items(): eq(report['mood_results'][n][field],count,'report '+n+' '+field)
eq(report['necessary_without_rigid_witness'],gaps,'gap counts')
eq(report['rigid_implies_necessary_failures'],0,'rigid implication')
eq(report['exposition_world_checks'],local,'local count')
eq(report['stable_exposition_model_checks'],stable,'stable count')
for p in [ROOT/'results.json',ROOT/'logs/results-O.json',ROOT/'logs/results-OO.json']:
    eq(json.loads(p.read_text()),report,'saved report')

invalid=[]
for n in [0,-1,True,False,1.5,'2',None]: invalid.append(lambda n=n:m.Model(n,((0,0,0),)))
for worlds in [(),[],None,((0,0),),((0,0,0,0),),([0,0,0],),((0,True,0),),((0,-1,0),),((0,4,0),)]:invalid.append(lambda worlds=worlds:m.Model(2,worlds))
base=m.Model(2,((0,0,0),(3,3,3)))
for bad in [None,True,0,[],{},'', 'bad']:
    invalid.extend([lambda bad=bad:m.necessary(base,bad,'S','P'),lambda bad=bad:m.necessary(base,'A',bad,'P'),lambda bad=bad:m.rigid_witnesses(base,bad,'S','P'),lambda bad=bad:m.propositions(bad),lambda bad=bad:m.exposition(base,bad)])
for w in [-1,2,True,None,'0',0.0]: invalid.append(lambda w=w:m.witnesses(base,w,'I','S','P'))
for bad in [0,1,None,'yes',[]]:invalid.append(lambda bad=bad:m.premises(base,'Barbara',bad))
for bad in [0,4,True,None,2.0]:invalid.append(lambda bad=bad:next(m.two_world_models(bad)))
for f in invalid:
    try:f()
    except ValueError:checks+=1
    else:raise RuntimeError('invalid input accepted')

# Mutations execute isolated module copies in memory; original author files stay unchanged.
source=(ROOT/'modal_models.py').read_text()
mutations=[
('necessary any','return all(categorical','return any(categorical'),
('I false','\'I\': s & p != 0',"'I': s & p == 0"),
('O reversed',"'O': s & ~p != 0","'O': p & ~s != 0"),
('rigid union','common &= s &','common |= s &'),
('rigid empty','common = (1 << model.n) - 1','common = 0'),
('world0 only','for w in range(len(model.worlds)))','for w in range(1))'),
('ignore existence','(existence or not require_middle)','True'),
('wrong conclusion',"(conclusion, 'S', 'P')","(conclusion, 'P', 'S')"),
('wrong figure2',"2: (('P', 'M'), ('S', 'M'))","2: (('M', 'P'), ('S', 'M'))"),
('wrong witness index','i = candidates[0]','i = 0'),
('bool size allowed','type(self.n) is not int','not isinstance(self.n, int)'),
]
def probes(mod):
    def ck(a,b):
        if a!=b:raise RuntimeError('probe caught semantic fault')
    for worlds in [((1,3,0),(2,3,0)),((2,3,1),(1,3,2)),((1,3,0),(1,3,0)),((1,1,1),(0,1,0)),((0,0,0),(0,0,0))]:
        model=mod.Model(2,worlds)
        for s,p,k in itertools.product(('P','S','M'),('P','S','M'),('A','E','I','O')):
            ck(mod.necessary(model,k,s,p),all(val(w,k,s,p) for w in worlds))
            if k in ('I','O'):
                sets=[ext(w,s)&ext(w,p) if k=='I' else ext(w,s)-ext(w,p) for w in worlds]
                ck(mod.rigid_witnesses(model,k,s,p),tuple(sorted(set.intersection(*sets))))
        for n,(a,b,c) in specs.items():
            pre=all(val(w,*a) and val(w,*b) for w in worlds)
            ck(mod.propositions(n),(a,b,c));ck(mod.premises(model,n,True),bool(pre and all(ext(w,'M') for w in worlds)))
            if n in ('Baroco','Bocardo') and pre:
                for wi,x in enumerate(mod.exposition(model,n)):ck(x in ext(worlds[wi],'S')-ext(worlds[wi],'P'),True)
    try:mod.Model(True,((0,0,0),))
    except ValueError:pass
    else:raise RuntimeError('bool accepted')
probes(m)
detected=[]
for i,(name,old,new) in enumerate(mutations):
    if old not in source:raise RuntimeError('mutation target missing')
    module=types.ModuleType('mutant_'+str(i));sys.modules[module.__name__]=module
    exec(compile(source.replace(old,new),'<isolated-mutant>','exec'),module.__dict__)
    try:probes(module)
    except RuntimeError:detected.append(name)
    else:raise RuntimeError('mutant survived: '+name)
    finally:sys.modules.pop(module.__name__)
print(json.dumps({'status':'PASS','explicit_checks':checks,'ordered_two_world_models':4096,'independent_set_oracle':True,'invalid_inputs':len(invalid),'exposition_world_checks':local,'stable_model_checks':stable,'witness_gap_counts':gaps,'report_rows':rows,'detected_mutations':detected,'limits':'Bounded implementation audit, not general proof or unique historical semantics.'},indent=2))
