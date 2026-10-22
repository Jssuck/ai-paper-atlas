"""Original finite relational teaching model; not an ancient-language parser."""

class Invalid(ValueError):
    """Malformed expression, fact or certificate."""

def name(s):
    if type(s) is not str or not s or not s.isascii() or not s.replace('_','a').isalnum():
        raise Invalid('nonempty ASCII alphanumeric/underscore name required')
    return s

def expression(e):
    if type(e) is not tuple or not e:
        raise Invalid('expression must be tuple')
    if e[0]=='atom' and len(e)==2:
        name(e[1])
    elif e[0]=='some' and len(e)==3:
        name(e[1]); expression(e[2])
    else:
        raise Invalid('unknown expression')
    return e

def fact(f):
    if type(f) is not tuple or not f: raise Invalid('fact must be tuple')
    if f[0] in ('member','notmember') and len(f)==3:
        expression(f[1]); name(f[2])
    elif f[0] in ('subset','disjoint','not_subset') and len(f)==3:
        expression(f[1]); expression(f[2])
    elif f[0]=='edge' and len(f)==4:
        for n in f[1:]: name(n)
    else: raise Invalid('unknown fact')
    return f

def infer(rule, inputs):
    """Return the uniquely determined conclusion; premises must be trusted."""
    if type(rule) is not str or type(inputs) is not tuple or len(inputs)!=2:
        raise Invalid('each rule requires exactly two facts')
    a,b=map(fact,inputs)
    if rule=='project' and a[0]=='member' and b[0]=='edge' and a[2]==b[2]:
        return ('member',('some',b[1],a[1]),b[3])
    if rule=='instantiate' and a[0]=='subset' and b[0]=='member' and a[1]==b[1]:
        return ('member',a[2],b[2])
    if rule=='transitive' and a[0]==b[0]=='subset' and a[2]==b[1]:
        return ('subset',a[1],b[2])
    if rule=='exclude' and a[0]=='disjoint' and b[0]=='member' and a[1]==b[1]:
        return ('notmember',a[2],b[2])
    if rule=='difference' and a[0]=='member' and b[0]=='notmember' and a[2]==b[2]:
        return ('not_subset',a[1],b[1])
    raise Invalid('rule pattern, expression or witness mismatch')

def check(premises, steps):
    """Steps {rule,refs,conclusion}; exact keys, backward integer references."""
    if type(premises) is not tuple or type(steps) is not tuple: raise Invalid('tuple inputs required')
    facts=[fact(p) for p in premises]
    for step in steps:
        if type(step) is not dict or set(step)!={'rule','refs','conclusion'}:
            raise Invalid('unexpected step fields')
        refs=step['refs']
        if type(refs) is not tuple or len(refs)!=2 or any(type(i) is not int or i<0 or i>=len(facts) for i in refs):
            raise Invalid('references must be two prior indices')
        out=infer(step['rule'],tuple(facts[i] for i in refs))
        if fact(step['conclusion'])!=out: raise Invalid('claimed conclusion differs')
        facts.append(out)
    return tuple(facts)

class Model:
    def __init__(self, universe, atoms, relations):
        if type(universe) is not frozenset or not universe: raise Invalid('nonempty frozenset universe')
        for u in universe:name(u)
        if type(atoms) is not dict or type(relations) is not dict: raise Invalid('dict interpretations required')
        for k,v in atoms.items():
            name(k)
            if type(v) is not frozenset or not v<=universe:raise Invalid('invalid atom extension')
        for k,v in relations.items():
            name(k)
            if type(v) is not frozenset or any(type(p) is not tuple or len(p)!=2 or any(x not in universe for x in p) for p in v):raise Invalid('invalid relation extension')
        self.universe=universe;self.atoms=atoms.copy();self.relations=relations.copy()
    def extension(self,e):
        expression(e)
        if e[0]=='atom':
            if e[1] not in self.atoms: raise Invalid('uninterpreted atom')
            return self.atoms[e[1]]
        if e[1] not in self.relations:raise Invalid('uninterpreted relation')
        source=self.extension(e[2])
        return frozenset(t for s,t in self.relations[e[1]] if s in source)
    def true(self,f):
        fact(f)
        k=f[0]
        if k=='edge':
            if f[1] not in self.relations or f[2] not in self.universe or f[3] not in self.universe:raise Invalid('uninterpreted edge')
            return (f[2],f[3]) in self.relations[f[1]]
        a=self.extension(f[1])
        if k in ('member','notmember'):
            if f[2] not in self.universe:raise Invalid('uninterpreted individual')
            return (f[2] in a)==(k=='member')
        b=self.extension(f[2])
        return {'subset':a<=b,'not_subset':not a<=b,'disjoint':not bool(a&b)}[k]
