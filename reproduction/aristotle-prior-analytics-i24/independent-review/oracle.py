"""Independent Boolean-row oracle, deliberately not calling author evaluators."""
import sys, json, itertools, hashlib, pathlib
from fractions import Fraction
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import model as author
NAMES=('S','P','M'); FORMS='AEIO'

def require(condition, message):
    if not condition: raise RuntimeError(message)

def rows(mask):
    return [tuple((k//(2**b))%2 == 1 for b in range(3)) for k in range(8) if (mask//(2**k))%2]

def oracle(rs,form,s,p):
    i,j=NAMES.index(s),NAMES.index(p)
    if form=='A': return all(not x[i] or x[j] for x in rs)
    if form=='E': return all(not(x[i] and x[j]) for x in rs)
    if form=='I': return any(x[i] and x[j] for x in rs)
    if form=='O': return any(x[i] and not x[j] for x in rs)
    raise ValueError(form)

def expected(mask,fig,mood):
    rs=rows(mask)
    if fig==1: pairs=[('M','P'),('S','M'),('S','P')]
    elif fig==2: pairs=[('P','M'),('S','M'),('S','P')]
    else: pairs=[('M','P'),('M','S'),('S','P')]
    return tuple(oracle(rs,f,*p) for f,p in zip(mood,pairs))

def encode(rs):
    return sum(2**k for k in {sum((2**b)*int(r[b]) for b in range(3)) for r in rs})

def run():
    counts={'primitive_queries':0,'syllogism_evaluations':0,'classifications':0,'metamorphic_comparisons':0,'invalid_inputs':0}
    for mask in range(1,256):
        rs=rows(mask)
        require(author.domain(mask)==frozenset(k for k in range(8) if (mask//2**k)%2),'domain')
        for s,p,f in itertools.product(NAMES,NAMES,FORMS):
            base=oracle(rs,f,s,p)
            require(author.proposition(mask,f,s,p)==base, f'primitive {mask} {f}{s}{p}')
            counts['primitive_queries']+=1
            # Simultaneous arbitrary permutation of predicates, independent of objects.
            for perm in itertools.permutations(range(3)):
                transformed=encode([tuple(r[b] for b in perm) for r in rs])
                ns=NAMES[perm.index(NAMES.index(s))]; np=NAMES[perm.index(NAMES.index(p))]
                require(author.proposition(transformed,f,ns,np)==base,'rename')
                counts['metamorphic_comparisons']+=1
            # Duplicating all witnesses and adding duplicates cannot alter AEIO.
            require(oracle(rs+rs,f,s,p)==base,'duplicate oracle invariance')
            counts['metamorphic_comparisons']+=1
        for fig in (1,2,3):
            for mood in map(''.join,itertools.product(FORMS,repeat=3)):
                require(author.evaluate(mask,fig,mood)==expected(mask,fig,mood),'evaluate')
                counts['syllogism_evaluations']+=1
    for policy in ('allow_empty_terms','all_terms_nonempty'):
        universe=[k for k in range(1,256) if policy=='allow_empty_terms' or all(any(r[b] for r in rows(k)) for b in range(3))]
        require(tuple(universe)==author.models(policy),'policy')
        valids=[]
        for fig in (1,2,3):
            for mood in map(''.join,itertools.product(FORMS,repeat=3)):
                vals=[(k,expected(k,fig,mood)) for k in universe]
                premises=[k for k,v in vals if v[0] and v[1]]
                bad=[k for k,v in vals if v[0] and v[1] and not v[2]]
                want=dict(figure=fig,mood=mood,policy=policy,premise_models=len(premises),countermodel_count=len(bad),valid=not bad,first_countermodel=bad[0] if bad else None)
                require(author.classify(fig,mood,policy)==want,'classify complete output')
                if not bad:
                    valids.append(f'{mood}-{fig}')
                    require(any(x in 'AI' for x in mood[:2]),'positive premise condition')
                    require(any(x in 'AE' for x in mood[:2]),'universal premise condition')
                    require(mood[2] not in 'AE' or all(x in 'AE' for x in mood[:2]),'universal conclusion condition')
                counts['classifications']+=1
        counts[policy]={'models':len(universe),'valid':len(valids),'valid_moods':valids}
    invalid=[]
    for x in [True,False,0,-1,256,1.,'1',None,[],{},Fraction(1)]:
        invalid.extend([(author.domain,(x,)),(author.evaluate,(x,1,'AAA'))])
    for x in ['a','Q','',None,[],{},True]:
        invalid.append((author.proposition,(1,x,'S','P')))
        invalid.append((author.extension,(1,x)))
    for x in [True,False,0,4,-1,1.,'1',None,[]]: invalid.append((author.classify,(x,'AAA')))
    for x in ['','AA','AAAA','aaa','AAQ',None,[],123,True]: invalid.append((author.classify,(1,x)))
    for x in ['',None,[],{},True,'all']: invalid.append((author.models,(x,)))
    for x in [(True,1,0,0),(1.,1,0,0),(-1,1,0,0),(1,1,2,0),(1,1,0,-1),('1',1,0,0),(None,1,0,0)]: invalid.append((author.equal_remainders,x))
    for fn,args in invalid:
        try: fn(*args)
        except ValueError: counts['invalid_inputs']+=1
        else: raise RuntimeError(f'Invalid input accepted {fn.__name__} {args}')
    # Named semantic variants, not source-code mutation coverage.
    variants={
      'reverse_A':lambda rs,s,p:oracle(rs,'A',p,s),
      'A_imports_existence':lambda rs,s,p:oracle(rs,'A',s,p) and any(r[NAMES.index(s)] for r in rs),
      'E_as_O':lambda rs,s,p:oracle(rs,'O',s,p),
      'I_as_A':lambda rs,s,p:oracle(rs,'A',s,p),
      'O_reverse':lambda rs,s,p:oracle(rs,'O',p,s),
      'E_as_not_A':lambda rs,s,p:not oracle(rs,'A',s,p),
      'I_requires_all':lambda rs,s,p:all(r[NAMES.index(s)] and r[NAMES.index(p)] for r in rs),
      'O_as_E':lambda rs,s,p:oracle(rs,'E',s,p),
      'A_as_some':lambda rs,s,p:oracle(rs,'I',s,p)}
    intended=['A','A','E','I','O','E','I','O','A']; witnesses={}
    for (name,fn),f in zip(variants.items(),intended):
        for mask in range(1,256):
            rs=rows(mask)
            if fn(rs,'S','P')!=oracle(rs,f,'S','P'):
                witnesses[name]={'mask':mask,'intended_form':f,'correct':oracle(rs,f,'S','P'),'variant':fn(rs,'S','P')};break
        require(name in witnesses,'variant undetected '+name)
    counts['semantic_variants']=witnesses
    # Article's exact rational example plus the author's different example.
    arithmetic=[]
    for a,b,c,d in [(180,180,Fraction(75,2),Fraction(75,2)),(180,180,30,40),(Fraction(9,2),Fraction(9,2),Fraction(1,3),Fraction(1,3)),(4,5,1,1),(0,0,0,0)]:
        r=author.equal_remainders(a,b,c,d)
        want={'assumptions':a==b and c==d,'conclusion':a-c==b-d,'implication':not(a==b and c==d) or a-c==b-d,'remainders':(Fraction(a)-c,Fraction(b)-d)}
        require(r==want,'rational example')
        arithmetic.append({k:list(map(str,v)) if k=='remainders' else v for k,v in r.items()})
    counts['exact_arithmetic_instances']=arithmetic
    # Main prose set assignments, preserving the bits documented by the author.
    sets=[({'a'},{'b'},{'a','b'}),({'s'},{'p'},{'m'}),({'s'},{'s'},{'m'}),({'a','b'},{'a'},{'a'}),({'a'},{'b'},set())]
    prose=[]
    for S,P,M in sets:
        U=S|P|M
        mask=encode([(x in S,x in P,x in M) for x in U])
        require(all(author.proposition(mask,f,s,p)==oracle(rows(mask),f,s,p) for f,s,p in itertools.product(FORMS,NAMES,NAMES)),'prose')
        prose.append(mask)
    counts['prose_model_masks']=prose
    named=[(96,1,'III'),(24,2,'EEE'),(96,2,'AAA'),(1,3,'AAI'),(130,3,'AAA')]
    for mask,fig,mood in named: require(author.evaluate(mask,fig,mood)==(True,True,False),'named countermodel')
    require((author.proposition(96,'I','M','P'),author.proposition(96,'A','S','M'),author.proposition(96,'A','S','P'))==(True,True,False),'music')
    require(author.classify(3,'AAI','all_terms_nonempty')['valid'],'AAI nonempty')
    counts['named_examples_checked']=7
    manifest=json.loads((ROOT/'author-manifest.json').read_text())['sha256']
    for path,digest in manifest.items(): require(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,'author manifest '+path)
    counts['author_hashes_matched']=len(manifest)
    print(json.dumps(counts,ensure_ascii=False,indent=2))
if __name__=='__main__':run()
