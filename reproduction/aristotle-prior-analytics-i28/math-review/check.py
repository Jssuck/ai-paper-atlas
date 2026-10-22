import itertools,json

def require(b,why):
    if not b: raise RuntimeError(why)
def goals(a,e):return [e<=a,not(e&a),bool(e&a),bool(e-a)]
U=set(range(5));sets=[{i for i in U if bits>>i&1} for bits in range(32)]
counts=dict.fromkeys(['CF','CG','DF','BH','DG','BG'],0)
for a,e,m in itertools.product(sets,repeat=3):
    conditions=[m<=a and e<=m,m<=a and m<=e and bool(m),not(a&m) and e<=m,a<=m and not(e&m),not(a&m) and m<=e and bool(m),a<=m and m<=e and bool(a)]
    results=[e<=a,bool(e&a),not(e&a),not(e&a),bool(e-a),bool(e&a)]
    for rule,cond,result in zip(counts,conditions,results):
        if cond:require(result,rule);counts[rule]+=1
# Section 6 paired models: every target has one countermodel; all named sets nonempty.
pairs={'BF':[({1},{1},{1,2}),({1},{2},{1,2})], 'CH':[({1,2},{2},{1}),({1},{2},{1})], 'DH':[({1},{1},{3}),({1},{2},{3})]}
for r,pair in pairs.items():
    for a,e,m in pair:
        require(bool(a) and bool(e) and bool(m),'nonempty')
        require({'BF':a<=m and e<=m,'CH':m<=a and not(e&m),'DH':not(a&m) and not(e&m)}[r],r+' premises')
    require(all(any(not goals(a,e)[j] for a,e,m in pair) for j in range(4)),r+' all four countered')
# Higher-class pruning, partial-overlap and tail warning.
a={1,2};e={1};j={1,2};k={1,2,3}
require(e<=j<=k and not(k<=a) and j<=a and e<=a,'higher class')
x={1,2};y={2,3};e={1};a={2,3}
require(e<=x and y<=a and bool(x&y) and not(e<=a),'overlap')
a=p={1};e={1,2};q={2}
require(a<=p and q<=e and bool(q) and not(p&q) and bool(e-a) and bool(p&e),'tail countermodel')
S=[{i for i in range(4) if bits>>i&1} for bits in range(16)]
red={'BF_to_BH':0,'BG_to_DG':0,'BG_not_BH':0}
for a,e,p,q in itertools.product(S,repeat=4):
    if a<=p and e<=q and not(p&q):
        require(not(p&e) and not(a&e),'BF reduction');red['BF_to_BH']+=1
    if a<=p and q<=e and bool(q) and not(p&q):
        require(not(a&q) and bool(e-a),'BG repair');red['BG_to_DG']+=1
        if p&e:red['BG_not_BH']+=1
require(red['BG_not_BH']>0,'tail defect witnessed')
print(json.dumps({'triple_assignments':32**3,'rule_antecedent_cases':counts,'paired_countermodels':6,'target_refutations':12,'quadruple_assignments':16**4,'reductions':red,'status':'PASS','scope':'finite checks supplement arbitrary-object proofs; no historical or general theorem certified'},sort_keys=True,indent=2))
