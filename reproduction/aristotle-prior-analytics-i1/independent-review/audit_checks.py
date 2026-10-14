"""Independent review, authored separately from test_model.py.

No production-private helpers or author test oracle are imported. Set semantics
are the primary oracle. Labelled universes intentionally retain duplicates.
All checks use explicit exceptions, so -O/-OO cannot erase the checks.
"""
from collections import Counter
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import argparse
import json
import sys

PARSER = argparse.ArgumentParser()
PARSER.add_argument('--module-root', type=Path, default=Path(__file__).resolve().parents[1])
PARSER.add_argument('--quick', action='store_true')
PARSER.add_argument('--section', choices=('all','validation','semantics','rules','entails'), default='all')
ARGS = PARSER.parse_args()
sys.path.insert(0, str(ARGS.module_root.resolve()))
from logic import Language, Model, Prop, ValidationError, entails, enumerate_models, evaluate, is_admissible
from proofs import Step, check_certificate

COUNTS = Counter()
ORACLE_CACHE = {}

def check(condition, message):
    if not condition:
        raise RuntimeError(message)

def reject(label, fn):
    try:
        fn()
    except ValidationError:
        COUNTS['invalid_inputs_rejected'] += 1
        return
    except Exception as exc:
        raise RuntimeError(f'{label}: wrong exception {type(exc).__name__}: {exc}') from exc
    raise RuntimeError(f'{label}: malformed input was accepted')

def truth(prop, extensions):
    left, right = extensions[prop.subject], extensions[prop.predicate]
    if prop.kind == 'A':
        return left <= right
    if prop.kind == 'E':
        return left.isdisjoint(right)
    if prop.kind == 'I':
        return bool(left & right)
    if prop.kind == 'O':
        return bool(left - right)
    raise RuntimeError('oracle kind is not AEIO')

def all_subsets(seq):
    return [frozenset(c) for size in range(len(seq) + 1) for c in combinations(seq, size)]

def support_extensions(terms, support):
    # Decoding is separate from production; the oracle itself works only on sets.
    extensions = {t: set() for t in terms}
    for obj in support:
        digits = bin(obj)[2:].zfill(len(terms))[::-1]
        for term, digit in zip(terms, digits):
            if digit == '1':
                extensions[term].add(obj)
    return extensions

def props_for(terms):
    return tuple(Prop(kind, s, p) for kind, s, p in product('AEIO', terms, terms))

def all_supports(terms):
    types = list(range(2 ** len(terms)))
    return [tuple(sorted(s)) for s in all_subsets(types) if s]

def check_supports_and_labelled():
    for k in (1, 2, 3):
        terms = ('alpha', 'beta', 'gamma')[:k]
        props = props_for(terms)
        supports = all_supports(terms)
        for required in all_subsets(terms):
            lang = Language(terms, required)
            expected = {s for s in supports if all(support_extensions(terms, s)[t] for t in required)}
            actual = enumerate_models(lang)
            check(len(actual) == len(expected), f'support count k={k} policy={required}')
            check({m.support for m in actual} == expected, 'support enumeration mismatch')
            masks = [sum(2 ** t for t in m.support) for m in actual]
            check(masks == sorted(masks), 'support enumeration order changed')
            COUNTS['support_policies'] += 1
            for support in supports:
                expected_allowed = support in expected
                check(is_admissible(lang, Model(terms, support)) == expected_allowed, 'admissibility mismatch')
                COUNTS['admissibility_cases'] += 1
        for support in supports:
            ext = support_extensions(terms, support)
            model = Model(terms, support)
            for p in props:
                check(type(evaluate(p, model)) is bool, 'non-Boolean truth result')
                check(evaluate(p, model) == truth(p, ext), f'support truth {p} {support}')
                COUNTS['support_truth_cases'] += 1
        # Independent labelled domains: every k-tuple of extensions on {0,..,n-1}.
        for n in range(1, 5):
            domain = tuple(range(n))
            choices = all_subsets(domain)
            for term_sets in product(choices, repeat=k):
                ext = dict(zip(terms, term_sets))
                encoded = tuple(sorted({sum(2 ** pos for pos, t in enumerate(terms) if x in ext[t]) for x in domain}))
                model = Model(terms, encoded)
                COUNTS['labelled_models'] += 1
                for p in props:
                    check(evaluate(p, model) == truth(p, ext), f'labelled compression {k} {n} {p} {ext}')
                    COUNTS['labelled_truth_cases'] += 1

def compare_entails(lang, premises, conclusion, table):
    if lang not in ORACLE_CACHE:
        allowed = {s for s, ext in table if all(ext[t] for t in lang.required_nonempty)}
        truths = {p: {s for s, ext in table if s in allowed and truth(p, ext)} for p in props_for(lang.terms)}
        ORACLE_CACHE[lang] = allowed, truths
    admissible, truths = ORACLE_CACHE[lang]
    good = set(admissible)
    for premise in premises:
        good &= truths[premise]
    counter = good - truths[conclusion]
    actual = entails(lang, premises, conclusion)
    check(actual.holds == (not counter), f'entailment mismatch {premises} {conclusion}')
    check(actual.satisfying_premise_models == len(good), 'premise-model count mismatch')
    check(actual.admissible_models == len(admissible), 'admissible count mismatch')
    if counter:
        check(actual.countermodel is not None, 'missing countermodel')
        check(actual.countermodel.terms == lang.terms, 'wrong-language countermodel')
        check(actual.countermodel.support in counter, 'invalid countermodel')
        # Production specifies integer-mask order, not minimum cardinality.
        first = min(counter, key=lambda s: sum(2 ** t for t in s))
        check(actual.countermodel.support == first, 'nondeterministic/nonfirst countermodel')
        COUNTS['returned_countermodels'] += 1
    else:
        check(actual.countermodel is None, 'spurious countermodel')
    COUNTS['full_entails_calls'] += 1

def check_entailments():
    for k in (1, 2, 3):
        terms = ('alpha', 'beta', 'gamma')[:k]
        props = props_for(terms)
        table = [(s, support_extensions(terms, s)) for s in all_supports(terms)]
        for required in all_subsets(terms):
            lang = Language(terms, required)
            for p in props:
                compare_entails(lang, (), p, table)
                compare_entails(lang, (p, p), p, table)
            pairs = tuple(combinations_with_replacement(props, 2))
            if k == 3 and (required or ARGS.quick):
                # Deterministic coverage distinct from author's test selectors.
                triples = ((pairs[(j * 137 + 19) % len(pairs)], props[(j * 17 + j // 36) % len(props)]) for j in range(180))
            else:
                triples = ((pair, c) for pair in pairs for c in props)
            for pair, conclusion in triples:
                compare_entails(lang, pair, conclusion, table)

def expected_rule(rule, inputs):
    # Independent contract, deliberately not calling _derived_claim.
    if rule == 'e_sym':
        first, = inputs
        return Prop('E', first.predicate, first.subject) if first.kind == 'E' else None
    first, second = inputs
    kinds = {'a_trans': ('A', 'A', 'A'), 'e_down': ('A', 'E', 'E'),
             'i_up': ('I', 'A', 'I'), 'o_from_i_e': ('I', 'E', 'O')}
    a, b, output = kinds[rule]
    if first.kind == a and second.kind == b and first.predicate == second.subject:
        return Prop(output, first.subject, second.predicate)
    return None

def check_rule_acceptance():
    terms = ('alpha', 'beta', 'gamma')
    lang = Language(terms)
    props = props_for(terms)
    extensions = [support_extensions(terms, s) for s in all_supports(terms)]
    for rule in ('e_sym', 'a_trans', 'e_down', 'i_up', 'o_from_i_e'):
        arity = 1 if rule == 'e_sym' else 2
        for premises in product(props, repeat=arity):
            expected = expected_rule(rule, premises)
            assumptions = tuple(Step(p, 'assume', assumption=i) for i, p in enumerate(premises))
            for conclusion in props:
                steps = assumptions + (Step(conclusion, rule, tuple(range(arity))),)
                try:
                    report = check_certificate(lang, premises, conclusion, steps)
                except ValidationError:
                    accepted = False
                else:
                    accepted = report.accepted
                    check(report.used_assumptions == tuple(range(arity)), 'wrong direct dependencies')
                    check(report.unused_assumptions == (), 'spurious unused dependencies')
                    check(report.repeats_assumption == (conclusion in premises), 'repeat flag mismatch')
                check(accepted == (expected == conclusion), f'rule direction/type/output {rule} {premises} {conclusion}')
                COUNTS['certificate_rule_acceptance_cases'] += 1
            if expected is not None:
                for ext in extensions:
                    check(not all(truth(p, ext) for p in premises) or truth(expected, ext), f'unsound rule {rule}')
                    COUNTS['rule_soundness_model_cases'] += 1
                COUNTS['valid_rule_instances'] += 1

def check_dependencies_and_invalid():
    lang = Language(('alpha', 'beta', 'gamma'))
    p = Prop('A', 'alpha', 'beta')
    q = Prop('E', 'gamma', 'beta')
    r = Prop('E', 'beta', 'gamma')
    goal = Prop('E', 'alpha', 'gamma')
    extra = Prop('I', 'gamma', 'gamma')
    # Scramble premise indices and step order; ensure only final ancestors count.
    premises = (extra, q, p, p)
    steps = (Step(extra, 'assume', assumption=0), Step(p, 'assume', assumption=3),
             Step(q, 'assume', assumption=1), Step(r, 'e_sym', (2,)),
             Step(goal, 'e_down', (1, 3)))
    report = check_certificate(lang, premises, goal, steps)
    check(report.used_assumptions == (1, 3), 'transitive dependency lost or overcounted')
    check(report.unused_assumptions == (0, 2), 'duplicate/unused assumption confusion')
    check(not report.repeats_assumption and report.step_count == 5, 'report metadata wrong')
    repeat = check_certificate(lang, premises, p, (Step(p, 'assume', assumption=2),))
    check(repeat.used_assumptions == (2,) and repeat.unused_assumptions == (0,1,3) and repeat.repeats_assumption, 'repeat or duplicate premise indices wrong')
    COUNTS['dependency_dag_cases'] += 2
    invalid = [
        ('foreign language order', lambda: is_admissible(lang, Model(tuple(reversed(lang.terms)), (0,)))),
        ('foreign vocabulary', lambda: is_admissible(lang, Model(('x','y','z'), (0,)))),
        ('foreign conclusion', lambda: entails(lang, (), Prop('A','x','beta'))),
        ('foreign premise', lambda: entails(lang, (Prop('I','alpha','x'),), p)),
        ('list premises', lambda: entails(lang, [p], p)),
        ('not Language', lambda: enumerate_models(None)),
        ('not Model', lambda: evaluate(p, {})),
        ('not Prop', lambda: evaluate(None, Model(lang.terms,(0,)))),
        ('not certificate tuple', lambda: check_certificate(lang, (p,), p, [])),
        ('empty certificate', lambda: check_certificate(lang, (p,), p, ())),
        ('not Step', lambda: check_certificate(lang, (p,), p, (p,))),
        ('undeclared premise index', lambda: check_certificate(lang,(p,),q,(Step(q,'assume',assumption=1),))),
        ('premise substitution', lambda: check_certificate(lang,(p,),q,(Step(q,'assume',assumption=0),))),
        ('unused illegal premise', lambda: check_certificate(lang,(p,),p,(Step(q,'assume',assumption=1),Step(p,'assume',assumption=0)))),
        ('wrong final goal', lambda: check_certificate(lang,(p,q),p,(Step(q,'assume',assumption=1),))),
        ('assumption reference forbidden', lambda: Step(p,'assume',(0,),0)),
        ('derived premise import forbidden', lambda: Step(r,'e_sym',(0,),1)),
        ('unknown rule', lambda: Step(r,'i_sym',(0,))),
    ]
    for bad in (True, False, -1, 1.5, '0', None):
        invalid += [(f'assumption {bad!r}', lambda bad=bad: Step(p,'assume',assumption=bad)),
                    (f'ref {bad!r}', lambda bad=bad: Step(r,'e_sym',(bad,)))]
    for bad in ((), (False,), (True,), (-1,), (8,), (0,0), (2,1), [0], (1.0,)):
        invalid.append((f'support {bad!r}', lambda bad=bad: Model(lang.terms,bad)))
    for bad in ((), ('x','x'), ('x','y','z','w'), ('',), (' x',), (True,), ['x']):
        invalid.append((f'terms {bad!r}', lambda bad=bad: Language(bad)))
    for bad in (set(), frozenset(('x',)), frozenset((True,))):
        invalid.append((f'policy {bad!r}', lambda bad=bad: Language(lang.terms,bad)))
    for bad in ('a', '', True, None):
        invalid.append((f'kind {bad!r}', lambda bad=bad: Prop(bad,'alpha','beta')))
    for bad in ('', ' x', 'x ', None, True, 1):
        invalid.append((f'prop name {bad!r}', lambda bad=bad: Prop('A',bad,'alpha')))
    for refs in ((1,), (2,), (99,)):
        invalid.append((f'self or forward {refs}', lambda refs=refs: check_certificate(lang,(q,),r,(Step(q,'assume',assumption=0),Step(r,'e_sym',refs)))))
    invalid.append(('unused invalid derived', lambda: check_certificate(lang,(q,p),p,(Step(q,'assume',assumption=0),Step(q,'e_sym',(0,)),Step(p,'assume',assumption=1)))))
    for label, fn in invalid:
        reject(label, fn)
    # Malformed exact-class objects, constructed by bypassing the normal frozen API.
    # This is robustness, not a claim that Python is a hostile-runtime sandbox.
    for field, value in (('assumption',-1),('assumption',True),('refs',(0,)),('rule','unknown')):
        forged = Step(p,'assume',assumption=0)
        object.__setattr__(forged,field,value)
        reject(f'forged Step {field}={value!r}', lambda forged=forged: check_certificate(lang,(p,p),p,(forged,)))
    for kind in ('UNKNOWN', True):
        forged = Prop('A','alpha','beta')
        object.__setattr__(forged,'kind',kind)
        reject('forged Prop',lambda forged=forged: evaluate(forged,Model(lang.terms,(1,))))
    forged = Model(lang.terms,(1,))
    object.__setattr__(forged,'support',(True,))
    reject('forged Model support bool',lambda: evaluate(p,forged))
    for cls, call in ((Prop, lambda obj: evaluate(obj,Model(lang.terms,(0,)))),
                      (Model, lambda obj: evaluate(p,obj)),
                      (Language, lambda obj: enumerate_models(obj)),
                      (Step, lambda obj: check_certificate(lang,(p,),p,(obj,)))):
        incomplete = object.__new__(cls)
        reject('incomplete '+cls.__name__,lambda incomplete=incomplete,call=call: call(incomplete))
    class DerivedProp(Prop):
        pass
    reject('Prop subclass',lambda: evaluate(DerivedProp('A','alpha','beta'),Model(lang.terms,(0,))))
    forged_lang = Language(lang.terms)
    object.__setattr__(forged_lang,'required_nonempty',frozenset(('missing',)))
    reject('forged Language',lambda: entails(forged_lang,(),p))

def main():
    for section, label, fn in [('validation','input_and_dependency_checks',check_dependencies_and_invalid),
                      ('semantics','support_and_labelled_oracle',check_supports_and_labelled),
                      ('rules','exhaustive_rule_acceptance',check_rule_acceptance),
                      ('entails','full_entailment_oracle',check_entailments)]:
        if ARGS.section not in ('all',section):
            continue
        fn()
        print('PASS '+label, flush=True)
    print(json.dumps({'passed': True, 'quick': ARGS.quick, 'counts': dict(sorted(COUNTS.items()))}, sort_keys=True), flush=True)

if __name__ == '__main__':
    main()
