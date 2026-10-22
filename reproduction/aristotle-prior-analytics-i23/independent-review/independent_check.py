"""Independent bounded oracle for I.23; no author implementation used in oracle."""
import sys, pathlib, json, itertools, math
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from model import Model, all_models, entails, skeleton, check_chain, raa_certificate, parity_probe

def need(v,msg):
    if not v: raise RuntimeError(msg)

def oracle(names,mask,q,p,s):
    # Build explicit Boolean membership vectors, rather than author set comparisons.
    occupied=[v for a,v in enumerate(itertools.product((False,True), repeat=len(names))) if mask & (1 << sum((1 << i) for i,b in enumerate(v) if b))]
    pi,si=names.index(p),names.index(s)
    pp=[v[pi] for v in occupied];ss=[v[si] for v in occupied]
    if q=='A': return all((not y) or x for x,y in zip(pp,ss))
    if q=='E': return all(not(x and y) for x,y in zip(pp,ss))
    if q=='I': return any(x and y for x,y in zip(pp,ss))
    if q=='O': return any(y and not x for x,y in zip(pp,ss))
    raise ValueError('oracle quality')

names=('P','M','S'); queries=0; metamorphic=0; rows=[]
for mask in range(1,256):
    m=Model(names,mask)
    vals={}
    for q,p,s in itertools.product('AEIO',names,names):
        value=oracle(names,mask,q,p,s);need(m.holds(q,p,s)==value,f'oracle {mask,q,p,s}')
        vals[q,p,s]=value;queries+=1
        renamed=Model(('X','Y','Z'),mask)
        need(renamed.holds(q,('X','Y','Z')[names.index(p)],('X','Y','Z')[names.index(s)])==value,'renaming');metamorphic+=1
    for p,s in itertools.product(names,names):
        need(vals['A',p,s]!=vals['O',p,s] and vals['E',p,s]!=vals['I',p,s],'contradictions');metamorphic+=2
        need(vals['E',p,s]==vals['E',s,p] and vals['I',p,s]==vals['I',s,p],'symmetry');metamorphic+=2
    rows.append((mask,vals,all(any(mask&(1<<a) and a&(1<<i) for a in range(8)) for i in range(3))))
need(len(list(all_models()))==255,'count');need(sum(r[2] for r in rows)==218,'nonempty count')

# Independently evaluate all 4 x 4^3 x 2 figure/quality/existence configurations.
patterns=[(('M','P'),('S','M')),(('P','M'),('M','S')),(('P','M'),('S','M')),(('M','P'),('M','S'))]
configurations=0
for edges in patterns:
  for q1,q2,qc in itertools.product('AEIO',repeat=3):
    p1=(q1,edges[0][1],edges[0][0]);p2=(q2,edges[1][1],edges[1][0]);c=(qc,'P','S')
    for nonempty in (False,True):
      witnesses=[mask for mask,v,ne in rows if (not nonempty or ne) and v[p1] and v[p2] and not v[c]]
      expected=(False,witnesses[0]) if witnesses else (True,None)
      need(entails((p1,p2),c,nonempty)==expected,'entails mismatch');configurations+=1

# Four-term chain oracle on all nonempty atom occupancies.
chain_cases=0; chain_hypotheses=0
for mask in range(1,65536):
    names4=('S','C','M','P');m=Model(names4,mask)
    expected_p=all(oracle(names4,mask,'A',names4[i+1],names4[i]) for i in range(3))
    expected_c=oracle(names4,mask,'A','P','S')
    need(check_chain(m,names4)=={'premises':expected_p,'conclusion':expected_c},'chain')
    need(not expected_p or expected_c,'chain semantic failure');chain_cases+=1;chain_hypotheses+=expected_p
need(chain_hypotheses==31,'chain premises')

# All valid skeletons and swapped premise order; term-role reversal is not silently merged.
expected_shapes=['chain_forward','chain_reverse','common_predicate','common_subject']
for edges,expected in zip(patterns,expected_shapes):
    need(skeleton(edges)==expected and skeleton(edges[::-1])==expected,'skeleton')

# Check every pair of same/different AEIO forms and term positions, not only valid pairs.
raa_cases=0
for mask in (1,8,24,72,129,255):
    m=Model(names,mask)
    props=list(itertools.product('AEIO',names,names))
    for assumption,derived in itertools.product(props,repeat=2):
        premise=('A','P','S');r=raa_certificate(m,premise,assumption,derived)
        pairing=(assumption[0],derived[0]) in [('A','O'),('O','A'),('E','I'),('I','E')] and assumption[1:]==derived[1:]
        need(r=={'contradictory_pair':pairing,'premise_true':oracle(names,mask,*premise),'assumption_true':oracle(names,mask,*assumption),'derived_true':oracle(names,mask,*derived),'outer_discharge_verified':False},'RAA scope');raa_cases+=1

# Invalid input expectations explicitly checked without removable assertions.
invalid=[]
for terms in ([],(),['P'],('P','P'),('',),('x-y',),('P',1),('P',False),('A','B','C','D','E')):
    invalid.append(lambda terms=terms:Model(terms,1))
for mask in (0,-1,256,True,False,1.0,'1',None):invalid.append(lambda mask=mask:Model(names,mask))
m=Model(names,1)
for q in ('a','e','i','o','',True,1,None,[]):invalid.append(lambda q=q:m.holds(q,'P','S'))
for t in ('Q','',True,1,None,[]):
    invalid.append(lambda t=t:m.extension(t));invalid.append(lambda t=t:m.holds('A',t,'S'));invalid.append(lambda t=t:m.holds('A','P',t))
for v in (0,1,None,'yes',[]):invalid.append(lambda v=v:list(all_models(require_nonempty_terms=v)))
for ps,c in [((),('A','P','S')),([],('A','P','S')),((('A','P'),),('A','P','S')),((('A','P','S'),),['A','P','S']),((('A','P','S'),),('a','P','S')),((('A','P','S'),),('A','Q','S'))]:invalid.append(lambda ps=ps,c=c:entails(ps,c))
for edges in ((),[],(('S','M'),('S','M')),(('S','P'),('M','P')),(('S','S'),('M','P')),(('S','M'),('M','Q')),(('S','M'),['M','P'])):invalid.append(lambda edges=edges:skeleton(edges))
for ch in ((),('S',),('S','S'),('S','Q'),['S','P']):invalid.append(lambda ch=ch:check_chain(m,ch))
invalid.append(lambda:check_chain(None,('S','P')))
for lim in (0,-1,1001,True,False,1.0,'10',None):invalid.append(lambda lim=lim:parity_probe(lim))
invalid.append(lambda:raa_certificate(None,('A','P','S'),('O','P','S'),('A','P','S')))
invalid.append(lambda:raa_certificate(m,['A','P','S'],('O','P','S'),('A','P','S')))
for i,f in enumerate(invalid):
    try:f()
    except ValueError:pass
    else:raise RuntimeError(f'invalid accepted {i}')

# Explicit semantic perturbations, with at least one witness for each. Not source-mutation coverage.
mutants={
 'reverse_A':lambda mask,q,p,s:oracle(names,mask,q,s,p) if q=='A' else oracle(names,mask,q,p,s),
 'reverse_O':lambda mask,q,p,s:oracle(names,mask,q,s,p) if q=='O' else oracle(names,mask,q,p,s),
 'A_requires_subject':lambda mask,q,p,s:oracle(names,mask,q,p,s) and oracle(names,mask,'I',s,s) if q=='A' else oracle(names,mask,q,p,s),
 'E_is_not_A':lambda mask,q,p,s:not oracle(names,mask,'A',p,s) if q=='E' else oracle(names,mask,q,p,s),
 'I_as_A':lambda mask,q,p,s:oracle(names,mask,'A',p,s) if q=='I' else oracle(names,mask,q,p,s),
 'O_as_E':lambda mask,q,p,s:oracle(names,mask,'E',p,s) if q=='O' else oracle(names,mask,q,p,s),
}
witnesses={}
for label,fn in mutants.items():
    for mask,values,ne in rows:
      for (q,p,s),expected in values.items():
        if fn(mask,q,p,s)!=expected:
          witnesses[label]={'mask':mask,'query':[q,p,s]};break
      if label in witnesses:break
    need(label in witnesses,'undetected explicit mutant')
need(skeleton(patterns[1])!=skeleton(patterns[0]),'direction mutation')
need(raa_certificate(m,('A','P','S'),('O','P','S'),('A','P','S'))['outer_discharge_verified'] is False,'false certification mutation')

for lim in (1,2,17,100):
    r=parity_probe(lim)
    need(r['parity_checks']==lim+1 and r['positive_pairs']==lim*lim,'parity bounds')
    need(r['parity_failures']==[] and r['reduced_solutions']==[] and r['general_irrationality_proved'] is False,'finite parity scope')

# Free B is interpreted over fixed x,y; atom representative labels may change.
free_B=[]
for mask,B in [(129,{'x'}),(24,{'y'})]:
    mm=Model(('A','C','B'),mask); A={'x'}
    truths=[A<=B,A.isdisjoint(B),bool(A&B),bool(A-B)]
    actual=[mm.holds(q,'B','A') for q in 'AEIO']
    need(actual==truths and mm.holds('A','A','C'),'fixed-domain free B')
    free_B.append(actual)
need(all(x!=y for x,y in zip(*free_B)),'free B flips')

out={'free_B_fixed_domain_truths':free_B,'AEIO_oracle_queries' :queries,'metamorphic_checks':metamorphic,'entailment_configurations':configurations,'chain_models':chain_cases,'chain_antecedent_models':chain_hypotheses,'RAA_pairing_cases':raa_cases,'invalid_inputs_rejected':len(invalid),'semantic_mutant_witnesses':witnesses,'additional_scope_mutants':2,'parity_limits':[1,2,17,100],'limits':['Independent finite implementation audit, not general theorem proof.','Six explicit AEIO semantic variants and two scope variants, not exhaustive mutation testing.','RAA pairing still does not check a derivation or discharge.']}
print(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True))
