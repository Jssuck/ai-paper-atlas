"""Independent set-based oracle. Author functions are the system under test only."""
import hashlib, importlib.util, itertools, json, pathlib, sys
R=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('author',R/'model.py'); a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
K='AEIO';T='SPM'
# Build ordinary sets from Cartesian boolean vectors; no author semantic functions.
V=list(itertools.product((False,True),repeat=3))
def model(n):
    selected=[v for v in V if n & (1 << (int(v[0])+2*int(v[1])+4*int(v[2])))]
    return {t:{i for i,v in enumerate(selected) if v[j]} for j,t in enumerate(T)}
def truth(k,s,p,d):
    x,y=d[s],d[p]
    if k=='A':return x<=y
    if k=='E':return x.isdisjoint(y)
    if k=='I':return not x.isdisjoint(y)
    return not x<=y
PAIRS={1:(('M','P'),('S','M')),2:(('P','M'),('S','M')),3:(('M','P'),('M','S'))}
def holds(f,m,d):
    pair=PAIRS[f]
    return (not (truth(m[0],*pair[0],d) and truth(m[1],*pair[1],d))) or truth(m[2],'S','P',d)
def check(ok,msg):
    if not ok:raise RuntimeError(msg)
D={n:model(n) for n in range(1,256)};counts={'atomic':0,'candidate_model_checks':0,'classification_sets':0,'contradictions':0,'weakening':0,'metamorphic':0,'invalid_inputs':0,'search_subsets':0,'search_queries':0}
for n,d in D.items():
 for s,p,k in itertools.product(T,T,K):
    check(a.truth(k,s,p,n)==truth(k,s,p,d),'atomic');counts['atomic']+=1
 for t in T:check(a.term_nonempty(t,n)==bool(d[t]),'nonempty')
 for k,neg in zip(K,'OIEA'):
    check(truth(k,'S','P',d)!=truth(neg,'S','P',d),'contradiction');counts['contradictions']+=1
 if d['S']:
    for x,y in [('A','I'),('E','O')]:
     check(not truth(x,'S','P',d) or truth(y,'S','P',d),'weakening');counts['weakening']+=1
 for perm in itertools.permutations(T):
    # Relabel each occupied object type into a different term coordinate system.
    new=0
    for old in range(8):
     if n & (1<<old):
      bits={'S':bool(old&1),'P':bool(old&2),'M':bool(old&4)}
      typ=sum((1<<i) for i,t in enumerate(perm) if bits[t]);new|=1<<typ
    for k,s,p in itertools.product(K,T,T):
     old_s=perm[T.index(s)];old_p=perm[T.index(p)]
     check(a.truth(k,s,p,new)==truth(k,old_s,old_p,d),'renaming');counts['metamorphic']+=1
valid={}
for policy in (False,True):
 ns=tuple(n for n,d in D.items() if not policy or all(d[t] for t in T))
 check(a.models(policy)==ns,'models')
 good=[]
 for f in (1,2,3):
  for mood in itertools.product(K,repeat=3):
   mood=''.join(mood);bad=[]
   for n in ns:
    if not holds(f,mood,D[n]):bad.append(n)
    counts['candidate_model_checks']+=1
   check(a.countermodels(f,mood,policy)==tuple(bad),'countermodels')
   if not bad:good.append((f,mood))
 check(a.classifications(policy)==tuple(good),'classification');counts['classification_sets']+=1;valid[str(policy)]=good
check(len(valid['False'])==12 and len(valid['True'])==18,'12/18')
canonical=((1,'AAA'),(1,'EAE'),(1,'AII'),(1,'EIO'),(2,'EAE'),(2,'AEE'),(2,'EIO'),(2,'AOO'),(3,'AAI'),(3,'IAI'),(3,'AII'),(3,'EAO'),(3,'OAO'),(3,'EIO'))
check(a.CANONICAL==canonical,'canonical')
check(a.canonical_counts()==dict(zip(K,(1,3,4,6))),'canonical counts')
check(set(valid['True'])-set(canonical)=={(1,'AAI'),(1,'EAO'),(2,'EAO'),(2,'AEO')},'extra')
# Exhaust all availability subsets. Oracle enumerates target-specific positions directly.
for mask in range(1<<14):
 avail=tuple(r for i,r in enumerate(canonical) if mask&(1<<i));counts['search_subsets']+=1
 for k in K:
  options=[r for r in canonical if r[1][2]==k];match=next((r for r in options if r in avail),None)
  expected={'target':k,'inspections':options.index(match)+1 if match else len(options),'found':list(match) if match else None}
  check(a.search(k,avail)==expected,'search');counts['search_queries']+=1
bad_calls=[]
for x in [True,False,0,256,-1,1.0,'1',None,[],{}]:bad_calls.append((a.truth,('A','S','P',x)))
for x in [None,[],{},1,'a','AA','']:
 bad_calls.extend([(a.truth,(x,'S','P',1)),(a.truth,('A',x,'P',1)),(a.truth,('A','S',x,1))])
for x in [True,False,0,4,-1,1.0,'1',None,[],{}]:bad_calls.append((a.premises,(x,'AAA')))
for x in [None,[],{},'aaa','AA','AAAA','AAQ',1]:bad_calls.append((a.premises,(1,x)))
for x in [0,1,None,[],{},'True']:bad_calls.extend([(a.models,(x,)),(a.classifications,(x,))])
for x in [[],None,{},((1,'AAI'),),((4,'AAA'),),((1,'AAA'),(1,'AAA')),('AAA',),((1,),),([1,'AAA'],),((1,'AAA',0),)]:bad_calls.append((a.search,('A',x)))
for fn,args in bad_calls:
 try:fn(*args)
 except ValueError:counts['invalid_inputs']+=1
 else:raise RuntimeError('invalid input accepted '+repr(args))
# Named wrong semantic variants, not a claim of arbitrary source mutation coverage.
variants={
 'A_requires_subject':lambda d: bool(d['S']) and d['S']<=d['P'],
 'E_means_not_A':lambda d: not d['S']<=d['P'],
 'I_means_all':lambda d: d['S']<=d['P'],
 'O_means_disjoint':lambda d:d['S'].isdisjoint(d['P']),
 'O_reversed':lambda d:not d['P']<=d['S'],
 'I_means_proper_some':lambda d:bool(d['S']&d['P']) and bool(d['S']-d['P']),
 'E_requires_subject':lambda d:bool(d['S']) and d['S'].isdisjoint(d['P']),
}
correct=['A','E','I','O','O','I','E'];witness={}
for (name,fn),k in zip(variants.items(),correct):
 ns=[n for n,d in D.items() if fn(d)!=truth(k,'S','P',d)];check(bool(ns),'undetected variant');witness[name]=ns[0]
manifest=json.loads((R/'author-manifest.json').read_text())
for p,h in manifest.items():check(hashlib.sha256((R/p).read_bytes()).hexdigest()==h,'author manifest '+p)
print(json.dumps({'python':sys.version,'optimization':sys.flags.optimize,'checks':counts,'population':[len(D),sum(all(d[t] for t in T) for d in D.values())],'valid':valid,'semantic_variant_witnesses':witness,'author_hashes':len(manifest),'scope':'Finite implementation review; search accepts route labels, does not match premises or verify certificates; not historical/general-proof certification.'},indent=2))
