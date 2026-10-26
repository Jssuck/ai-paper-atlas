"""II.10 teaching records: rearrangement preserves supplied content, not its truth."""
from dataclasses import dataclass
from itertools import product
import json

def nonempty_text(*values):
    if any(not isinstance(v, str) or not v.strip() for v in values):
        raise ValueError('Terms and source identifiers must be nonempty strings')

@dataclass(frozen=True)
class Proof:
    subject: str
    middle: str
    predicate: str
    major_source: str
    minor_source: str
    def __post_init__(self):
        nonempty_text(self.subject,self.middle,self.predicate,self.major_source,self.minor_source)

@dataclass(frozen=True)
class CausalDefinition:
    subject: str
    predicate: str
    because_middle: str
    minor_source: str
    major_source: str
    def __post_init__(self):
        nonempty_text(self.subject,self.predicate,self.because_middle,self.minor_source,self.major_source)

def to_definition(p):
    if not isinstance(p,Proof): raise TypeError('Proof record required')
    return CausalDefinition(p.subject,p.predicate,p.middle,p.minor_source,p.major_source)

def to_proof(d):
    if not isinstance(d,CausalDefinition): raise TypeError('CausalDefinition record required')
    return Proof(d.subject,d.because_middle,d.predicate,d.major_source,d.minor_source)

def conclusion(p):
    if not isinstance(p,Proof): raise TypeError('Proof record required')
    return (p.subject,p.predicate)

def chain_report(p,domain,interpretation):
    """Check given finite extensions. Sources are labels, not verified evidence."""
    if not isinstance(p,Proof): raise TypeError('Proof record required')
    u=frozenset(domain)
    sets=[]
    for term in (p.subject,p.middle,p.predicate):
        if term not in interpretation: raise ValueError('Missing term interpretation')
        extension=frozenset(interpretation[term])
        if not extension <= u: raise ValueError('Extension outside domain')
        sets.append(extension)
    s,m,a=sets
    return {'minor':s<=m,'major':m<=a,'conclusion':s<=a,
            'subject_exists':bool(s)}

def nominal_lookup(name,lexicon):
    """Retrieve a supplied phrase only; no existence or essence inference."""
    nonempty_text(name)
    return lexicon.get(name)

def enumerate_chains(max_n=4):
    if type(max_n) is not int or not 0<=max_n<=6: raise ValueError('max_n must be integer 0..6')
    total=valid=violations=oracle_disagreements=empty_valid=0
    p=Proof('S','M','A','major-given','minor-given')
    for n in range(max_n+1):
        u=set(range(n))
        for sm,mm,am in product(range(1<<n),repeat=3):
            ex=lambda bits:{i for i in range(n) if bits>>i&1}
            r=chain_report(p,u,{'S':ex(sm),'M':ex(mm),'A':ex(am)})
            # Independent per-member Boolean implication, not set subset.
            minor=all(not(sm>>i&1) or mm>>i&1 for i in range(n))
            major=all(not(mm>>i&1) or am>>i&1 for i in range(n))
            result=all(not(sm>>i&1) or am>>i&1 for i in range(n))
            total+=1
            oracle_disagreements+=r['minor']!=minor or r['major']!=major or r['conclusion']!=result
            if r['minor'] and r['major']:
                valid+=1;empty_valid+=not r['subject_exists'];violations+=not r['conclusion']
    return dict(total=total,valid_chains=valid,empty_subject_valid=empty_valid,
                transitivity_violations=violations,oracle_disagreements=oracle_disagreements)

def enumerate_records():
    groups={}; total=roundtrip_errors=0
    for s,m,a,x,y in product(('A','B','C'),('A','B','C'),('A','B','C'),('src1','src2'),('src1','src2')):
        p=Proof(s,m,a,x,y);total+=1
        roundtrip_errors+=to_proof(to_definition(p))!=p
        groups.setdefault(conclusion(p),[]).append(p)
    return dict(records=total,conclusions=len(groups),roundtrip_errors=roundtrip_errors,
                preimages_per_conclusion=sorted({len(v) for v in groups.values()}))

def experiment():
    return {'finite_chains':enumerate_chains(),'record_conversion':enumerate_records(),
            'interpretation':'Record roundtrip does not certify reality, causes, essence, or scientific knowledge.'}

if __name__=='__main__':print(json.dumps(experiment(),ensure_ascii=False,indent=2))
