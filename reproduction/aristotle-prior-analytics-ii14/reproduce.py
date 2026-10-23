"""Original finite teaching model of Prior Analytics II.14; not textual adjudication."""
from dataclasses import dataclass, asdict
import json

TERMS = 'ABC'
KINDS = 'UEIO'
@dataclass(frozen=True)
class Proposition:
    kind: str
    pred: str
    subj: str
    def __post_init__(self):
        if self.kind not in tuple(KINDS) or self.pred not in tuple(TERMS) or self.subj not in tuple(TERMS):
            raise ValueError('Expected one U/E/I/O kind and one A/B/C term per slot')
        if self.pred == self.subj:
            raise ValueError('This experiment requires distinct term slots')
    def negate(self):
        return Proposition(dict(U='O', O='U', E='I', I='E')[self.kind], self.pred, self.subj)

@dataclass(frozen=True)
class Route:
    name: str
    internal_figure: int
    direct_figure: int
    target: Proposition
    fixed: Proposition
    background: Proposition
    internal_result: Proposition
    location: str
    @property
    def hypothesis(self):
        return self.target.negate()

def p(s):
    if not isinstance(s, str) or len(s) != 3:
        raise ValueError('Use a three-character proposition such as UAB')
    return Proposition(*s)

def route(name, internal, direct, target, fixed, background, result, location):
    return Route(name, internal, direct, p(target), p(fixed), p(background), p(result), location)

ROUTES = (
 route('F1_E_positive_fixed',1,2,'EAB','UCA','ECB','ICB','63a7–14'),
 route('F1_O_positive_fixed',1,2,'OAB','UCA','OCB','UCB','63a14–18'),
 route('F1_E_negative_fixed',1,2,'EAB','ECA','UCB','OCB','63a17–18'),
 route('F1_O_negative_fixed',1,2,'OAB','ECA','ICB','ECB','63a17–18'),
 route('F1_I_both_universal',1,3,'IAB','UBC','UAC','EAC','63a18–24'),
 route('F1_I_A_particular',1,3,'IAB','UBC','IAC','EAC','63a18–24'),
 route('F1_I_B_particular',1,3,'IAB','IBC','UAC','OAC','63a23–24'),
 route('F2_U',2,1,'UAB','UAC','UCB','OCB','63a25–29'),
 route('F2_I',2,1,'IAB','UAC','ICB','ECB','63a29–32'),
 route('F2_E',2,1,'EAB','EAC','UCB','OCB','63a32–35'),
 route('F2_O',2,1,'OAB','EAC','ICB','ECB','63a35–38'),
 route('F3_U',3,1,'UAB','UCB','UAC','OAC','63a39–63b3'),
 route('F3_I',3,1,'IAB','ICB','UAC','OAC','63b3–5'),
 route('F3_E',3,2,'EAB','UCB','ECA','ICA','63b5–8'),
 route('F3_O',3,2,'OAB','ICB','ECA','IAC','63b8–10'),
)

def validate_model(model):
    if type(model) is not int or not 1 <= model <= 255:
        raise ValueError('A model is a nonempty set of the eight A/B/C membership types (1..255)')

def extension(model, term):
    validate_model(model)
    if term not in tuple(TERMS):
        raise ValueError('Unknown term')
    bit = 1 << TERMS.index(term)
    return frozenset(t for t in range(8) if model & (1 << t) and t & bit)

def holds(model, prop):
    if not isinstance(prop, Proposition):
        raise TypeError('Expected Proposition')
    pred, subj = extension(model, prop.pred), extension(model, prop.subj)
    return {'U': subj <= pred, 'E': not bool(subj & pred), 'I': bool(subj & pred), 'O': bool(subj - pred)}[prop.kind]

def models(policy):
    if policy not in ('empty_allowed', 'all_terms_nonempty', 'C_nonempty'):
        raise ValueError('Unknown existence policy')
    return tuple(m for m in range(1,256) if policy == 'empty_allowed' or
                 (policy == 'all_terms_nonempty' and all(extension(m,t) for t in TERMS)) or
                 (policy == 'C_nonempty' and extension(m,'C')))

def witness(model):
    if model is None: return None
    return {'mask':model, 'domain_types':[t for t in range(8) if model & (1<<t)],
            'extensions':{t:sorted(extension(model,t)) for t in TERMS}}

def smallest(items):
    return min(items, key=lambda m:(m.bit_count(),m),default=None)

def implication(ms, premises, conclusion):
    satisfying = [m for m in ms if all(holds(m,x) for x in premises)]
    bad = [m for m in satisfying if not holds(m, conclusion)]
    return {'valid':not bad,'premise_models':len(satisfying),'countermodels':len(bad),
            'smallest_countermodel':witness(smallest(bad))}

def check_route(r, policy):
    ms=models(policy)
    overlap=[m for m in ms if holds(m,r.background) and holds(m,r.internal_result)]
    return {'name':r.name,'internal_figure':r.internal_figure,'direct_figure':r.direct_figure,
            'target':asdict(r.target),'hypothesis':asdict(r.hypothesis),
            'fixed':asdict(r.fixed),'background':asdict(r.background),
            'internal_result':asdict(r.internal_result),'location':r.location,
            'internal':implication(ms,(r.fixed,r.hypothesis),r.internal_result),
            'direct':implication(ms,(r.fixed,r.background),r.target),
            'conflict':{'incompatible':not overlap,'overlap_models':len(overlap),
                        'smallest_overlap':witness(smallest(overlap))},
            'reverse_refutation':implication(ms,(r.fixed,r.hypothesis),r.background.negate())}

def run():
    out={'scope':'15 chapter-based teaching routes; not enumeration of every syllogism or historical semantics',
         'policies':{}}
    for policy in ('empty_allowed','all_terms_nonempty','C_nonempty'):
        records=[check_route(r,policy) for r in ROUTES]
        out['policies'][policy]={'model_count':len(models(policy)),'routes':records,
            'summary':{k:sum(x[k]['valid'] for x in records) for k in ('internal','direct','reverse_refutation')},
            'conflicts':sum(x['conflict']['incompatible'] for x in records)}
    return out

if __name__ == '__main__':
    print(json.dumps(run(),ensure_ascii=False,indent=2,sort_keys=True))
