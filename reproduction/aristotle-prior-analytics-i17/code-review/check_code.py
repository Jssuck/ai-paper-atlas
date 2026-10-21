"""Independent set-based oracle and bounded mutation audit; standard library only."""
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import platform
import sys
import types

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import model
import demo


def ensure(test, reason):
    if not test:
        raise RuntimeError(reason)


def extension(n, row, term):
    # Decode masks via binary text, not the author's membership operation.
    return {i for i, digit in enumerate(format(row['ABC'.index(term)], '0%db' % n)[::-1]) if digit == '1'}


def oracle(n, worlds, actual, p, s, form, mode):
    universe = set(range(n))
    subject = extension(n, worlds[actual], s)
    ext = [extension(n, row, p) for row in worlds]
    if form in ('E', 'O'):
        ext = [universe - part for part in ext]
    if mode == 'actual':
        eligible = ext[actual]
    elif mode == 'necessary':
        eligible = set.intersection(*ext)
    elif mode == 'possible':
        eligible = set.union(*ext)
    else:
        eligible = set.union(*ext) - set.intersection(*ext)
    return subject <= eligible if form in ('A', 'E') else bool(subject & eligible)


def configurations():
    for n, nw in ((1, 1), (1, 2), (1, 3), (2, 1), (2, 2)):
        for flat in itertools.product(range(2**n), repeat=3*nw):
            worlds = tuple(tuple(flat[i:i+3]) for i in range(0, len(flat), 3))
            for actual in range(nw):
                yield n, worlds, actual


def exhaustive(module):
    counts = dict(configurations=0, categorical=0, extensions=0, profiles=0, witnesses=0, joint=0, branch_equivalences=0)
    for n, worlds, actual in configurations():
        m = module.Model(n, worlds, actual)
        counts['configurations'] += 1
        for p in 'ABC':
            for w in range(len(worlds)):
                ensure(m.extension(p, w) == extension(n, worlds[w], p), 'extension')
                counts['extensions'] += 1
            for x in range(n):
                expected = tuple(x in extension(n, row, p) for row in worlds)
                ensure(m.profile(p, x) == expected, 'profile')
                counts['profiles'] += 1
            for s in 'ABC':
                for f, mode in itertools.product('AEIO', ('actual', 'necessary', 'possible', 'contingent')):
                    ensure(m.categorical(p, s, f, mode) == oracle(n, worlds, actual, p, s, f, mode), 'categorical '+f+':'+mode)
                    counts['categorical'] += 1
                subject = extension(n, worlds[actual], s)
                exts = [extension(n, row, p) for row in worlds]
                positive = sorted(subject & set.intersection(*exts))
                negative = sorted(subject - set.union(*exts))
                ensure(m.noncontingency_witnesses(p,s) == {'necessary_positive': positive, 'necessary_negative':negative}, 'witnesses')
                counts['witnesses'] += 1
                ensure((not oracle(n, worlds, actual,p,s,'A','contingent')) == bool(positive or negative), 'branch disjunction')
                counts['branch_equivalences'] += 1
                for sign in (False,True):
                    expected = any(subject <= part if sign else not subject & part for part in exts)
                    ensure(m.jointly_possible(p,s,sign) == expected, 'joint')
                    counts['joint'] += 1
    return counts


def invalid(module):
    probes=[]
    row=((0,0,0),)
    for bad in (0,-1,True,False,1.0,'1',None,[],{}):
        probes.append(lambda bad=bad:module.Model(bad,row))
    for bad in ((),[],None,1,'',((0,0),),([0,0,0],),((0,0,0,0),)):
        probes.append(lambda bad=bad:module.Model(1,bad))
    for bad in (-1,2,True,False,0.0,'0',None,[],{}):
        probes.append(lambda bad=bad:module.Model(1,((bad,0,0),)))
    for bad in (-1,1,True,False,0.0,'0',None,[],{}):
        probes.append(lambda bad=bad:module.Model(1,row,bad))
    m=module.Model(1,row)
    for bad in ('D','',None,[],{},1,True):
        probes.extend((lambda bad=bad:m.extension(bad),lambda bad=bad:m.profile(bad,0),lambda bad=bad:m.categorical(bad,'B'),lambda bad=bad:m.categorical('A',bad),lambda bad=bad:m.noncontingency_witnesses(bad,'B'),lambda bad=bad:m.jointly_possible(bad,'B')))
    for bad in (-1,1,True,False,0.0,'0',[],{}):
        probes.extend((lambda bad=bad:m.extension('A',bad),lambda bad=bad:m.profile('A',bad)))
    for bad in ('X','',None,[],{},1,True):
        probes.extend((lambda bad=bad:m.categorical('A','B',bad),lambda bad=bad:m.categorical('A','B','A',bad)))
    for bad in (1,0,None,[],{},'yes'):
        probes.append(lambda bad=bad:m.jointly_possible('A','B',bad))
    for args in ((0,),(-1,),(True,),(1,0),(1,False),(1,1.0)):
        probes.append(lambda args=args:list(module.models(*args)))
    for i, f in enumerate(probes):
        try:f()
        except ValueError:pass
        else:raise RuntimeError('invalid input accepted '+str(i))
    return len(probes)


def endpoint():
    rows=demo.endpoint_checks()
    ensure(len(rows)==16,'endpoint length')
    ensure({tuple(r['premises']) for r in rows}==set(itertools.product('AEIO',repeat=2)),'premise coverage')
    examples=model.examples()
    count=0
    for row in rows:
        for name in ('disjoint','identical'):
            m=examples[name]
            for subject,f in zip('BC',row['premises']):
                ensure(oracle(m.n,m.worlds,m.actual,'A',subject,f,'contingent'),'endpoint premise')
        ensure(set(row['countermodels'])=={mode+':'+f for mode,f in itertools.product(model.MODALITIES,'AEIO')},'conclusion coverage')
        for key,names in row['countermodels'].items():
            mode,f=key.split(':')
            expected=[name for name in ('disjoint','identical') if not oracle(examples[name].n,examples[name].worlds,examples[name].actual,'B','C',f,mode)]
            ensure(names==expected and bool(names),'endpoint witnesses')
            count+=1
    return count


def mutants():
    src=(ROOT/'model.py').read_text()
    changes={
      'contingency_becomes_weak':('answer = any(signed) and not all(signed)','answer = any(signed)'),
      'necessary_becomes_possible':('answer = all(signed)','answer = any(signed)'),
      'possible_becomes_necessary':('answer = any(signed)','answer = all(signed)'),
      'actual_point_ignored':('answer = signed[self.actual]','answer = signed[0]'),
      'subject_point_ignored':('subjects = self.extension(subject)','subjects = self.extension(subject, 0)'),
      'existential_becomes_universal':("return all(answers) if form in ('A', 'E') else any(answers)","return all(answers)"),
      'negative_quality_lost':("positive = form in ('A', 'I')","positive = True"),
      'negative_branch_dropped':('negative.append(obj)','pass'),
      'joint_becomes_objectwise':('return any(s <= p if positive else s.isdisjoint(p) for p in possibilities)',"return self.categorical(predicate, subject, 'A' if positive else 'E', 'possible')"),
      'bool_domain_accepted':('type(self.n) is not int','not isinstance(self.n, int)'),
    }
    result={}
    for label,(old,new) in changes.items():
        ensure(src.count(old)>=1,'mutation anchor '+label)
        name='_mutant_'+label
        mod=types.ModuleType(name)
        sys.modules[name]=mod
        exec(compile(src.replace(old,new,1),label,'exec'),mod.__dict__)
        try:
            if label=='bool_domain_accepted':invalid(mod)
            else:exhaustive(mod)
        except RuntimeError as error:result[label]=str(error)
        else:raise RuntimeError('surviving mutant '+label)
        finally:sys.modules.pop(name,None)
    return result


if __name__=='__main__':
    out={'scope':'independent finite set oracle; not general proof or ancient semantics certification','python':platform.python_version(),'optimization':sys.flags.optimize,'oracle':exhaustive(model),'invalid_probes':invalid(model),'endpoint_refutations':endpoint(),'detected_mutants':mutants()}
    print(json.dumps(out,ensure_ascii=False,indent=2))
