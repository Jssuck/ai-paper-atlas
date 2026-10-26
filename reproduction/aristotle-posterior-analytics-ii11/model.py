"""Finite teaching models for APo II.11; not historical causal discovery."""
from dataclasses import dataclass
from itertools import product
import json

ROLES = ('essence', 'necessitating_conditions', 'moving_origin', 'end')

def chain(a, b, c):
    """Return two premises and conclusion for finite sets C subset B subset A."""
    a,b,c=map(frozenset,(a,b,c))
    return {'c_in_b':c<=b, 'b_in_a':b<=a, 'c_in_a':c<=a}

def element_oracle(a,b,c,universe):
    """Independent per-element reading, with explicit supplied domain validation."""
    u=frozenset(universe); a,b,c=map(frozenset,(a,b,c))
    if not (a|b|c)<=u: raise ValueError('sets must lie in domain')
    return {'c_in_b':all(x not in c or x in b for x in u),
            'b_in_a':all(x not in b or x in a for x in u),
            'c_in_a':all(x not in c or x in a for x in u)}

def subsets(n):
    if type(n) is not int or n<0: raise ValueError('nonnegative integer required')
    return [frozenset(i for i in range(n) if bits>>i&1) for bits in range(1<<n)]

@dataclass(frozen=True)
class Explanation:
    role: str
    target: str
    middle: str
    premises: tuple[str,str]
    source: str

    def __post_init__(self):
        if self.role not in ROLES: raise ValueError('unknown declared role')
        if not all(type(x) is str and x.strip() for x in (self.target,self.middle,self.source)):
            raise ValueError('nonempty labels and source required')
        if type(self.premises) is not tuple or len(self.premises)!=2 or not all(type(p) is str and p.strip() for p in self.premises):
            raise ValueError('exactly two nonempty premise labels required')

    def report(self):
        return {'role':self.role,'target':self.target,'middle':self.middle,
                'premises':list(self.premises),'source':self.source,
                'certifies_real_cause':False}

@dataclass(frozen=True)
class Scenario:
    goal_represented: bool
    action: bool
    mechanism_enabled: bool
    background_holds: bool

    def __post_init__(self):
        if any(type(v) is not bool for v in (self.goal_represented,self.action,self.mechanism_enabled,self.background_holds)):
            raise ValueError('strict Boolean inputs required')

    @property
    def outcome(self):
        # This equation is a stipulated toy mechanism, not an empirical law.
        return self.action and self.mechanism_enabled and self.background_holds

    @property
    def goal_and_success(self):
        # Compatibility of represented goal and outcome; no intention detector.
        return self.goal_represented and self.outcome

def planning_order(goal_time,action_time,outcome_time):
    """Check only a stipulated intentional-plan chronology; not all final causes."""
    if any(type(t) is not int for t in (goal_time,action_time,outcome_time)):
        raise ValueError('integer teaching times required')
    return goal_time<=action_time<outcome_time

def enumerate_chains(max_n=4):
    if type(max_n) is not int or max_n<0: raise ValueError('nonnegative bound required')
    total=valid=empty=violations=disagreements=missing_major=missing_minor=0
    for n in range(max_n+1):
        ss=subsets(n)
        for a,b,c in product(ss,repeat=3):
            total+=1; r=chain(a,b,c)
            disagreements+=r!=element_oracle(a,b,c,range(n))
            if r['c_in_b'] and r['b_in_a']:
                valid+=1; empty+=not c; violations+=not r['c_in_a']
            missing_major+=r['c_in_b'] and not r['c_in_a']
            missing_minor+=r['b_in_a'] and not r['c_in_a']
    return dict(combinations=total,valid_chains=valid,empty_subject_valid=empty,
                violations=violations,oracle_disagreements=disagreements,
                counterexamples_without_major=missing_major,counterexamples_without_minor=missing_minor)

def enumerate_scenarios():
    cases=[Scenario(*v) for v in product((False,True),repeat=4)]
    return {'cases':len(cases),'goal_without_action':sum(s.goal_represented and not s.action for s in cases),
            'goal_without_outcome':sum(s.goal_represented and not s.outcome for s in cases),
            'goal_and_success':sum(s.goal_and_success for s in cases),
            'outcome_without_goal':sum(s.outcome and not s.goal_represented for s in cases),
            'goal_toggle_changes_mechanism':sum(Scenario(False,*v).outcome!=Scenario(True,*v).outcome for v in product((False,True),repeat=3))}

def main():
    print(json.dumps({'chains':enumerate_chains(),'scenarios':enumerate_scenarios(),
        'chronologies':{'checked':27,'accepted':sum(planning_order(*ts) for ts in product(range(3),repeat=3))}},indent=2))
if __name__=='__main__':main()
