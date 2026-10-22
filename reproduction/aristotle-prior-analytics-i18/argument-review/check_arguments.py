"""Independent finite audit. No import of author code; not a proof by exhaustion."""
import hashlib, itertools, json, platform, sys
from pathlib import Path

def require(v, message):
    if not v: raise RuntimeError(message)

def cat(worlds, p, s, form, mode):
    values=[]
    for x in worlds[0][s]:
        signs=[x in w[p] for w in worlds]
        if form in ('E','O'): signs=[not z for z in signs]
        if mode=='actual': v=signs[0]
        elif mode=='necessary': v=all(signs)
        elif mode=='possible': v=any(signs)
        elif mode=='contingent': v=any(signs) and not all(signs)
        else: raise ValueError(mode)
        values.append(v)
    return all(values) if form in ('A','E') else any(values)

def rigid(ws,t): return all(w[t]==ws[0][t] for w in ws)
def disjoint(ws,p,s): return all(not (w[p]&w[s]) for w in ws)
def serial(ws): return [[sorted(x) for x in w] for w in ws]
def worldsets(n):
    subs=[frozenset(i for i in range(n) if m>>i&1) for m in range(2**n)]
    return itertools.product(subs,repeat=3)
def main():
    counts=dict(configurations=0,quality_equivalences=0,actual_E_symmetries=0,direct_universal=0,direct_particular=0,reverse_universal=0,reverse_particular_native=0,rigid_reverse_universal=0)
    witnesses={}; pairs={}
    for n in (1,2):
      for ws in itertools.product(tuple(worldsets(n)),repeat=2):
        counts['configurations']+=1
        for p,s in itertools.permutations(range(3),2):
          for a,b in [('A','E'),('I','O')]:
            require(cat(ws,p,s,a,'contingent')==cat(ws,p,s,b,'contingent'),'Q quality equivalence');counts['quality_equivalences']+=1
          require(cat(ws,p,s,'E','actual')==cat(ws,s,p,'E','actual'),'actual E symmetry');counts['actual_E_symmetries']+=1
        eab=cat(ws,0,1,'E','actual');eac=cat(ws,0,2,'E','actual')
        for q,con,label in [('A','E','universal'),('I','O','particular')]:
          direct=eab and cat(ws,0,2,q,'contingent')
          if direct and disjoint(ws,0,1):
            require(cat(ws,1,2,con,'possible'),'persistent exclusion forward');counts['direct_'+label]+=1
          reverse=eac and cat(ws,0,1,q,'contingent')
          if reverse and disjoint(ws,0,2):
            require(cat(ws,2,1,con,'possible'),'persistent exclusion reverse native');counts['reverse_universal' if q=='A' else 'reverse_particular_native']+=1
            if q=='A' and rigid(ws,1) and rigid(ws,2):
              require(cat(ws,1,2,'E','necessary'),'rigid reverse universal');counts['rigid_reverse_universal']+=1
            if not cat(ws,1,2,con,'possible'):
              key='reverse_'+label+'_conversion_fails'
              witnesses.setdefault(key,{'n':n,'worlds':serial(ws)})
          if direct and not cat(ws,1,2,con,'possible'):
            witnesses.setdefault('unbridged_'+label+'_fails',{'n':n,'worlds':serial(ws)})
          if direct and disjoint(ws,0,1) and ws[0][1] and ws[0][2] and not cat(ws,1,2,con,'contingent'):
            witnesses.setdefault('strict_'+label+'_fails',{'n':n,'worlds':serial(ws)})
        if eac and cat(ws,0,1,'I','contingent') and disjoint(ws,0,2) and rigid(ws,1) and rigid(ws,2) and ws[0][2] and not cat(ws,1,2,'O','possible'):
          witnesses.setdefault('rigid_reverse_particular_conversion_fails',{'n':n,'worlds':serial(ws)})
        if not (rigid(ws,1) and rigid(ws,2) and ws[0][1] and ws[0][2]): continue
        endpoint='equal' if ws[0][1]==ws[0][2] else ('disjoint' if not ws[0][1]&ws[0][2] else None)
        if endpoint is None: continue
        for pure,qform,orientation in itertools.product(('A','I','O'),('A','E','I','O'),(0,1)):
          ps,qs=(1,2) if orientation==0 else (2,1)
          if cat(ws,0,ps,pure,'actual') and cat(ws,0,qs,qform,'contingent'):
            key=f'actual_{pure}_Q_{qform}_orientation_{orientation}'
            pairs.setdefault(key,{}).setdefault(endpoint,{'n':n,'worlds':serial(ws)})
    require(len(pairs)==24,'24 failure layouts')
    require(all(set(v)=={'equal','disjoint'} for v in pairs.values()),'paired witnesses')
    require(len(witnesses)==7,'all seven gap types')
    # Independent hand-written witnesses for every mathematical prose example.
    def ws(a0,b0,c0,a1,b1,c1):
        return tuple(tuple(frozenset(z) for z in row) for row in ((a0,b0,c0),(a1,b1,c1)))
    examples={
      '5.1_overlap':ws((0,1),(0,),(0,),(),(0,),(0,)),
      '5.1_separation':ws((0,1),(1,),(0,),(),(1,),(0,)),
      '5.2_overlap':ws((0,),(0,1),(0,),(),(0,1),(0,)),
      '5.2_separation':ws((0,),(1,),(0,),(),(1,),(0,)),
      '6.1_missing_bridge':ws((),(0,),(0,),(0,),(0,),(0,)),
      '6.2_actual_gap':ws((),(0,),(0,),(0,),(),(0,)),
      '6.3_strict_gap':ws((),(1,),(0,),(0,),(1,),(0,)),
      '6.3_quantifier_gap':ws((0,),(1,),(0,1),(1,),(0,),(0,1)),
      '6.4_nonempty_reverse':ws((),(0,),(0,),(0,),(0,),()),
      '6.4_rigid_particular':ws((),(0,1),(0,),(1,),(0,1),(0,))}
    a=examples['5.1_overlap']; b=examples['5.1_separation']
    for z in (a,b): require(cat(z,0,1,'A','actual') and cat(z,0,2,'A','contingent'),'5.1 premises')
    for f in ('E','O'): require(not cat(a,1,2,f,'possible'),'5.1 negative fail')
    for f in ('A','I'): require(not cat(b,1,2,f,'possible'),'5.1 positive fail')
    for k in ('5.2_overlap','5.2_separation'):
      z=examples[k];require(cat(z,0,1,'O','actual') and cat(z,0,2,'A','contingent'),'5.2 premises')
    require(not cat(examples['5.2_overlap'],1,2,'O','possible'),'5.2 target')
    z=examples['6.1_missing_bridge'];require(cat(z,0,1,'E','actual') and cat(z,0,2,'A','contingent') and not cat(z,1,2,'E','possible'),'6.1')
    z=examples['6.2_actual_gap'];require(disjoint(z,0,1) and cat(z,0,2,'A','contingent') and cat(z,1,2,'E','possible') and not cat(z,1,2,'E','actual'),'6.2 actual gap')
    z=examples['6.3_strict_gap'];require(disjoint(z,0,1) and cat(z,0,2,'A','contingent') and cat(z,1,2,'E','necessary') and not cat(z,1,2,'E','contingent'),'6.3 strict')
    z=examples['6.3_quantifier_gap'];require(cat(z,1,2,'E','possible') and not any(not(w[1]&z[0][2]) for w in z),'6.3 quantifier')
    z=examples['6.4_nonempty_reverse'];require(disjoint(z,0,2) and cat(z,0,1,'A','contingent') and cat(z,2,1,'E','possible') and not cat(z,1,2,'E','possible'),'6.4 reverse')
    z=examples['6.4_rigid_particular'];require(rigid(z,1) and rigid(z,2) and disjoint(z,0,2) and cat(z,0,1,'I','contingent') and not cat(z,1,2,'O','possible'),'6.4 particular')
    prose_examples={k:serial(v) for k,v in examples.items()}
    out={'scope':'Modern actual-subject semantics; domain sizes 1 and 2, two worlds, actual world 0. No general theorem proved by enumeration.','counts':counts,'prose_examples':prose_examples,'gap_witnesses':witnesses,'failure_layout_pairs':pairs,'status':'pass'}
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
