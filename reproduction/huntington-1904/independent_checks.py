"""Independent direct-formula checks, including nonclosed rules. Standard library only.

Reference formulas do not call the production equation/Check/complement helpers.
They share the documented nonunique-bound convention; this is not a theorem proof.
"""
import itertools,json
import huntington as h
P=itertools.product

def first_ref(K,s,t):
 z=[z for z in K if all(s[a,z]==a for a in K)]; u=[u for u in K if all(t[a,u]==a for a in K)]
 def dist(s,t):
  for a,b,c in P(K,repeat=3):
   bc=t[b,c]; ab=s[a,b]; ac=s[a,c]
   if any(v not in K for v in (bc,ab,ac)): continue
   lhs=s[a,bc]; rhs=t[ab,ac]
   if lhs in K and rhs in K and lhs!=rhs: return False
  return True
 return dict(Ia=all(v in K for v in s.values()),Ib=all(v in K for v in t.values()),IIa=bool(z),IIb=bool(u),IIIa=all(s[a,b]==s[b,a] for a,b in P(K,repeat=2) if s[a,b] in K and s[b,a] in K),IIIb=all(t[a,b]==t[b,a] for a,b in P(K,repeat=2) if t[a,b] in K and t[b,a] in K),IVa=dist(s,t),IVb=dist(t,s),V=len(z)!=1 or len(u)!=1 or all(any(s[a,b]==u[0] and t[a,b]==z[0] for b in K) for a in K),VI=len(K)>1)

def second_ref(K,R):
 lower=lambda a,b:R[a,b]
 z=[a for a in K if all(a==b or R[a,b] for b in K)];u=[a for a in K if all(a==b or R[b,a] for b in K)]
 q={'1':all(R[a,a] for a in K),'2':all(a==b or not(R[a,b] and R[b,a]) for a,b in P(K,repeat=2)), '3':all(not(R[a,b] and R[b,c]) or R[a,c] for a,b,c in P(K,repeat=3)), '4':bool(z),'5':bool(u)}
 incomparable=[(a,b) for a,b in P(K,repeat=2) if a!=b and not(R[a,b] or R[b,a])]
 q['6']=all(any(R[a,s] and R[b,s] and all(y==s or not(R[a,y] and R[b,y]) or R[s,y] for y in K) for s in K) for a,b in incomparable)
 q['7']=all(any(R[p,a] and R[p,b] and all(x==p or not(R[x,a] and R[x,b]) or R[x,p] for x in K) for p in K) for a,b in incomparable)
 unique=len(z)==len(u)==1
 comps={a:[b for b in K if all(not(R[x,a] and R[x,b]) or x==z[0] for x in K) and all(not(R[a,x] and R[b,x]) or x==u[0] for x in K)] for a in K} if unique else {a:list(K) for a in K}
 q['8']=all(comps.values()) if unique else True
 q['9']=not all(q[k] for k in ('1','4','5','8')) or all(R[a,bar] or any(x!=zero and R[x,a] and R[x,b] for x in K) for zero in z for a,b in P(K,repeat=2) for bar in comps[b])
 q['10']=len(K)>1
 return q

def third_ref(K,s):
 z=[z for z in K if all(s[a,z]==a for a in K)];u=[u for u in K if all(s[u,a]==u for a in K)]
 assoc=True
 for a,b,c in P(K,repeat=3):
  ab=s[a,b];bc=s[b,c]
  if ab not in K or bc not in K: continue
  lhs=s[ab,c];rhs=s[a,bc]
  if lhs in K and rhs in K and lhs!=rhs: assoc=False
 q={'A':all(s[a,a]==a for a in K if s[a,a] in K),'B':all(s[a,b]==s[b,a] for a,b in P(K,repeat=2) if s[a,b] in K and s[b,a] in K),'C':assoc,'D':bool(z),'E':bool(u),'F':all(x in K for x in s.values())}
 unique=len(z)==len(u)==1
 comps={a:[b for b in K if s[a,b]==u[0] and all(not(s[x,a]==a and s[x,b]==b) or x==z[0] for x in K)] for a in K} if unique else {a:list(K) for a in K}
 q['G']=all(comps.values()) if unique else True
 q['H']=not all(q[k] for k in ('A','D','E','G')) or all(s[a,bar]==bar or any(x!=zero and s[a,x]==a and s[b,x]==b for x in K) for zero in z for a,b in P(K,repeat=2) for bar in comps[b])
 q['J']=len(K)>1
 return q

def same(got,want):
 assert {k:v.holds for k,v in got.items()}==want, ({k:v.holds for k,v in got.items()},want)
count={}
K=(0,1); pairs=list(P(K,repeat=2))
for vals in P((0,1,'OUT'),repeat=8):
 s=dict(zip(pairs,vals[:4]));t=dict(zip(pairs,vals[4:]));same(h.first(h.Algebra(K,{'+':s,'*':t})),first_ref(K,s,t))
count['first_two_elements_with_external_output']=3**8
for n in (1,2,3):
 K=tuple(range(n)); pairs=list(P(K,repeat=2))
 for vals in P((False,True),repeat=n*n):
  r=dict(zip(pairs,vals));same(h.second(h.Relation(K,{p for p,v in r.items() if v})),second_ref(K,r))
count['second_all_relations_n1_to3']=2+16+512
for n,outputs in ((1,(0,'OUT')),(2,(0,1,'OUT')),(3,(0,1,2))):
 K=tuple(range(n)); pairs=list(P(K,repeat=2))
 for vals in P(outputs,repeat=n*n):
  s=dict(zip(pairs,vals));same(h.third(h.Algebra(K,{'+':s})),third_ref(K,s))
count['third_n1_partial_n2_partial_n3_closed']=2+81+19683
# Check table relabeling does not hard-code numeric zero or one.
for generator,checker in ((h.first_original_models,h.first),(h.third_original_models,h.third)):
 for label,m in generator().items():
  rename={x:'element_'+str(i) for i,x in enumerate(reversed(m.elements))}
  mm=h.Algebra(tuple(rename[x] for x in m.elements),{op:{(rename[a],rename[b]):rename.get(v,'external') for (a,b),v in tab.items()} for op,tab in m.operations.items()})
  assert h.failed(checker(m))==h.failed(checker(mm))
count['relabelled_original_algebras']=16
print(json.dumps(count,indent=2));print('All independent reference comparisons and relabeling tests passed.')
